# ---------------------- IMPORTS ----------------------
import json
import socket
from time import sleep
import sys
import requests

# ---------------------- Variables Globales ----------------------
HEADER = 64
FORMATO_MSG = 'utf-8'

ipRegistry = 0
puertoRegistry = 0
ipBroker = 0
puertoBroker = 0
ipAPI = 0
puertoAPI = 0
serverAPI = "/lac56-alu/SD-REGISTRY/1.0.0/"

currentUser = []

def asignarNombrePass(u,p, currentUser):
    currentUser.append(u)
    currentUser.append(p)

def asignarToken(t,currentUser):
    currentUser.append(t)

def asignarTODO(u,p,t, currentUser):
    currentUser.append(u)
    currentUser.append(p)
    currentUser.append(t)

def borrarCurrent(currentUser):
    currentUser = []

# ---------------------- Modulos SOCKETS ----------------------
def enviarMensaje(msg):
    nuevoMSG = msg.encode(FORMATO_MSG)
    msg_length = len(nuevoMSG)
    send_length = str(msg_length).encode(FORMATO_MSG)
    send_length += b' ' * (HEADER - len(send_length))
    cliente.send(send_length)
    cliente.send(nuevoMSG)


def menuInicio():
    print("Elige método de conexión:")
    print(" 1. Sockets")
    print(" 2. API Rest")
    seleccion = input()


    if int(seleccion) == 1:
        return seleccion
    elif int(seleccion) == 2:
        return seleccion
    else:
        print("Introduce una de las dos opciones")
        menuInicio()

def logInSockets():
    print(" Nombre Usuario: ")
    userName = input()
    print(" Constraseña: ")
    password = input()

    asignarNombrePass(userName, password, currentUser)

    cadena = "logIn," + userName + "," + password
    return cadena


def crearUsuarioSockets():
    comprobarPass = False

    print(" Nombre Usuario: ")
    userName = input()

    while not comprobarPass:
        print(" Constraseña: ")
        password = input()
        print(" Repita la contraseña: ")
        password2 = input()

        if password == password2:
            comprobarPass = True

    cadena = "crearUsuario," + userName + "," + password
    return cadena

def modificarUsuario():
    comprobarPass = False

    print(" Introduzca la contraseña actual: ")
    passOld = input()

    while not comprobarPass:
        print(" Constraseña nueva: ")
        password = input()
        print(" Repita la contraseña nueva: ")
        password2 = input()

        if password == password2:
            comprobarPass = True

    cadena = "modificarUsuario," + currentUser[0] + "," + passOld + "," + password
    return cadena


def menuRegistradoSockets():
    print("Elige una de las opciones:")
    print(" 1. Ir al Mapa")
    print(" 2. Editar Perfil")
    print(" 3. Borrar Perfil")
    print(" 0. Salir")
    seleccion = input()

    if int(seleccion) == 1:
        print("Mostrando Mapa")



    elif int(seleccion) == 2:
        datosModificarUsuario = modificarUsuario()
        enviarMensaje(datosModificarUsuario)
        msg = cliente.recv(HEADER).decode(FORMATO_MSG)
        print(msg)
    elif int(seleccion) == 3:
        cadenaBorrar = "deleteUsuario," + currentUser[0] + "," + currentUser[1]
        enviarMensaje(cadenaBorrar)
        msg = cliente.recv(HEADER).decode(FORMATO_MSG)
        print(msg)
    elif int(seleccion) == 0:
        print(" Saliendo de la aplicacion...")
    else:
        print("Introduce una de las dos opciones")
        menuRegistradoSockets()


def menuSockets():
    print("1. LogIn")
    print("2. Crear Usuario")
    print("0. SALIR")
    seleccion = input()

    if int(seleccion) == 1:
        datosLogIn = logInSockets()
        enviarMensaje(datosLogIn)
        msg = cliente.recv(HEADER).decode(FORMATO_MSG)

        if msg == "No encontrado":
            print("Credenciales Incorrectas")
            menuSockets()
        elif msg == "Error":
            print("Error al realizar la operacion...")
        else:
            print("Acceso Correcto")
            asignarToken(msg, currentUser)
            menuRegistradoSockets()
    elif int(seleccion) == 2:
        datosCrearUsuario = crearUsuarioSockets()
        enviarMensaje(datosCrearUsuario)
        msg = cliente.recv(HEADER).decode(FORMATO_MSG)
        print(msg)
        menuSockets()
    elif int(seleccion) == 0:
        print("  Saliendo de la aplicacion...")
        return
    else:
        print("Introduce una opcion valida")
        menuSockets()

# ---------------------- Modulos API ----------------------

def modificarUsuarioAPI():
    comprobarPass = False

    print(" Introduzca la contraseña actual: ")
    passOld = input()

    while not comprobarPass:
        print(" Constraseña nueva: ")
        password = input()
        print(" Repita la contraseña nueva: ")
        password2 = input()

        if password == password2:
            comprobarPass = True

    try:
        endPoint = "http://" + str(ipAPI) + ":" + str(puertoAPI) + serverAPI + "modificarUsuario/" + currentUser[2]
        body = {"name": currentUser[0], "oldPassword": passOld, "newPassword": password}
        jsonBody = json.dumps(body)

        response = requests.put(
            endPoint,
            jsonBody,
            headers={'Content-Type': 'application/json'}
        )
        print(response.status_code)
        jsonRespuesta = json.loads(response.text)

        if response.status_code == 201:
            msg = jsonRespuesta['cadena']
            print("Usuario modificado correctamente.")
        else:
            msg = "Valores no validos."
    except Exception:
        msg = "No se ha podido conectar con el endpoint."

    return msg

