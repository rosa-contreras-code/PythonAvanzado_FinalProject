"""
Módulo database
Contiene la conexión y creación de la base de datos SQLite.
"""
import sqlite3
import os

class BD:
    def __init__(self, nombreBaseDatos):
        self.nombreBaseDatos = nombreBaseDatos
    
    def crearBaseDatos(self):
        try:
            conn = sqlite3.connect(self.nombreBaseDatos)
        except Exception as e:
            print('Erro al crear la Base de Datos: {}'.format(e))

    def verificarBaseDatosExiste(self):
        if os.path.isfile(self.nombreBaseDatos):
            return True
        else:
            return False
        
    def crearTablaClientes(self):
        conexion = self.abrirConexion()

        conexion.execute('''CREATE TABLE IF NOT EXISTS clientes
                        ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                         clave TEXT NOT NULL,
                         nombre TEXT NOT NULL,
                         direccion TEXT NOT NULL,
                         correo_electronico TEXT NOT NULL,
                         telefono TEXT NOT NULL
                         );''')
        conexion.commit()
        conexion.close()

    def crearTablaMenu(self):
        conexion = self.abrirConexion()
        conexion.execute('''CREATE TABLE IF NOT EXISTS menu
                         (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         clave TEXT NOT NULL,
                         nombre TEXT NOT NULL,
                         precio FLOAT NOT NULL
                         );''')
        conexion.commit()
        conexion.close()
        print("Se creó tabla menu")
        
    def crearTablaPedido(self):
        conexion = self.abrirConexion()
        conexion.execute('''CREATE TABLE IF NOT EXISTS pedido
                         (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         cliente TEXT NOT NULL,
                         producto TEXT NOT NULL,
                         cantidad INTEGER,
                         precio FLOAT NOT NULL
                         );''')
        conexion.commit()
        conexion.close()

    def abrirConexion(self):
        try:
            conexion = sqlite3.connect(self.nombreBaseDatos)
            return conexion
        except Exception as e:
            print('Error al conectar a la Base de Datos: {}'.format(e))
