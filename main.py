import stomp

topicEngine = "/topic/engine"
ipActiveMQ = '127.0.0.1'
puertoActiveMQ = 61613

def enviarEngine(msg):
    try:
        print(msg)
        conn = stomp.Connection([(ipActiveMQ, puertoActiveMQ)])
        conn.connect(login="", passcode="", wait=True)
        conn.send(topicEngine, msg, headers=None)
    except Exception as e:
        print("Error Enviar Mensaje:", e)


msg = "entrar,raq"
enviarEngine(msg)