import socket
from pdealer import PokerDealer
from pprotocol import PokerProtocol
import jsonpickle

def sendMessage(player,msgObj):
	sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sSocket.connect((host,player))
	sSocket.send(jsonpickle.encode(msgObj).encode())
	sSocket.close()

host = 'localhost'
myPort = 50000
backlog = 5
size = 1024

nPlayers = 2
nEndRequests = 0

# Receiving socket
rSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rSocket.bind((host,myPort))
rSocket.listen(backlog)
# Dealer object
dealer = PokerDealer(nPlayers, host, myPort)

while 1:
    client, address = rSocket.accept()
    jsonStr = client.recv(size).decode()
    jsonObj = jsonpickle.decode(jsonStr)
    
    if jsonObj.messageCode == "EOGM":
    	endResponse = PokerProtocol("EOGR",myPort)
    	sendMessage(jsonObj.sendingProcessNumber,endResponse)
    	nEndRequests += 1
    	if nEndRequests == nPlayers:
    		print("Game ended")
    		break

    dealer.resolve(jsonObj)
    client.close()

