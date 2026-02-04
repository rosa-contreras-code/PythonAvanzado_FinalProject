"""
Archivo principal del proyecto
"""
from models.cliente import Cliente
from models.menu import Menu
from models.pedido import Pedido
from database.bd import BD

def inicializarBaseDatos():
    """
    Función que asegura que existan la base de datos y tablas necesarias
    """
    bd = BD("happyburger.db")
    if not bd.verificarBaseDatosExiste():
        bd.crearBaseDatos()

    bd.crearTablaClientes()
    bd.crearTablaMenu()
    bd.crearTablaPedido()


def imprimirMenu():
    """
    Función que imprime el menú principal
    """
    print("--------------------------------------------------")
    print("Bienvenido a Happy Burger")
    print("1-Pedido")
    print("2-Clientes")
    print("3-Menu")
    print("4-Salir")
    print("--------------------------------------------------")

def imprimirSubMenuCliente():
    """
    Función que imprime el menú de clientes
    """
    print("--------------------------------------------------")
    print("Gestión de clientes")
    print("1-Consulta de clientes")
    print("2-Agregar un nuevo Cliente")
    print("3-Editar un cliente")
    print("4-Eliminar un cliente")
    print("5-Regresar al menú anterior")
    print("--------------------------------------------------")

def imprimirSubMenuMenu():
    """
    Función que imprime el menú del menú de Happy burger
    """
    print("--------------------------------------------------")
    print("Gestión del menú Happy Buger")
    print("1-Consulta del menú")
    print("2-Agregar un producto al menú")
    print("3-Editar un producto del menú")
    print("4-Eliminar un producto del menú")
    print("5-Regresar al menú anterior")
    print("--------------------------------------------------")

def imprimirSubMenuPedido():
    """
    Función que imprime el menú de pedidos
    """
    print("--------------------------------------------------")
    print("Gestión del pedidos")
    print("1-Consultar pedidos")
    print("2-Crear un nuevo pedido")
    print("3-cancelar pedido")
    print("4-Regresar al menú anterior")
    print("--------------------------------------------------")


def seleccionarOpcion():
    """
    Función que controla el flujo del sistema
    """
    try: 
        opcion = 0
        while (opcion != 4):
            imprimirMenu()
            opcion = int(input("Ingrese el número de opción: "))

            if (opcion == 1):
                pedido = Pedido()
                opcionSubmenu = 0
                while opcionSubmenu != 4:
                    imprimirSubMenuPedido()
                    opcionSubmenu =int(input("Ingrese el número de opción: "))
                    if opcionSubmenu == 1:
                        pedido.mostrarListaPedidos()
                    elif opcionSubmenu == 2:
                        pedido.crearPedido()
                    elif opcionSubmenu == 3:
                        pedido.cancelarPedido()
            elif (opcion == 2):
                cliente = Cliente()
                opcionSubmenu = 0
                while opcionSubmenu != 5:
                    imprimirSubMenuCliente()
                    opcionSubmenu =int(input("Ingrese el número de opción: "))
                    if opcionSubmenu == 1:
                        cliente.mostrarListaClientes()
                    elif opcionSubmenu == 2:
                        cliente.agregarCliente()
                    elif opcionSubmenu == 3:
                        cliente.actualizarCliente()
                    elif opcionSubmenu == 4:
                        cliente.eliminarCliente()
            elif (opcion == 3):
                menu = Menu()
                opcionSubmenu = 0
                while opcionSubmenu != 5:
                    imprimirSubMenuMenu()
                    opcionSubmenu =int(input("Ingrese el número de opción: "))
                    if opcionSubmenu == 1:
                        menu.mostrarListaMenu()
                    elif opcionSubmenu == 2:
                        menu.agregarProducto()
                    elif opcionSubmenu == 3:
                        menu.actualizarProducto()
                    elif opcionSubmenu == 4:
                        menu.eliminarProducto()
            elif (opcion == 4):
                print("Fue un placer atenderlo, vuelva pronto")
            else:
                print("Opción no válida, intente nuevamente")
    except Exception as e:
        print("Error: {}".format(e))
    
inicializarBaseDatos()
seleccionarOpcion()