def borrarUsuarioAPI():
    msg = ""
    print("¿Seguro que quiere borrar su usuario? y/n")
    seleccion = input()

    if seleccion == "y":
        print(" Introduzca la contraseña actual: ")
        password = input()

        if password == currentUser[1]:
            print("las contraseñas coinciden")
            endPoint = "http://" + str(ipAPI) + ":" + str(puertoAPI) + serverAPI \
                       + "borrarUsuario/" + currentUser[2] + "/" + currentUser[0]
            response = requests.delete(
                endPoint,
                headers={'Content-Type': 'application/json'}
            )

            jsonRespuesta = json.loads(response.text)

            if response.status_code == 201:
                print(jsonRespuesta['cadena'])
                msg = jsonRespuesta['cadena']
            else:
                print(jsonRespuesta['cadena'])
                msg = "No se ha podido borrar el usuario."
        else:
            print("Credendiales incorrectas.")


    elif seleccion == "n":
        print("Operación cancelada.")

    return msg



def menuRegistradoAPI():
    print("Elige una de las opciones:")
    print(" 1. Ir al Mapa")
    print(" 2. Editar Perfil")
    print(" 3. Borrar Perfil")
    print(" 0. Salir")
    seleccion = input()

    if int(seleccion) == 1:
        print("Mostrando Mapa")

    elif int(seleccion) == 2:
        modificarUsuarioAPI()
        menuRegistradoAPI()

    elif int(seleccion) == 3:
        resp = borrarUsuarioAPI()

        if resp == "No se ha podido borrar el usuario." or resp == "":
            menuRegistradoAPI()
        else:
            borrarCurrent(currentUser)
            menuAPI()

    elif int(seleccion) == 0:
        print("Saliendo de la aplicacion...")


def crearUsuarioAPI():
    msg = ""

    print(" Nombre Usuario: ")
    userName = input()
    print(" Constraseña: ")
    password = input()

    try:
        endPoint = "http://" + str(ipAPI) + ":" + str(puertoAPI) + serverAPI + "nuevoUsuario"
        body = {"name": userName, "password": password}
        jsonBody = json.dumps(body)

        response = requests.post(
            endPoint,
            jsonBody,
            headers={'Content-Type': 'application/json'}
        )

        jsonRespuesta = json.loads(response.text)

        if response.status_code == 201:
            print("Usuario creado correctamente.")
            msg = jsonRespuesta['cadena']
            print("Su token es: " + msg)
        else:
            msg = "Valores no validos."
    except Exception:
        msg = "No se ha podido conectar con el endpoint."

    return msg



def logInAPI():
    msg = ""

    print(" Nombre Usuario: ")
    userName = input()
    print(" Constraseña: ")
    password = input()

    try:
        endPoint = "http://" + str(ipAPI) + ":" + str(puertoAPI) + serverAPI + "login"
        body = {"name": userName, "password": password}
        jsonBody = json.dumps(body)

        response = requests.post(
            endPoint,
            jsonBody,
            headers={'Content-Type': 'application/json'}
        )

        jsonRespuesta = json.loads(response.text)

        if response.status_code == 201:
            token = jsonRespuesta['cadena']
            try:
                asignarTODO(userName, password, token, currentUser)
            except Exception as e:
                print(e)

            """currentUser.append(userName)
            currentUser.append(password)
            currentUser.append(token)"""
            msg = "Usuario logeado correctamente."
        else:
            msg = "Credenciales Incorrectas"
    except Exception:
        msg = "No se ha podido conectar con el endpoint."

    return msg

def menuAPI():
    print("1. LogIn")
    print("2. Crear Usuario")
    print("0. SALIR")
    seleccion = input()

    if int(seleccion) == 1:
        respuestaLogin = logInAPI()
        print(respuestaLogin)

        if respuestaLogin == "Usuario logeado correctamente.":
            menuRegistradoAPI()
        elif respuestaLogin == "No se ha podido conectar con el endpoint.":
            menuInicio()
        elif respuestaLogin == "Credenciales Incorrectas":
            menuAPI()

    elif int(seleccion) == 2:
        respuestaCrear = crearUsuarioAPI()

        if respuestaCrear == "Valores no validos." or respuestaCrear == "No se ha podido conectar con el endpoint.":
            menuAPI()
        else:
            currentUser.append(respuestaCrear)
    elif int(seleccion) == 0:
        print("  Saliendo de la aplicacion...")
        return
    else:
        print("Introduce una opcion valida")
        menuAPI()



# ---------------------- MAIN ----------------------
ipRegistry = sys.argv[1]
puertoRegistry = sys.argv[2]
ipBroker = sys.argv[3]
puertoBroker = sys.argv[4]
ipAPI = sys.argv[5]
puertoAPI = sys.argv[6]


eleccion = menuInicio()

if int(eleccion) == 1:

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    parseToInt = int(puertoRegistry)
    direccionRegistro = (ipRegistry, parseToInt)
    comprobarBucle = False

    while not comprobarBucle:
        try:
            currentUser = []
            cliente.connect(direccionRegistro)
            print("Conexion completada.")
            print(" ################### SOCKETS ###################")
            comprobarBucle = True
            menuSockets()
        except Exception:
            print("No se puede establecer la conexion...")
            print(" Intentandolo de nuevo...")
            sleep(5)
else:
    currentUser = []
    menuAPI()
