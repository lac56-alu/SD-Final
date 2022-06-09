# ---------------------------------- IMPORTS -----------------------------
import random
import sys
import stomp
from time import sleep

# ---------------------------------- MAIN -----------------------------
try:
    ipActive = sys.argv[1]
    puertoActive = sys.argv[2]
    idAtraccion = int(sys.argv[3])

    try:

        conn = stomp.Connection([(ipActive, puertoActive)])
        conn.connect(login="", passcode="", wait=True)
    except Exception as e:
        print("Error al conectar con ActiveMQ...")

    while True:
        try:
            personasCola = random.randint(3, 15)
            mensaje = str(idAtraccion) + "," + str(personasCola)
            headerDestination = "/topic/sensor"
            print(mensaje)
            conn.send(headerDestination, mensaje, headers=None)
            sleep(5)
        except Exception as e:
            print("Se produjo un error al enviar los datos...")
            break

except Exception as e:
    print("Error número de parametros incorrecto.")