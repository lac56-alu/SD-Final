# ---------------------- IMPORTS ----------------------
import sys
import socket
import threading
import os, binascii

import mysql.connector

# ---------------------- Variables Globales ----------------------
HEADER = 100
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

def obtenerToken(nombre):
    token = ""
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        executeQuery = cnx.cursor()
        sql = "SELECT * FROM claves WHERE name = '" + nombre + "'"
        executeQuery.execute(sql)

        myresult = executeQuery.fetchone()

        if myresult == None:
            cnx.commit()
            cnx.close()
            token = "no existe"
            return token
        elif myresult[0] == nombre:
            token = myresult[1]
            cnx.commit()
            cnx.close()
            return token
    except Exception as e:
        token = "error"
        return token

def comprobarToken(nombre, token):
    comprobar = False
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        executeQuery = cnx.cursor()
        sql = "SELECT * FROM claves WHERE name = '" + nombre + "' and clave='" + token + "'"
        executeQuery.execute(sql)

        myresult = executeQuery.fetchone()
        print(myresult)

        if myresult == None:
            cnx.commit()
            cnx.close()
        elif myresult[0] == nombre and myresult[1] == token:
            print("TOKEN CORRECTO")
            cnx.commit()
            cnx.close()
            comprobar = True
    except Exception as e:
        comprobar = False

    return comprobar


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


def modificarUsuario(msg):
    print("Entra en MODIFICAR")
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )
        partes = msg.split(',')
        print(partes)

        if comprobarToken(partes[1], partes[3]):

            executeQuery = cnx.cursor()
            sql = "UPDATE usuarios SET password = '" + partes[2] + "' WHERE nombre = '" + partes[1] + "'"
            executeQuery.execute(sql)

            cnx.commit()
            cnx.close()
            return("Se ha modificado el usuario correctamente.")
        else:
            return("Credenciales Incorrectas.")

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

        if comprobarToken(partes[1], partes[3]):
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
            return ("No encontrado")
        elif myresult[1] == partes[1] and myresult[2] == partes[2]:
            cnx.commit()
            cnx.close()
            return obtenerToken(partes[1])
    except Exception as e:
        return ("Error")

def threadsHandler(connHandler, addrHandler):
    comprobarBucle: bool = True
    print(f"Usuario: {addrHandler} conectado. ")

    while comprobarBucle:
        try:
            print("hola 1")
            msg_length = connHandler.recv(HEADER).decode(FORMATO_MSG)
            if msg_length:
                print("hola 2")
                msg_length = int(msg_length)
                msg = connHandler.recv(msg_length).decode(FORMATO_MSG)

                print(msg)
                if msg == "LOGOUT":
                    connHandler.send("La sesión se cerró correctamente.")
                    comprobarBucle = False

                elif "deleteUsuario" in msg:
                    deleteUsuarios(str(msg))
                    connHandler.send("Sesión cerrada y usuario eliminado.")

                elif "crearUsuario" in msg:
                    result = crearUsuario(str(msg))
                    connHandler.send(result.encode(FORMATO_MSG))

                elif "modificar" in msg:
                    print("Entra en el IF")
                    result = modificarUsuario(str(msg))
                    connHandler.send(result.encode(FORMATO_MSG))

                elif "logIn" in msg:
                    result = logIn(str(msg))
                    connHandler.send(result.encode(FORMATO_MSG))
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