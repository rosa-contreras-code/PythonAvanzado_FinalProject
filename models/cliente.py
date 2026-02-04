"""
Módulo clientes
Contiene la clase Cliente para la gestión de clientes.
"""
from database.bd import BD
from utils.utils import Utils
import sqlite3

class Cliente:
    """
    Clase Cliente
    Representa la estructura y operaciones relacionadas con los clientes.
    """
    def __init__(self):
        """
        Inicializa la estructura de datos para almacenar clientes
        """
        # self.clientes = {}
        "Verifica la existencia de la tabla"
        self.bd = BD('happyburger.db')
        # if self.bd.verificarBaseDatosExiste():
        #     pass
        # else:
        #     self.bd.crearBaseDatos()
        #     self.bd.crearTablaClientes()
    
    def mostrarListaClientes(self):
        """
        Regresa una lista de clientes registrados
        """
        try: 
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()

            if len(clientes) > 0:
                print("--------------------------------------------------")
                print("Lista de clientes:")
                for id, clave, nombre, direccion, correo_electronico, telefono in clientes:
                    print("ID: {}, Clave: {}, Nombre: {}, Dirección: {}, Correo electrónico: {}, Teléfono: {}".format(id, clave, nombre, direccion, correo_electronico, telefono))
            else:
                print("No hay clientes registrados")

        except sqlite3.Error as e:
            print("Error al intentar obtener la lista de clientes: {}".format(e))
        finally:
            print("--------------------------------------------------")
            if conexion:
                cursor.close()
                conexion.close()

    def buscarCliente(self, id_cliente):
        """
        Busca y regresa un cliente por su id
        """
        try: 
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,))
            cliente = cursor.fetchone()
            if not cliente:
                print(f"No se encontró un cliente con el id {id_cliente}")
                return cliente
            
            return {
                "id": cliente[0],
                "clave": cliente[1],
                "nombre": cliente[2],
                "direccion": cliente[3],
                "correo": cliente[4],
                "telefono": cliente[5]
            }
        except Exception as e:
            print("Error al buscar el cliente: {}".format(e))
        finally:
            print("--------------------------------------------------")
            if conexion:
                cursor.close()
                conexion.close()


    def agregarCliente(self):
        """
        Agrega un nuevo cliente al sistema
        """
        try:
            print("--------------------------------------------------")
            print("Nuevo cliente")
            cliente = self.ingresarDatosCliente()

            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            sql = '''INSERT INTO clientes(clave, nombre, direccion, correo_electronico, telefono)
            VALUES(?,?,?,?,?)'''
            cursor.execute(sql, (cliente["clave"], cliente["nombre"], cliente["direccion"], cliente["correo_electronico"], cliente["telefono"]))
            conexion.commit()

            print("Cliente guardado correctamente")
        except sqlite3.Error as e:
            print('Ocurró un error al intentar guardar los datos {}'.format(e))
        except Exception as e:
            print(f'Error: {e}')
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def actualizarCliente(self):
        """
        Actualiza la información de un cliente existente
        """
        try:
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            self.mostrarListaClientes()
            id_cliente = Utils.ingresarId("Ingrese el id del cliente a editar: ")
            if not self.buscarCliente(id_cliente):
                return
            cliente = self.ingresarDatosCliente()
            sql ="UPDATE clientes SET clave = ?, nombre = ?, direccion = ?, correo_electronico = ?, telefono = ? WHERE id = ?"
            valores =  (cliente["clave"], cliente["nombre"], cliente["direccion"], cliente["correo_electronico"], cliente["telefono"], id_cliente)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Cliente actualizado correctamente")
        except sqlite3.Error as e:
            print(f"Ocurrió un error al intentar actualizar el cliente: {e}")
        except Exception as e:
            print("Error:".format(e))
        finally:
            print("--------------------------------------------------")
            if conexion:
                cursor.close()
                conexion.close()
        
    def eliminarCliente(self):
        """
        Elimina un cliente del sistema
        """
        try:
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            self.mostrarListaClientes()
            id_cliente = Utils.ingresarId("Ingrese el id del cliente a eliminar: ")
            if not self.buscarCliente(id_cliente):
                return
            sql = '''DELETE FROM clientes WHERE id = ?'''
            cursor.execute(sql, (id_cliente,))
            conexion.commit()
            print("Cliente eliminado correctamente")
        except sqlite3.Error as e:
            print(f"Ocurrió un error al intentar eliminar el cliente: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def ingresarDatosCliente(self):
        """
        Solicita y retorna los datos de un cliente
        """
        datosIncorrectos = True
        while datosIncorrectos:
            try:
                clave = input("Ingrese la clave del cliente: ")
                nombre = input("Ingrese en nombre del cliente: ")
                direccion = input("Ingrese la dirección del cliente: ")
                correo_electronico = input("Ingrese la dirección de correó electrónico del cliente: ")
                telefono = input("Ingrese el teléfono del cliente: ")
                datosIncorrectos = False
            except Exception as e:
                print('Error al capturar un dato: {}'.format(e))
                print('Intente de nuevo \n')
        return {
            "clave": clave,
            "nombre": nombre,
            "direccion": direccion,
            "correo_electronico": correo_electronico,
            "telefono": telefono
        }

    # def ingresarId(self, mensaje):
    #     """
    #     Solicita y retorna el id de un cliente
    #     """
    #     id_cliente = 0
    #     id_incorrecto = True
    #     while id_incorrecto:
    #         try:
    #             id_cliente = int(input(mensaje))
    #             id_incorrecto = False
    #         except Exception as e:
    #             print("Error al capturar el id: {}".format(e))
    #             print("Intente de nuevo ingresar el id \n")
    #     return id_cliente