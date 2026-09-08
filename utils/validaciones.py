import re


class Validaciones:
    CODIGO = re.compile(r"^[A-Za-z0-9_-]+$")
    TEXTO = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 .,'()-]+$")
    PERSONA = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ .'-]+$")

    @classmethod
    def vehiculo(cls, codigo, nombre, piloto):
        errores = {}
        codigo = str(codigo).strip()
        nombre = " ".join(str(nombre).strip().split())
        piloto = " ".join(str(piloto).strip().split())

        if not 2 <= len(codigo) <= 20 or not cls.CODIGO.fullmatch(codigo):
            errores["codigo"] = "Use 2 a 20 caracteres alfanuméricos, guion o guion bajo."
        if not 2 <= len(nombre) <= 50 or not cls.TEXTO.fullmatch(nombre):
            errores["nombre"] = "Use un nombre de 2 a 50 caracteres válidos."
        if not 2 <= len(piloto) <= 50 or not cls.PERSONA.fullmatch(piloto):
            errores["piloto"] = "Use un nombre de piloto de 2 a 50 caracteres, sin números."
        return errores
