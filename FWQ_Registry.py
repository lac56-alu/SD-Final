# ---------------------- IMPORTS ----------------------
import sys
import socket
import threading
import os, binascii

import mysql.connector
import re

# ---------------------- Variables Globales ----------------------
HEADER = 64
FORMATO_MSG = 'utf-8'

puertoEscucha: int = 0
MAX_CONEXIONES: int = 500
CONEXIONES_ACTIVAS: int = 0

mensajeMaxConex = "Se ha superado el número de conexiones permitidas... (max = 500)"
""""""
class User:
    nombre = ""
    password = ""
    token = ""

    def __init__(self, n, p, t):
        self.nombre = n
        self.password = p
        self.token = t


UsuariosCreados: User = []

# ---------------------- Modulos ----------------------
def crearUsuario(msg):
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        partes = msg.split(',')
        executeQuery = cnx.cursor()
        sql = "insert into usuarios (nombre, password) values(%s, %s)"
        val = (partes[1], partes[2])
        executeQuery.execute(sql, val)

        cnx.commit()
        cnx.close()

        token = str(binascii.b2a_hex(os.urandom(20)))

        cnx2 = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )
        executeQuery2 = cnx2.cursor()
        sql2 = "insert into claves (name, clave) values(%s, %s)"
        val2 = (partes[1], token)
        executeQuery2.execute(sql2, val2)

        cnx2.commit()
        cnx2.close()

        usuario = User(partes[1], partes[2], token)
        UsuariosCreados.append(usuario)
        return ("Correcto, token:" + token)

    except Exception as e:
        return ("Se ha producido un error al crear el usuario...")


def modificarUsuario(nombre, password):
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        executeQuery = cnx.cursor()
        sql = "UPDATE usuarios SET password = '" + password + "' WHERE nombre = '" + nombre + "'"
        executeQuery.execute(sql)

        cnx.commit()
        cnx.close()

    except Exception as e:
        return ("Se ha producido un error al modificar el usuario...")

def deleteUsuarios(msg):
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )
        partes = msg.split(',')
        executeQuery = cnx.cursor()
        sql = "DELETE FROM usuarios WHERE password = '" + partes[2] + "' and nombre = '" + partes[1] + "'"
        executeQuery.execute(sql)

        cnx.commit()
        cnx.close()

        cnx2 = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )
        executeQuery2 = cnx2.cursor()
        sql2 = "DELETE FROM claves WHERE name = '" + partes[1] + "'"
        executeQuery2.execute(sql2)

        cnx2.commit()
        cnx2.close()


        return ("Usuario borrado correctamente.")

    except Exception as e:
        return ("No se ha podido borrar el usuario...")

def logIn(msg):
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )
        partes = msg.split(',')
        executeQuery = cnx.cursor()
        sql = "SELECT * FROM usuarios WHERE password = '" + partes[2] + "' and nombre = '" + partes[1] + "'"
        executeQuery.execute(sql)

        myresult = executeQuery.fetchone()

        if myresult == None:
            cnx.commit()
            cnx.close()
            return ("No se ha encontrado ese usuario/password.")
        elif myresult[1] == partes[1] and myresult[2] == partes[2]:
            cnx.commit()
            cnx.close()
            return ("LogIn correcto.")
    except Exception as e:
        return ("Se ha producido un error al hacer logIn...")

def threadsHandler(connHandler, addrHandler):
    comprobarBucle: bool = True
    print(f"Usuario: {addrHandler} conectado. ")

    while comprobarBucle:
        try:
            msg_length = connHandler.recv(HEADER).decode(FORMATO_MSG)
            if msg_length:
                msg_length = int(msg_length)
                msg = connHandler.recv(msg_length).decode(FORMATO_MSG)

                if msg == "LOGOUT":
                    connHandler.send("La sesión se cerró correctamente.")
                    comprobarBucle = False

                elif "deleteUsuario" in msg:
                    deleteUsuarios(str(msg))
                    connHandler.send("Sesión cerrada y usuario eliminado.")
                    comprobarBucle = False

                elif "crearUsuario" in msg:
                    result = crearUsuario(str(msg))
                    connHandler.send(result.encode(FORMATO_MSG))
                    comprobarBucle = False

                elif "modificarUsuario" in msg:
                    result = modificarUsuario(str(msg))
                    connHandler.send(result.encode(FORMATO_MSG))
                    comprobarBucle = False

                elif "logIn" in msg:
                    result = logIn(str(msg))
                    connHandler.send(result.encode(FORMATO_MSG))
                    comprobarBucle = False
        except Exception as e:
            return ("Error en el Handler...")


def start():
    server.listen()
    print(f"Server: {DIRECCION}")
    CONEXIONES_ACTIVAS = threading.active_count() - 1

    while True:
        connServer, addrServer = server.accept()
        CONEXIONES_ACTIVAS = threading.active_count()

        if (CONEXIONES_ACTIVAS > MAX_CONEXIONES):
            print(mensajeMaxConex)
            connServer.send(mensajeMaxConex.encode(FORMATO_MSG))
            connServer.close()
        else:
            print(f"Numero de Conexiones Activas: {CONEXIONES_ACTIVAS}")
            thread = threading.Thread(target=threadsHandler, args=(connServer, addrServer))
            thread.start()




# ---------------------- MAIN ----------------------
puertoEscucha = int(sys.argv[1])
print("################ FWQ_REGISTRY ################")

SERVIDOR = socket.gethostbyname(socket.gethostname())
DIRECCION = (SERVIDOR, puertoEscucha)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(DIRECCION)

start()

#crearUsuario("luis", "hola")
#crearUsuario("pepe", "hola")
#modificarUsuario("luis", "prueba2")
#deleteUsuarios("pepe", "hola")