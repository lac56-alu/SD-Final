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
posicionesAtracciones = [33, 86, 137, 143, 255, 262, 328, 373]
saltoPosiciones = [19, 39, 59, 79, 99, 119, 139, 159, 179, 199, 219, 239, 259, 279, 299, 319, 339, 359, 379, 399]

posicionesCuadrante0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42, 43, 44, 45, 46,
                       47, 48, 49, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 100,
                       101, 102, 103, 104, 105, 106, 107, 108, 109, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
                       140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 160, 161, 162, 163, 164, 165, 166, 167, 168,
                       169, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189]

posicionesCuadrante1 = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 50, 51, 52, 53,
                       54, 55, 56, 57, 58, 59, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 90, 91, 92, 93, 94, 95, 96, 97,
                       98, 99, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 130, 131, 132, 133, 134, 135, 136, 137,
                       138, 139, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 170, 171, 172, 173, 174, 175, 176,
                       177, 178, 179, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199]

posicionesCuadrante2 = [200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 220, 221, 222, 223, 224, 225, 226, 227, 228,
                       229, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 260, 261, 262, 263, 264, 265, 266, 267,
                       268, 269, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 300, 301, 302, 303, 304, 305, 306,
                       307, 308, 309, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 340, 341, 342, 343, 344, 345,
                       346, 347, 348, 349, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 380, 381, 382, 383, 384,
                       385, 386, 387, 388, 389]

posicionesCuadrante3 = [210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 230, 231, 232, 233, 234, 235, 236, 237, 238,
                       239, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 270, 271, 272, 273, 274, 275, 276, 277,
                       278, 279, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 310, 311, 312, 313, 314, 315, 316,
                       317, 318, 319, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 350, 351, 352, 353, 354, 355,
                       356, 357, 358, 359, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 390, 391, 392, 393, 394,
                       395, 396, 397, 398, 399]

cuadratesActivos = ["si", "si", "si", "si"]

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
    numAtraccion = 0

    mapaString = ""
    salto = 20
    print(len(mapa))
    tiempos = consultarTiempo()
    partes = tiempos.split(',')

    consultarCuadrante("0")
    consultarCuadrante("1")
    consultarCuadrante("2")
    consultarCuadrante("3")

    print(cuadratesActivos)

    for i in range(0, len(mapa)):
        if mapa[i] == 'X':
            if i in posicionesCuadrante0:
                if cuadratesActivos[0] == 'no':
                    mapaString += "- "
                else:
                    mapaString += partes[numAtraccion] + " "
                    numAtraccion += 1
            elif i in posicionesCuadrante1:
                if cuadratesActivos[1] == 'no':
                    mapaString += "- "
                else:
                    mapaString += partes[numAtraccion] + " "
                    numAtraccion += 1
            elif i in posicionesCuadrante2:
                if cuadratesActivos[2] == 'no':
                    mapaString += "- "
                else:
                    mapaString += partes[numAtraccion] + " "
                    numAtraccion += 1
            elif i in posicionesCuadrante3:
                if cuadratesActivos[3] == 'no':
                    mapaString += "- "
                else:
                    mapaString += partes[numAtraccion] + " "
                    numAtraccion += 1
        else:
            if comprobarPosicion(i, nombre) == True:
                mapaString += "T "
            elif comprobarUsuarioPosicion(i) == True:
                mapaString += "X "
            elif i in posicionesCuadrante0:
                if cuadratesActivos[0] == 'no':
                    mapaString += "- "
                else:
                    mapaString += mapaGlobal[i] + " "
            elif i in posicionesCuadrante1:
                if cuadratesActivos[1] == 'no':
                    mapaString += "- "
                else:
                    mapaString += mapaGlobal[i] + " "
            elif i in posicionesCuadrante2:
                if cuadratesActivos[2] == 'no':
                    mapaString += "- "
                else:
                    mapaString += mapaGlobal[i] + " "
            elif i in posicionesCuadrante3:
                if cuadratesActivos[3] == 'no':
                    mapaString += "- "
                else:
                    mapaString += mapaGlobal[i] + " "

        if i in saltoPosiciones:
            mapaString += "\n"

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

def comprobarUsuarioPosicion(posi):
    comprobar = False

    for i in range(0, len(usuariosParque)):
        if usuariosParque[i].posicion == posi:
            comprobar = True
            break

    return comprobar

def addCola(idAtr):
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        executeQuery = cnx.cursor()
        sql = "UPDATE cola SET numpersonas = numpersonas + 1 where atraccion =" + str(idAtr)
        print(sql)
        executeQuery.execute(sql)

        cnx.commit()
        cnx.close()
        return("Se encuentra esperando en la cola de la Atraccion: " + str(idAtr))

    except Exception as e:
        print(e)
        return ("Se ha producido un error al ponerse en la cola...")


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

    consultarCuadrante("0")
    consultarCuadrante("1")
    consultarCuadrante("2")
    consultarCuadrante("3")

    newPosi = usuariosParque[usuarioPosi].posicion + desplazamiento
    print("Posicion Actual: ", str(usuariosParque[usuarioPosi].posicion))
    print("Desplazamiento: ", str(desplazamiento))
    print("Posicion Final: ", newPosi)

    if newPosi in posicionesCuadrante0:
        if cuadratesActivos[0] == 'no':
            print("Zona NO activa")
            top = "/topic/" + nombre
            enviarEngine("Zona NO DISPONIBLE", top)
            return
    elif newPosi in posicionesCuadrante1:
        if cuadratesActivos[1] == 'no':
            print("Zona NO activa")
            top = "/topic/" + nombre
            enviarEngine("Zona NO DISPONIBLE", top)
        return
    elif newPosi in posicionesCuadrante2:
        if cuadratesActivos[2] == 'no':
            print("Zona NO activa")
            top = "/topic/" + nombre
            enviarEngine("Zona NO DISPONIBLE", top)
            return
    elif newPosi in posicionesCuadrante3:
        if cuadratesActivos[3] == 'no':
            print("Zona NO activa")
            top = "/topic/" + nombre
            enviarEngine("Zona NO DISPONIBLE", top)
            return

    if comprobar == True and newPosi >= 0 and newPosi <= 399:
        if newPosi in posicionesAtracciones:
            idAtraccion = posicionesAtracciones.index(newPosi)
            addCola(idAtraccion)
        usuariosParque[usuarioPosi].posicion = newPosi
    else:
        print("No se puede realizar el desplazamiento")

def consultarCuadrante(idCuadrante):
    comprobar = True
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        executeQuery = cnx.cursor()

        sql = "select activo from cuadrantes where id = " + str(idCuadrante)
        executeQuery.execute(sql)

        myresult = executeQuery.fetchone()
        if myresult == None:
            cnx.commit()
            cnx.close()
            comprobar = False
        else:
            cuadratesActivos[int(idCuadrante)] = myresult[0]
            cnx.commit()
            cnx.close()
            comprobar = False

        return comprobar

    except Exception as e:
        print("Se ha producido un error al consultar el cuadrante...")
        return comprobar

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