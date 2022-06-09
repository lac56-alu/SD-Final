# ---------------------------------- IMPORTS -----------------------------
import sys
import time
import socket
import threading

import mysql.connector
import stomp

mensajeMaxConex = "Se ha superado el número de conexiones permitidas... (max = 8)"
HEADER = 100
FORMATO_MSG = 'utf-8'
topic = "/topic/sensor"

class Listener(object):
    def __init__(self, conn):
        self.conn = conn
        self.count = 0
        self.start = time.time()
    def on_message(headers, message):
        # ESTE ES EL TOPIC QUE ESTA A LA ESCUCHA
        if(message.headers['destination'] == topic):
            print("entra en lo del topic")
            print(message.body)
            updateTiempos(message.body)


def threadsHandler():
    print("ENTRA EN EL HANDLER")

def updateTiempos(msg):
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )
        partes = msg.split(',')
        print(partes)

        executeQuery = cnx.cursor()
        sql = "UPDATE tiemposespera SET tiempo = " + partes[1] + " WHERE atraccion = " + partes[0]
        executeQuery.execute(sql)

        cnx.commit()
        cnx.close()
        return ("Se ha modificado el tiempo de espera correctamente.")

    except Exception as e:
        print(e)
        return ("Se ha producido un error al modificar el usuario...")


def main():
    conn = stomp.Connection([(ipActive, int(puertoActive))])
    listener = Listener(conn)
    conn.set_listener('listener', listener)
    conn.connect(login="", passcode="", wait=True)
    conn.subscribe(topic, id=1, ack='auto')

def start():
    server.listen()
    print(f"Server: {DIRECCION}")

    while True:
        connServer, addrServer = server.accept()
        CONEXIONES_ACTIVAS = threading.active_count()

        if (CONEXIONES_ACTIVAS > 8):
            print(mensajeMaxConex)
            connServer.send(mensajeMaxConex.encode(FORMATO_MSG))
            connServer.close()
        else:
            print(f"Numero de Conexiones Activas: {CONEXIONES_ACTIVAS}")
            thread = threading.Thread(target=threadsHandler, args=(connServer, addrServer))
            thread.start()

atraccion1 = [33, 3]
atraccion2 = [86, 4]
atraccion3 = [137, 2]
atraccion4 = [143, 5]
atraccion5 = [255, 3]
atraccion6 = [262, 4]
atraccion7 = [328, 3]
atraccion8 = [373, 4]

arrayAtracciones = []
arrayAtracciones.append(atraccion1)
arrayAtracciones.append(atraccion2)
arrayAtracciones.append(atraccion3)
arrayAtracciones.append(atraccion4)
arrayAtracciones.append(atraccion5)
arrayAtracciones.append(atraccion6)
arrayAtracciones.append(atraccion7)
arrayAtracciones.append(atraccion8)


# ---------------------------------- MAIN -----------------------------
ipActive = sys.argv[1]
puertoActive = sys.argv[2]
ipServer = sys.argv[3]


try:
    main()

    SERVIDOR = socket.gethostbyname(socket.gethostname())
    DIRECCION = (SERVIDOR, int(ipServer))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(DIRECCION)
    start()

    activeMqError = False
except Exception as e:
    print("ERROR: No se ha podido ejecutar el servicio...")
    print(e)


