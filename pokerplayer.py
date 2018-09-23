import socket
import sys
from phand import PokerHand
from pprotocol import PokerProtocol
import jsonpickle

host = 'localhost'
myPort = int(sys.argv[1])
dealerPort = 50000
size = 1024
backlog = 5

# Sending socket
sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSocket.connect((host,dealerPort))

# Play request
playReq = PokerProtocol("PLRQ", myPort)
sSocket.send(jsonpickle.encode(playReq).encode())


"""s.send('Hello, world')
data = s.recv(size)
s.close()
print("Received: %s" % data)"""