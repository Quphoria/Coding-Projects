import websocket
import threading
from time import sleep

def on_message(ws, message):
    print()
    print ("###: " + message)
    print()

def on_close(ws):
    print ("### closed ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://echo.websocket.org/", on_message = on_message, on_close = on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    conn_timeout = 5
    while not ws.sock.connected and conn_timeout:
        sleep(1)
        conn_timeout -= 1

    msg_counter = 0
    while ws.sock.connected:
        ws.send('Hello world %d'%msg_counter)
        sleep(1)
        msg_counter += 1
