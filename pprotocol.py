class PokerProtocol:

	def __init__(self, msgCode, pNumber, cValue="", cNipe="", wProcess="", qMsg=1):
		self.messageCode = msgCode
		self.sendingProcessNumber = pNumber
		self.cardValue = cValue
		self.cardNipe = cNipe
		self.winningProcessNumber = wProcess
		self.quantityOfMessages = qMsg