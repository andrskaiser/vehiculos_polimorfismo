import pandas as pd
import streamlit as st

from models.vehiculo import VehiculoFactory
from services.simulacion import SimuladorCarrera
from ui.components import tarjeta_metrica, titulo_seccion, toastr
from ui.styles import aplicar_estilos
from utils.validaciones import Validaciones

st.set_page_config(page_title="Sistema de vehículos", page_icon="🏁", layout="wide")
aplicar_estilos()


def vehiculos_demo():
    return [
        VehiculoFactory.crear("Deportivo", "DEP-01", "Deportivo 01", "Camila Soto"),
        VehiculoFactory.crear("Deportivo", "DEP-02", "Deportivo 02", "Martín Rojas"),
        VehiculoFactory.crear("Clásico", "CLA-01", "Clásico 01", "Valentina Díaz"),
        VehiculoFactory.crear("Clásico", "CLA-02", "Clásico 02", "Tomás Pérez"),
        VehiculoFactory.crear("Uso diario", "DIA-01", "Uso diario 01", "Daniela Muñoz"),
        VehiculoFactory.crear("Uso diario", "DIA-02", "Uso diario 02", "Felipe Silva"),
    ]


if "vehiculos" not in st.session_state:
    st.session_state.vehiculos = vehiculos_demo()
if "ultima_simulacion" not in st.session_state:
    st.session_state.ultima_simulacion = None

