# ---------------------------------- IMPORTS -----------------------------
import sys
import time
import socket
import threading
import stomp
import mysql.connector

mensajeMaxConex = "Se ha superado el número de conexiones permitidas... (max = 8)"
HEADER = 100
FORMATO_MSG = 'utf-8'
topic = "/topic/sensor"
topic2 = "/topic/waiting"

class Listener(object):
    def __init__(self, conn):
        self.conn = conn
        self.count = 0
        self.start = time.time()
    def on_message(headers, message):
        # ESTE ES EL TOPIC QUE ESTA A LA ESCUCHA
        if(message.headers['destination'] == topic):
            print("Mensaje:", message.body)
            print(calcularTiempo(message.body))
            print("-----------------------------------------------------------------------------")

class Listener2(object):
    def __init__(self, conn):
        self.conn = conn
        self.count = 0
        self.start = time.time()
    def on_message(headers, message):
        # ESTE ES EL TOPIC QUE ESTA A LA ESCUCHA
        if (message.headers['destination'] == topic2):
            print("Mensaje:", message.body)
            print(montarCadenaTiempos())
            print("-----------------------------------------------------------------------------")





def threadsHandler():
    print("ENTRA EN EL HANDLER")


def montarCadenaTiempos():
    print(arrayAtracciones)
    cadena = str(arrayAtracciones[0][1]) + "," + str(arrayAtracciones[1][1]) + "," + str(arrayAtracciones[2][1]) + "," + str(arrayAtracciones[3][1]) + "," \
             + str(arrayAtracciones[4][1]) + "," + str(arrayAtracciones[5][1]) + "," + str(arrayAtracciones[6][1]) + "," + str(arrayAtracciones[7][1])
    print(cadena)
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        executeQuery = cnx.cursor()
        sql = "INSERT INTO tiempostotal(tiempos) VALUES ('" + str(cadena) + "')"
        print(sql)
        executeQuery.execute(sql)

        cnx.commit()
        cnx.close()
        return("Se ha insertado el tiempo correctamente.")

    except Exception as e:
        print(e)
        return ("Se ha producido un error al modificar el tiempo...")

    print(cadena)

def calcularTiempo(msg):
    partes = msg.split(',')
    tiempoEspera = int(partes[1]) * 5

    arrayAtracciones[int(partes[0])][1] = tiempoEspera
    print("Tiempo de espera: ", arrayAtracciones[int(partes[0])][1], " min")

    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        executeQuery = cnx.cursor()
        sql = "UPDATE tiempoespera SET tiempo = " + str(tiempoEspera) + " WHERE atraccion = " + str(partes[0])
        executeQuery.execute(sql)

        cnx.commit()
        cnx.close()
        return("Se ha modificado el tiempo correctamente.")

    except Exception as e:
        return ("Se ha producido un error al modificar el tiempo...")




def main():
    conn = stomp.Connection([(ipActive, int(puertoActive))])
    listener = Listener(conn)
    conn.set_listener('listener', listener)
    conn.connect(login="", passcode="", wait=True)
    conn.subscribe(topic, id=1, ack='auto')

    conn2 = stomp.Connection([(ipActive, int(puertoActive))])
    listener2 = Listener2(conn2)
    conn2.set_listener('listener', listener2)
    conn2.connect(login="", passcode="", wait=True)
    conn2.subscribe(topic2, id=1, ack='auto')

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

atraccion1 = [33, 0]
atraccion2 = [86, 0]
atraccion3 = [137, 0]
atraccion4 = [143, 0]
atraccion5 = [255, 0]
atraccion6 = [262, 0]
atraccion7 = [328, 0]
atraccion8 = [373, 0]

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
puertoServer = sys.argv[3]


try:
    main()

    SERVIDOR = socket.gethostbyname(socket.gethostname())
    DIRECCION = (SERVIDOR, int(puertoServer))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(DIRECCION)
    start()

    activeMqError = False
except Exception as e:
    print("ERROR: No se ha podido ejecutar el servicio...")
    print(e)


