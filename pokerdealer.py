import socket
from pdealer import PokerDealer
import jsonpickle

host = 'localhost'
myPort = 50000
backlog = 5
size = 1024

nPlayers = 5

# Receiving socket
rSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rSocket.bind((host,myPort))
rSocket.listen(backlog)
# Sending socket
sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Dealer object
dealer = PokerDealer(nPlayers, host, myPort, sSocket)

while 1:
    client, address = rSocket.accept()
    jsonStr = client.recv(size).decode()
    jsonObj = jsonpickle.decode(jsonStr)
    dealer.resolve(jsonObj)
    client.close()
"""    rSocket.bind((host,myPort))
    rSocket.listen(backlog)"""
"""if data:
    	data = data.upper()
        client.send(data)
    client.close()"""


"""s.connect((host,port))
s.send('Hello, world')
data = s.recv(size)
s.close()
print("Received: %s" % data)"""





msg = PokerProtocol(112, 11345)
p = jsonpickle.encode(msg)
print(p)
p = jsonpickle.decode(p)
print(p.messageCode)