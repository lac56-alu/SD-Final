# ---------------------- IMPORTS ----------------------
import socket
from time import sleep
import sys

# ---------------------- Variables Globales ----------------------
HEADER = 64
FORMATO_MSG = 'utf-8'

ipRegistry = 0
puertoRegistry = 0
ipBroker = 0
puertoBroker = 0
ipAPI = 0
puertoAPI = 0

currentUser = []

# ---------------------- Modulos ----------------------
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
        print("API REST, proximamente.....")
        return seleccion
    else:
        print("Introduce una de las dos opciones")
        menuInicio()

def logInSockets():
    print(" Nombre Usuario: ")
    userName = input()
    print(" Constraseña: ")
    password = input()

    currentUser.append(userName)
    currentUser.append(password)

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

        if msg == "LogIn correcto.":
            print(msg)
            menuRegistradoSockets()
        else:
            print(msg)
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
    print("API REST, proximamente.....")
