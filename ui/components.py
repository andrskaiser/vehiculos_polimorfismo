import streamlit as st


def toastr(mensaje, tipo="success"):
    """Helper de notificaciones. Usa el toast nativo de Streamlit."""
    iconos = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
    }
    st.toast(mensaje, icon=iconos.get(tipo, "ℹ️"))


def titulo_seccion(titulo, ayuda=""):
    st.markdown(f'<div class="section-title">{titulo}</div>', unsafe_allow_html=True)
    if ayuda:
        st.markdown(f'<div class="section-help">{ayuda}</div>', unsafe_allow_html=True)


def tarjeta_metrica(etiqueta, valor, detalle=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{etiqueta}</div>
            <div class="metric-value">{valor}</div>
            <div class="metric-detail">{detalle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
