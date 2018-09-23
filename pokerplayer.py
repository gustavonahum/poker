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
# Sending socket
sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSocket.connect((host,dealerPort))
# Player object
player = PokerPlayer(dealerPort, myPort, host, sSocket)

while 1:
    client, address = rSocket.accept()
    jsonStr = client.recv(size).decode()
    jsonObj = jsonpickle.decode(jsonStr)
    client.close()
    player.resolve(jsonObj)


"""s.send('Hello, world')
data = s.recv(size)
s.close()
print("Received: %s" % data)"""