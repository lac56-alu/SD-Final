import sys
import time
import stomp
import mysql.connector

# ---------------------- Variables Globales --- -------------------
mapaGlobal = ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#',
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
topic2 = "/topic/waiting"
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
            if "mostrarMapa" in message.body:
                partes = message.body.split(',')
                mapaToString(mapaGlobal, partes[1])


            elif "entrar" in message.body:
                entrarParque(message.body)

                partes = message.body.split(',')
                mapaToString(mapaGlobal, partes[1])

            elif "salir" in message.body:
                salirParque(message.body)

            elif "mover" in message.body:
                movimientoUsuario(message.body)
                partes = message.body.split(',')
                mapaToString(mapaGlobal, partes[1])

            print("Mensaje:", message.body)
            print("-----------------------------------------------------------------------------")

def enviarEngine(msg, top):
    try:
        print("Enviar: ", msg)
        conn = stomp.Connection([(ipActiveMQ, puertoActiveMQ)])
        conn.connect(login="", passcode="", wait=True)
        conn.send(top, msg, headers=None)
    except Exception as e:
        print("Error Enviar Mensaje:", e)



def mapaToString(mapa, nombre):
    posi = 0
    numAtraccion = 0

    mapaString = ""
    salto = 19
    print(len(mapa))
    tiempos = consultarTiempo()
    partes = tiempos.split(',')
    for i in range(0, len(mapa)):
        if comprobarPosicion(i, nombre) == True:
            mapaString += "X "
            posi += 1
        else:
            if mapa[i] == 'X':
                mapaString += partes[numAtraccion] + " "
                numAtraccion += 1
            else:
                mapaString += mapa[i] + " "

            if posi == salto:
                mapaString += "\n"
                salto = 20
                posi = 0
            posi += 1
    print(mapaString)
    if mapaString != "":
        try:
            cnx = mysql.connector.connect(
                user='luis',
                password='root',
                host='127.0.0.1',
                database='sd'
            )

            executeQuery = cnx.cursor()
            sql = "INSERT INTO mapaparque(mapa, usuario) values ('" + mapaString + "', '"+ nombre+ "')"
            executeQuery.execute(sql)

            cnx.commit()
            cnx.close()
            top = "/topic/" + nombre
            enviarEngine(mapaString, top)
        except Exception as e:
            return ("Se ha producido un error al guardar el mapa en la BD...")

    return mapaString

def movimientoUsuario(msg):
    partes = msg.split(',')
    nombre = partes[1]
    mov = partes[2]

    desplazamiento = 0
    usuarioPosi = 0

    if mov == 'N':
        desplazamiento = -20
    elif mov == 'NE':
        desplazamiento = -19
    elif mov == 'E':
        desplazamiento = 1
    elif mov == 'SE':
        desplazamiento = 21
    elif mov == 'S':
        desplazamiento = 20
    elif mov == 'SO':
        desplazamiento = 19
    elif mov == 'O':
        desplazamiento = -1
    elif mov == 'NO':
        desplazamiento = -21

    for i in range(0, len(usuariosParque)):
        if usuariosParque[i].nombre == nombre:
            usuarioPosi = i
            comprobar = True
            break

    newPosi = usuariosParque[usuarioPosi].posicion + desplazamiento
    print("Posicion Actual: ", str(usuariosParque[usuarioPosi].posicion))
    print("Desplazamiento: ", str(desplazamiento))
    print("Posicion Final: ", newPosi)

    if comprobar == True and newPosi >= 0 and newPosi <= 399:
        usuariosParque[usuarioPosi].posicion = newPosi
    else:
        print("No se puede realizar el desplazamiento")



def consultarTiempo():
    msg = "yes"
    conn = stomp.Connection([(ipActiveMQ, puertoActiveMQ)])
    conn.connect(login="", passcode="", wait=True)
    conn.send(topic2, msg, headers=None)

    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        executeQuery = cnx.cursor()
        sql = "select tiempos from tiempostotal where id = (select max(id) from tiempostotal)"
        executeQuery.execute(sql)

        myresult = executeQuery.fetchone()

        if myresult == None:
            cnx.commit()
            cnx.close()
            return ("No encontrado")
        else:
            cnx.commit()
            cnx.close()
            resp = str(myresult[0])
            return resp

    except Exception as e:
        print(e)
        return ("Se ha producido un error al consultar el tiempo...")


def entrarParque(msg):
    partes = msg.split(',')
    usuario = User(partes[1], 0)
    usuariosParque.append(usuario)

    top = "/topic/" + str(partes[1])
    print(top)
    enviarEngine("Entrada correcta, difrute del parque.", top)

def salirParque(msg):
    partes = msg.split(',')
    for i in range(0, len(usuariosParque)):
        if usuariosParque[i].nombre == partes[1]:
            usuariosParque.pop(i)
            break
    top = "/topic/" + str(partes[1])
    print(top)
    enviarEngine("Salida correcta, esperamos que vuelva pronto.", top)

def comprobarPosicion(posi, nombre):
    comprobar = False

    for i in range(0, len(usuariosParque)):
        if usuariosParque[i].posicion == posi and usuariosParque[i].nombre == nombre:
            comprobar = True
            break

    return comprobar

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