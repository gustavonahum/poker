import socket
import sys
from pplayer import PokerPlayer
import jsonpickle

host = 'localhost'
myPort = int(sys.argv[1])
dealerPort = 50000
size = 1024
backlog = 5

# Receiving socket
rSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rSocket.bind((host,myPort))
rSocket.listen(backlog)

# Player object
player = PokerPlayer(dealerPort, myPort, host)

while 1:
    client, address = rSocket.accept()
    jsonStr = client.recv(size).decode()
    jsonObj = jsonpickle.decode(jsonStr)

    if jsonObj.messageCode == "EOGR":
    	print("Exited the game")
    	break
    elif jsonObj.messageCode == "PLRR":
    	print("Didn't enter the game")
    	break

    player.resolve(jsonObj)
    client.close()
