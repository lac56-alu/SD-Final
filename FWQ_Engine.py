import sys
import time
import stomp

# ---------------------- Variables Globales --- -------------------
mapa = ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','X','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','X','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','X','#','#',
        '#','#','#','X','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
         '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','X','#','#','#','#',
        '#','#','X','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','X','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','X','#','#','#','#','#','#',
        '#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']

host = '127.0.0.1'
port = 61613
topic = "/topic/engine"
ipActiveMQ = '127.0.0.1'
puertoActiveMQ = 61613
usuariosParque = []



# ---------------------- Modulos ----------------------
class User:
    nombre = ""
    posicion = ""

    def __init__(self, n, p):
        self.nombre = n
        self.posicion = p


class Listener(object):
    def __init__(self, conn):
        self.conn = conn
        self.count = 0
        self.start = time.time()
    def on_message(headers, message):
        # ESTE ES EL TOPIC QUE ESTA A LA ESCUCHA
        if(message.headers['destination'] == topic):
            if message.body == "mostrarMapa":
                mapa = montarMapa()
            elif "entrar" in message.body:
                entrarParque(message.body)
            elif "salir" in message.body:
                salirParque(message.body)

            print("Mensaje:", message.body)
            print("-----------------------------------------------------------------------------")


def entrarParque(msg):
    partes = msg.split(',')
    usuario = User(partes[1], 0)
    usuariosParque.append(usuario)

def salirParque(msg):
    partes = msg.split(',')
    for i in range(0, len(usuariosParque)):
        if usuariosParque[i].nombre == partes[1]:
            usuariosParque.pop(i)
            break

def montarMapa():
    print("------- MOSTRAR MAPA -------")
    mapa = ""

    return mapa

def activeMQ():
    conn = stomp.Connection([(ipActiveMQ, puertoActiveMQ)])
    listener = Listener(conn)
    conn.set_listener('listener', listener)
    conn.connect(login="", passcode="", wait=True)
    conn.subscribe(topic, id=1, ack='auto')


# ---------------------- MAIN ----------------------
ipBroker = sys.argv[1]
puertoBroker = int(sys.argv[2])
maxVisit = int(sys.argv[3])
ipWatingTimeServer = sys.argv[4]
puertoWatingTimeServer = int(sys.argv[5])

try:
    activeMQ()
    while True:
        cad = ""
except Exception as e:
    print("ActiveMQ error:", e)