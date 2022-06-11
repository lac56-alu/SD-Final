# ---------------------------------- IMPORTS -----------------------------
import random
import sys
import stomp
from time import sleep
import mysql.connector

def obtenerPersonas(id):
    try:
        cnx = mysql.connector.connect(
            user='luis',
            password='root',
            host='127.0.0.1',
            database='sd'
        )

        executeQuery = cnx.cursor()
        sql = "SELECT * from cola WHERE atraccion = " + str(id)
        executeQuery.execute(sql)

        myresult = executeQuery.fetchone()

        if myresult == None:
            cnx.commit()
            cnx.close()
            msg = "No existe esa atraccion"
            return msg
        elif myresult[0] == id:
            msg = myresult[1]
            cnx.commit()
            cnx.close()
            return msg

    except Exception as e:
        print(e)
        return ("Se ha producido un error al obtener personas...")


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
            personasCola = obtenerPersonas(idAtraccion)
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