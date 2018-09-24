from phand import PokerHand
from collections import defaultdict
import copy

class CompareHands():
	# Hands of players
	hands = []
	# Category order
	categoryOrder = []
	# Possible values
	values = ["7","8","9","10","J","Q","K","A"]

	def __init__(self, hands):
		self.initializeHands(hands)
		self.initializeCategoryOrder()

	def resolveBestHand(self):
		handsCopy = copy.deepcopy(self.hands)
		eliminated = True
		while eliminated:
			eliminated = False
			for hand1 in handsCopy:
				if self.betterThanSomeHand(hand1, handsCopy):
					eliminated = True
					break
		return handsCopy

	def betterThanSomeHand(self, hand1, handsCopy):
		for hand2 in handsCopy:
			if self.betterThan(hand1, hand2):
				handsCopy.remove(hand2)
				return True
		return False



	# Evaluates if hand1 is better than hand2
	def betterThan(self, hand1, hand2):
		pHand1 = PokerHand(hand1)
		pHand2 = PokerHand(hand2)
		category1 = pHand1.getCategory()
		category2 = pHand2.getCategory()
		if self.betterCategoryThan(category1,category2):
			return True
		return False
		#else:
		#	return self.betterTieBreakerThan(hand1,hand2)


	def betterCategoryThan(self, category1, category2):
		index1 = self.categoryOrder.index(category1)
		index2 = self.categoryOrder.index(category2)
		return index1 > index2

	def betterTieBreakerThan(self, hand1, hand2):
		pHand1 = PokerHand(hand1)
		if pHand1.isRoyalFlush():
			return False
		if pHand1.isStraightFlush():
			return self.betterTieBreakerInStraightFlush(hand1, hand2)
		if pHand1.isFourOfAKind():
			return self.betterTieBreakerInFourOfAKind(hand1, hand2)
		if pHand1.isFullHouse():
			return self.betterTieBreakerInFullHouse(hand1, hand2)
		if pHand1.isFlush():
			return self.betterTieBreakerInFlush(hand1, hand2)
		if pHand1.isStraight():
			return self.betterTieBreakerInStraight(hand1, hand2)
		if pHand1.isThreeOfAKind():
			return self.betterTieBreakerInThreeOfAKind(hand1, hand2)
		if pHand1.isTwoPair():
			return self.betterTieBreakerInTwoPair(hand1, hand2)
		if pHand1.isOnePair():
			return self.betterTieBreakerInOnePair(hand1, hand2)
		return self.betterTieBreakerInHighCard(hand1, hand2)

	def betterTieBreakerInStraightFlush(self, hand1, hand2):
		return self.highestValueGreaterThan(hand1, hand2)

	def betterTieBreakerInFourOfAKind(self, hand1, hand2):
		f1 = self.valueOfRepeatedValues(hand1,4)
		f2 = self.valueOfRepeatedValues(hand2,4)
		return f1 > f2

	def betterTieBreakerInFullHouse(self, hand1, hand2):
		t1 = self.valueOfRepeatedValues(hand1,3)
		t2 = self.valueOfRepeatedValues(hand2,3)
		return t1 > t2

	def betterTieBreakerInFlush(self, hand1, hand2):
		return self.greatestValues(hand1, hand2, 5)

	def betterTieBreakerInStraight(self, hand1, hand2):
		return self.highestValueGreaterThan(hand1, hand2)

	def betterTieBreakerInThreeOfAKind(self, hand1, hand2):
		t1 = self.valueOfRepeatedValues(hand1,3)
		t2 = self.valueOfRepeatedValues(hand2,3)
		return t1 > t2

	def betterTieBreakerInTwoPair(self, hand1, hand2):
		h1Copy = copy.deepcopy(hand1)
		h2Copy = copy.deepcopy(hand2)
		p1 = self.values.index(self.valueOfHighestPair(h1Copy))
		p2 = self.values.index(self.valueOfHighestPair(h2Copy))
		if p1 > p2:
			return True
		for i in range(2):
			self.removePair(h1Copy, p1)
			self.removePair(h2Copy, p2)
		p1 = self.values.index(self.valueOfHighestPair(h1Copy))
		p2 = self.values.index(self.valueOfHighestPair(h2Copy))
		if p1 > p2:
			return True
		for i in range(2):
			self.removePair(h1Copy, p1)
			self.removePair(h2Copy, p2)
		(p1, n1) = h1Copy[0]
		(p2, n2) = h2Copy[0]
		return p1 > p2

	def betterTieBreakerInOnePair(self, hand1, hand2):
		h1Copy = copy.deepcopy(hand1)
		h2Copy = copy.deepcopy(hand2)
		p1 = self.values.index(self.valueOfHighestPair(h1Copy))
		p2 = self.values.index(self.valueOfHighestPair(h2Copy))
		if p1 > p2:
			return True
		for i in range(2):
			self.removePair(h1Copy, p1)
			self.removePair(h2Copy, p2)
		return self.greatestValues(h1Copy, h2Copy, 3)

	def betterTieBreakerInHighCard(self, hand1, hand2):
		return self.greatestValues(hand1, hand2, 5)


	"""Auxiliary methods"""
	def initializeHands(self, hands):
		for hand in hands:
			self.hands.append(hands[hand])

	def initializeCategoryOrder(self):
		self.categoryOrder.append("High Card")
		self.categoryOrder.append("One Pair")
		self.categoryOrder.append("Two Pair")
		self.categoryOrder.append("Three of a Kind")
		self.categoryOrder.append("Straight")
		self.categoryOrder.append("Flush")
		self.categoryOrder.append("Full House")
		self.categoryOrder.append("Four of a Kind")
		self.categoryOrder.append("Straight Flush")
		self.categoryOrder.append("Three of a Kind")
		self.categoryOrder.append("Royal Flush")

	def valueGreaterThan(self, value1, value2):
		index1 = self.values.index(value1)
		index2 = self.values.index(value2)
		return index1 > index2

	# Returns the value that is repeated "num" times in "hand"
	def valueOfRepeatedValues(self, hand, num):
		pHand = PokerHand(hand)
		for (value, nipe) in hand:
			if pHand.valueRepeats(value, num):
				return value


	def highestValueGreaterThan(self, hand1, hand2):
		pHand1 = PokerHand(hand1)
		pHand2 = PokerHand(hand2)
		highestValue1 = pHand1.highestValue()
		highestValue2 = pHand2.highestValue()
		return self.valueGreaterThan(highestValue1, highestValue2)


	def greatestValues(self, hand1, hand2, num):
		for i in range(num):
			g1 = self.values.index(self.greatestValue(hand1, i))
			g2 = self.values.index(self.greatestValue(hand2, i))
			if g1 > g2:
				return True
		return False

	def greatestValue(self, hand, num):
		handCopy = copy.deepcopy(hand)
		gValue = self.absoluteGreatestValue(handCopy)
		for i in range(num):
			self.removePair(handCopy,gValue)
			gValue = self.absoluteGreatestValue(handCopy)
		return gValue


	def absoluteGreatestValue(self, hand):
		(aGValue, nipe) = hand[0]
		for (v, n) in hand:
			if v > gValue:
				aGValue = v
		return aGValue


	def valueOfHighestPair(self, hand):
		handCopy = copy.deepcopy(hand)
		for i in range(5):
			gValue = self.greatestValue(handCopy, i)
			if self.areRepeatedValues(handCopy, gValue, 2):
				return gValue

	def areRepeatedValues(self, hand, value, num):
		counter = 0
		for (v, n) in hand:
			if v == value:
				counter+=1
		return counter == num

	def removePair(self, hand, value):
		for (v, n) in hand:
			if v == value:
				hand.remove((v, n))
				return