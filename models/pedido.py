"""
Módulo pedido
Contiene la clase Pedido para la gestión de pedidos del sistema.
"""
from cliente import Cliente
from menu import Menu
from utils import Utils
from database.bd import BD
import sqlite3
import os
from datetime import datetime

class Pedido:
    """
    Clase Pedido
    Representa los pedidos realizados por los clientes.
    """
    def __init__(self):
        """
        Inicializa la estructura de datos para almacenar pedidos
        """
        # self.pedidos = {}
        self.bd = BD('happyburger.db')
        self.cliente = Cliente()
        self.menu = Menu()

    def mostrarListaPedidos(self):
        """
        Regresa una lista de pedidos registrados
        """
        try: 
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM pedido")
            pedidos = cursor.fetchall()

            if len(pedidos) > 0:
                print("--------------------------------------------------")
                print("Pedidos:")
                for id, cliente, producto, cantidad, precio in pedidos:
                    print("ID: {}, Cliente: {}, Producto: {}, Cantidad: {}, Total: {}".format(id, cliente, producto, cantidad, precio))
            else:
                print("No hay pedidos registrados")

        except sqlite3.Error as e:
            print("Error al intentar obtener los pedidos: {}".format(e))
        finally:
            print("--------------------------------------------------")
            if conexion:
                cursor.close()
                conexion.close()

    def buscarPedido(self, id_pedido):
        """
        Busca y regresa un pedido por su id
        """
        try: 
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM pedido WHERE id = ?", (id_pedido,))
            pedido = cursor.fetchone()
            if not pedido:
                print(f"No se encontró un pedido con el id {id_pedido}")
                return pedido

            return {
                "id": pedido[0],
                "cliente": pedido[1],
                "producto": pedido[2],
                "cantidad": pedido[3],
                "precio": pedido[4]
            }
        except Exception as e:
            print("Error al buscar el pedido: {}".format(e))
        finally:
            print("--------------------------------------------------")
            if conexion:
                cursor.close()
                conexion.close()

    def crearPedido(self):
        """
        Crea un nuevo pedido
        """
        try:
            print("Nuevo Pedido")
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()

            self.cliente.mostrarListaClientes()
            id_cliente = Utils.ingresarId("Ingrese el id del cliente: ")
            cliente = self.cliente.buscarCliente(id_cliente)
            if not cliente: return

            self.menu.mostrarListaMenu()
            id_menu = Utils.ingresarId("Ingrese el id del producto: ")
            producto = self.menu.buscarProducto(id_menu)
            if not producto: return

            cantidad = int(input("Ingrese la cantidad: "))
            total = producto["precio"] * cantidad

            sql = '''INSERT INTO pedido(cliente, producto, cantidad, precio)
                    VALUES(?, ?, ?, ?)'''
            valores = (cliente["nombre"], producto["nombre"], cantidad, total,)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Pedido registrado correctamente")
            self.imprimirTicket({
                "cliente": cliente["nombre"],
                "producto": producto["nombre"],
                "precioUnitario": producto["precio"],
                "cantidad": cantidad,
                "total": total
                })
        except sqlite3.Error as e:
            print("Ocurrió un error al registrar el pedido: {}".format(e))
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def cancelarPedido(self):
        """
        Cancela un pedido existente
        """
        try:
            conexion = self.bd.abrirConexion()
            cursor = conexion.cursor()
            self.mostrarListaPedidos()
            id_pedido = Utils.ingresarId("Ingrese el id del pedido a cancelar: ")
            if not self.buscarPedido(id_pedido):
                return
            sql = '''DELETE FROM pedido WHERE id = ?'''
            cursor.execute(sql, (id_pedido,))
            conexion.commit()
            print("Pedido cancelado correctamente")
        except sqlite3.Error as e:
            print(f"Ocurrió un error al intentar cancelar el pedido: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()
    
    def imprimirTicket(self, pedido):
        """
        Genera un archivo .txt con el ticket del pedido
        """
        try:
            os.makedirs("tickets", exist_ok=True)
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nombre_archivo = f"tickets/ticket_{fecha.replace(':','-')}.txt"
            with open(nombre_archivo, 'w', encoding="utf-8") as ticket:
                ticket.write("============================ TICKET DE COMPRA ============================\n")
                ticket.write(f"Fecha: {fecha}\n")
                ticket.write("Cliente: {}\n".format(pedido["cliente"]))
                ticket.write("--------------------------------------------------------------------------\n")
                ticket.write("Producto: {}, Cantidad: {}, Precio unitario: ${}\n".format(pedido["producto"], pedido["cantidad"], pedido["precioUnitario"]))
                ticket.write("--------------------------------------------------------------------------\n")
                ticket.write("Total: ${}\n".format(pedido["total"]))
                ticket.write("==========================================================================\n")
                ticket.write("Gracias por su compra, vuelva pronto\n")
            print("Ticket generado correctamente")
        except Exception as e:
            print("Error: {}".format(e))