st.markdown(
    """
    <div class="app-header">
      <div class="app-mark">V</div>
      <div>
        <div class="app-title">Gestión de vehículos</div>
        <div class="app-subtitle">Polimorfismo, simulación secuencial y concurrencia</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

pagina = st.radio(
    "Navegación",
    ["Resumen", "Vehículos", "Carrera", "Resultados"],
    horizontal=True,
    label_visibility="collapsed",
)


def df_vehiculos():
    return pd.DataFrame([v.resumen() for v in st.session_state.vehiculos]).drop(
        columns=["Distancia"]
    )


if pagina == "Resumen":
    total = len(st.session_state.vehiculos)
    tipos = len({v.tipo for v in st.session_state.vehiculos})
    c1, c2, c3 = st.columns(3)
    with c1:
        tarjeta_metrica(
            "Vehículos registrados", total, "Instancias activas en la sesión"
        )
    with c2:
        tarjeta_metrica("Tipos disponibles", tipos, "Subclases de Vehículo")
    with c3:
        estado = "Disponible" if total >= 2 else "Faltan vehículos"
        tarjeta_metrica("Carrera", estado, "Se requieren al menos dos participantes")

    izquierda, derecha = st.columns([3.45, 1.25], gap="large")
    with izquierda:
        with st.container(border=True):
            titulo_seccion(
                "Participantes",
                "Listado principal con la estructura visual solicitada.",
            )
            st.dataframe(
                df_vehiculos(), hide_index=True, use_container_width=True, height=355
            )
        with st.container(border=True):
            titulo_seccion("Modelo aplicado")
            st.markdown(
                "La clase abstracta **Vehículo** concentra datos comunes y reglas de encapsulamiento. "
                "Las clases **Deportivo**, **Clásico** y **Uso diario** sobrescriben `calcular_avance()`. "
                "La carrera concurrente crea un `threading.Thread` independiente por vehículo."
            )
    with derecha:
        with st.container(border=True):
            titulo_seccion("Panel de operaciones", "Acciones rápidas")
            if st.button("Ir a Vehículos", use_container_width=True):
                toastr("Seleccione Vehículos en el menú superior.", "info")
            if st.button("Preparar carrera", type="primary", use_container_width=True):
                toastr("Seleccione Carrera en el menú superior.", "info")
            st.markdown(
                '<div class="small-note">La interfaz utiliza un menú superior, un panel principal amplio y un panel lateral de menor tamaño, siguiendo la distribución de la referencia entregada.</div>',
                unsafe_allow_html=True,
            )

elif pagina == "Vehículos":
    izquierda, derecha = st.columns([3.45, 1.25], gap="large")
    with izquierda:
        with st.container(border=True):
            titulo_seccion(
                "Catálogo de vehículos",
                "Cada fila corresponde a una instancia de una subclase.",
            )
            tabla = df_vehiculos()
            evento = st.dataframe(
                tabla,
                hide_index=True,
                use_container_width=True,
                height=420,
                on_select="rerun",
                selection_mode="single-row",
                key="tabla_vehiculos",
            )
            seleccionado = None
            if evento.selection.rows:
                seleccionado = st.session_state.vehiculos[evento.selection.rows[0]]
                st.caption(
                    f"Seleccionado: {seleccionado.codigo} · {seleccionado.tipo} · {seleccionado.nombre}"
                )
    with derecha:
        with st.container(border=True):
            titulo_seccion("Panel de vehículos", "Crear o eliminar participantes")
            modo = st.radio(
                "Operación",
                ["Nuevo", "Eliminar"],
                horizontal=True,
                label_visibility="collapsed",
            )
            if modo == "Nuevo":
                with st.form("nuevo_vehiculo"):
                    tipo = st.selectbox("Tipo", VehiculoFactory.TIPOS)
                    codigo = st.text_input("Código", placeholder="DEP-03")
                    nombre = st.text_input("Nombre", placeholder="Deportivo 03")
                    piloto = st.text_input("Piloto", placeholder="Nombre y apellido")
                    guardar = st.form_submit_button(
                        "Agregar vehículo", type="primary", use_container_width=True
                    )
                if guardar:
                    errores = Validaciones.vehiculo(codigo, nombre, piloto)
                    if codigo.strip() in {v.codigo for v in st.session_state.vehiculos}:
                        errores["codigo"] = "El código ya se encuentra registrado."
                    if errores:
                        for mensaje in errores.values():
                            st.error(mensaje)
                        toastr("Revise los datos ingresados.", "error")
                    else:
                        st.session_state.vehiculos.append(
                            VehiculoFactory.crear(tipo, codigo, nombre, piloto)
                        )
                        toastr("Vehículo agregado correctamente.")
                        st.rerun()
            else:
                codigos = [v.codigo for v in st.session_state.vehiculos]
                if codigos:
                    codigo = st.selectbox("Vehículo", codigos)
                    confirmar = st.checkbox("Confirmo la eliminación")
                    if st.button(
                        "Eliminar", disabled=not confirmar, use_container_width=True
                    ):
                        st.session_state.vehiculos = [
                            v for v in st.session_state.vehiculos if v.codigo != codigo
                        ]
                        st.session_state.ultima_simulacion = None
                        toastr("Vehículo eliminado.", "warning")
                        st.rerun()
                else:
                    st.info("No existen vehículos registrados.")
            if st.button("Restaurar datos de demostración", use_container_width=True):
                st.session_state.vehiculos = vehiculos_demo()
                st.session_state.ultima_simulacion = None
                toastr("Datos de demostración restaurados.", "info")
                st.rerun()

elif pagina == "Carrera":
    izquierda, derecha = st.columns([3.45, 1.25], gap="large")
    with izquierda:
        with st.container(border=True):
            titulo_seccion(
                "Participantes de la carrera",
                "La misma carga se ejecuta primero en forma secuencial y luego concurrente.",
            )
            st.dataframe(
                df_vehiculos(), hide_index=True, use_container_width=True, height=330
            )
            st.markdown(
                '<div class="small-note">Los intervalos y las variaciones se precalculan con una semilla. De esta forma ambos modos reciben exactamente el mismo plan de trabajo y la comparación de tiempo es directa.</div>',
                unsafe_allow_html=True,
            )
    with derecha:
        with st.container(border=True):
            titulo_seccion("Configuración", "Parámetros de simulación")
            tramos = st.slider("Tramos", 3, 10, 6)
            avance = st.number_input(
                "Avance base", min_value=20.0, max_value=500.0, value=100.0, step=10.0
            )
            espera_min = st.number_input(
                "Espera mínima (s)",
                min_value=0.05,
                max_value=1.0,
                value=0.12,
                step=0.01,
            )
            espera_max = st.number_input(
                "Espera máxima (s)",
                min_value=0.05,
                max_value=1.5,
                value=0.30,
                step=0.01,
            )
            semilla = st.number_input(
                "Semilla", min_value=1, max_value=9999, value=30, step=1
            )
            ejecutar = st.button(
                "Ejecutar comparación", type="primary", use_container_width=True
            )
            if ejecutar:
                if len(st.session_state.vehiculos) < 2:
                    st.error("Registre al menos dos vehículos.")
                    toastr("No hay participantes suficientes.", "error")
                elif espera_max < espera_min:
                    st.error("La espera máxima debe ser igual o mayor que la mínima.")
                    toastr("Revise los intervalos de tiempo.", "error")
                else:
                    simulador = SimuladorCarrera(tramos, avance, espera_min, espera_max)
                    plan = simulador.crear_plan(st.session_state.vehiculos, semilla)
                    with st.spinner("Ejecutando versión secuencial..."):
                        sec, hist_sec, t_sec = simulador.ejecutar_secuencial(
                            st.session_state.vehiculos, plan
                        )
                    with st.spinner("Ejecutando versión concurrente..."):
                        con, hist_con, t_con = simulador.ejecutar_concurrente(
                            st.session_state.vehiculos, plan
                        )
                    comparacion = simulador.comparar(t_sec, t_con)
                    st.session_state.ultima_simulacion = {
                        "secuencial": sec,
                        "concurrente": con,
                        "historial_secuencial": hist_sec,
                        "historial_concurrente": hist_con,
                        "comparacion": comparacion,
                    }
                    toastr("Comparación finalizada correctamente.")
                    st.rerun()

else:
    datos = st.session_state.ultima_simulacion
    if not datos:
        st.info(
            "Ejecute una comparación desde la sección Carrera para generar resultados."
        )
    else:
        comp = datos["comparacion"]
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            tarjeta_metrica(
                "Secuencial", f'{comp["Secuencial_s"]:.3f} s', "Tiempo total medido"
            )
        with c2:
            tarjeta_metrica(
                "Concurrente", f'{comp["Concurrente_s"]:.3f} s', "Tiempo total medido"
            )
        with c3:
            tarjeta_metrica(
                "Reducción",
                f'{comp["Reducción_%"]:.2f} %',
                "Diferencia respecto del modo secuencial",
            )
        with c4:
            tarjeta_metrica(
                "Aceleración",
                f'{comp["Aceleración_x"]:.2f}x',
                "Relación secuencial/concurrente",
            )

        izquierda, derecha = st.columns([3.45, 1.25], gap="large")
        with izquierda:
            with st.container(border=True):
                titulo_seccion(
                    "Clasificación concurrente",
                    "Resultados ordenados por distancia final.",
                )
                df_con = pd.DataFrame(datos["concurrente"])
                df_con.insert(0, "Posición", range(1, len(df_con) + 1))
                st.dataframe(
                    df_con, hide_index=True, use_container_width=True, height=310
                )
            with st.container(border=True):
                titulo_seccion("Comparación de tiempos")
                df_tiempos = pd.DataFrame(
                    {
                        "Modo": ["Secuencial", "Concurrente"],
                        "Segundos": [comp["Secuencial_s"], comp["Concurrente_s"]],
                    }
                ).set_index("Modo")
                st.bar_chart(df_tiempos, height=280)
            with st.container(border=True):
                titulo_seccion("Progreso por tramo")
                progreso = pd.DataFrame(datos["historial_concurrente"])
                tabla = progreso.pivot(
                    index="Tramo", columns="Vehículo", values="Distancia"
                )
                st.line_chart(tabla, height=300)
        with derecha:
            with st.container(border=True):
                titulo_seccion("Lectura del resultado")
                ganador = datos["concurrente"][0]
                st.markdown(f"**Ganador:** {ganador['Vehículo']}")
                st.caption(f"Tipo: {ganador['Tipo']} · Piloto: {ganador['Piloto']}")
                st.metric("Distancia", f"{ganador['Distancia']:.2f}")
                st.divider()
                st.markdown(
                    f"La versión concurrente redujo el tiempo total en **{comp['Reducción_%']:.2f}%** "
                    f"para esta ejecución. El resultado se obtiene porque los vehículos esperan y avanzan de forma superpuesta, "
                    "en lugar de completar toda la tarea de un vehículo antes de iniciar el siguiente."
                )
