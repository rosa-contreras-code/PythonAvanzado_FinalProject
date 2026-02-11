"""
Módulo menú
Contiene la clase Menú para la gestión de productos.
"""
from database.bd import BD
from utils.utils import Utils
import sqlite3
class Menu:
    """
    Clase Menu
    Representa los productos disponibles en el menú.
    """
    def __init__(self):
        """
        Inicializa la estructura de datos para almacenar productos
        """
        self.bd = BD('happyburger.db')

    def mostrarListaMenu(self):
        """
        Regresa una lista de productos registrados
        """
        try: 
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM menu")
            menu = cursor.fetchall()

            if len(menu) > 0:
                print("--------------------------------------------------")
                print("Menú:")
                for id, clave, nombre, precio in menu:
                    print("ID: {}, Clave: {}, Nombre: {}, Precio: {}".format(id, clave, nombre, precio))
            else:
                print("No hay productos registrados")

        except sqlite3.Error as e:
            print("Error al intentar obtener el menú: {}".format(e))
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def buscarProducto(self, id_menu):
        """
        Busca y regresa un producto por su id
        """
        try: 
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM menu WHERE id = ?", (id_menu,))
            producto = cursor.fetchone()
            if not producto:
                print(f"No se encontró un producto con el id {id_menu}")
                return producto

            return {
                "id": producto[0],
                "clave": producto[1],
                "nombre": producto[2],
                "precio": producto[3]
            }
        except Exception as e:
            print("Error al buscar el producto: {}".format(e))
        finally:
            if conexion:
                cursor.close()
                conexion.close()
    
    def buscarProductoPorNombre(self, nombre_producto):
        """
        Busca y regresa un producto por su nombre
        """
        try: 
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM menu WHERE nombre = ?", (nombre_producto,))
            producto = cursor.fetchone()
            if not producto:
                print(f"No se encontró un producto con el nombre {nombre_producto}")
                return producto

            return {
                "id": producto[0],
                "clave": producto[1],
                "nombre": producto[2],
                "precio": producto[3]
            }
        except Exception as e:
            print("Error al buscar el producto: {}".format(e))
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def agregarProducto(self):
        """
        Agrega un nuevo producto al menú
        """
        try:
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            print("--------------------------------------------------")
            print("Nuevo producto")
            producto = self.ingresarDatosProducto()
            if not producto:
                print("Operación cancelada")
                return
            
            sql = '''INSERT INTO menu(clave, nombre, precio)
            VALUES(?,?,?)'''
            cursor.execute(sql, (producto["clave"], producto["nombre"], producto["precio"],))
            conexion.commit()

            print("Producto guardado correctamente")
        except sqlite3.Error as e:
            print('Ocurró un error al intentar guardar los datos {}'.format(e))
        except Exception as e:
            print(f'Error: {e}')
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def actualizarProducto(self):
        """
        Actualiza la información de un producto existente
        """
        try:
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            self.mostrarListaMenu()
            print("--------------------------------------------------")
            id_menu = Utils.ingresarId("Ingrese el id del producto a editar (para cancelar teclee la palabra esc): ")
            if not id_menu:
                print("Operación cancelada")
                return
            
            if not self.buscarProducto(id_menu):
                return
            producto = self.ingresarDatosProducto()
            if not producto:
                print("Operación cancelada")
                return
            
            sql ="UPDATE menu SET clave = ?, nombre = ?, precio = ? WHERE id = ?"
            valores =  (producto["clave"], producto["nombre"], producto["precio"], id_menu)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Producto actualizado correctamente")
        except sqlite3.Error as e:
            print(f"Ocurrió un error al intentar actualizar el producto: {e}")
        except Exception as e:
            print("Error:".format(e))
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def eliminarProducto(self):
        """
        Elimina un producto del menú
        """
        try:
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            self.mostrarListaMenu()
            print("--------------------------------------------------")
            id_menu = Utils.ingresarId("Ingrese el id del producto a eliminar (para cancelar teclee la palabra esc): ")
            if not id_menu:
                print("Operación cancelada")
                return
            
            if not self.buscarProducto(id_menu):
                return
            sql = '''DELETE FROM menu WHERE id = ?'''
            cursor.execute(sql, (id_menu,))
            conexion.commit()
            print("Producto eliminado correctamente")
        except sqlite3.Error as e:
            print(f"Ocurrió un error al intentar eliminar el producto: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def ingresarDatosProducto(self):
        """
        Solicita y retorna los datos de un producto
        """
        datosIncorrectos = True
        while datosIncorrectos:
            try:
                print("Datos del producto (para cancelar teclee la palabra esc)")
                clave = input("Ingrese la clave del producto: ")
                if clave == "esc": return {}
                nombre = input("Ingrese en nombre del producto: ")
                if nombre == "esc": return {}
                precio = input("Ingrese el precio del producto: ")
                if precio == "esc": return {}
                precio = float(precio)
                datosIncorrectos = False
            except Exception as e:
                print('Error al capturar un dato: {}'.format(e))
                print('Intente de nuevo \n')
        return {
            "clave": clave,
            "nombre": nombre,
            "precio": precio
        }