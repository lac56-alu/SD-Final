from time import sleep

import mysql

msg = "logIn,luis,prueba2"

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

    myresult = executeQuery.fetchall()
    for row in myresult:
        print(row[0])
        print(row[1])
        print(row[2])

    cnx.commit()
    cnx.close()


except Exception as e:
    print ("Se ha producido un error al hacer logIn...")