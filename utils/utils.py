"""Clase general"""
class Utils():

    @staticmethod
    def ingresarId(mensaje):
        """
        Solicita y retorna el id 
        """
        id = 0
        id_incorrecto = True
        while id_incorrecto:
            try:
                id = int(input(mensaje))
                id_incorrecto = False
            except Exception as e:
                print("Error al capturar el id: {}".format(e))
                print("Intente de nuevo ingresar el id \n")
        return id