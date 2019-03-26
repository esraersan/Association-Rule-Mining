# Finding association rules between itemsets using Apriori Algorithm 
#run with "python apriori.py" command

import itertools

"""prompt user to enter minsupport and minconfidence values in percent"""
# I wanted to turn all the float numbers as percentage cause i had many problems and it took so much time 

MinSupport = int(input("Minimum support : %"))
MinConfidence = int(input("Minimum confidence : % "))

##FIRST PART
C1 = {} #dict
"""total number of transactions contained in the file"""
NumberOfTransactions = 0
Dataset = []
TransactionList = []
with open("input.txt", "r") as f:
	for line in f:
		TransactionList = []
		NumberOfTransactions += 1
		for number in line.split():
			TransactionList.append(number)
			if number not in C1.keys():
				C1[number] = 1
			else:
				count = C1[number]
				C1[number] = count + 1
		Dataset.append(TransactionList)
print ("-------------------------DATASET----------------------------")
print (Dataset)
print ("****************************************************************")
#print "--------------------CANDIDATE 1-ITEMSET------------------------- "
#print C1
#print "-----------------------------------------------------------------"

#Second Part
#we should find subsets
def FindSubsets(S,m):
	return set(itertools.combinations(S, m))

"""Compute frequent 1-itemset"""
#this is only for the 1-itemset so i am not going to create a function for
L1 = []
for key in C1:
	if (100 * C1[key]/NumberOfTransactions) >= MinSupport:
		list = []
		list.append(key)
		L1.append(list)
print ("----------------------frequent 1-itemset-------------------------")
print (L1)
print ("*******************************************************************")

#Third Part  
"""Apriori function to compute candidate k-itemset, (Ck) , using frequent (k-1)-itemset, (Lk_1)"""
"""FindInfrequentItemset function to determine if pruning is required to remove unuseful candidates (c) using the Apriori property, with prior knowledge of frequent (k-1)-itemset (Lk_1)"""
 

def FindInfrequentItemset(c, Lk_1, k):
	list = []
	list = FindSubsets(c,k)
	for item in list: 
		s = []
		for l in item:
			s.append(l)
		s.sort()
		if s not in Lk_1:
			return True
	return False

def Apriori(Lk_1, k):
	length = k
	Ck = [] 
	for list1 in Lk_1:
		for list2 in Lk_1:
			count = 0
			c = []
			if list1 != list2:
				while count < length-1:
					if list1[count] != list2[count]:
						break
					else:
						count += 1
				else:
					if list1[length-1] < list2[length-1]:
						for item in list1:
							c.append(item)
						c.append(list2[length-1])
						if not FindInfrequentItemset(c, Lk_1, k):
							Ck.append(c) #then we add the item as a frequent(we called the finding infrequent if this list is empty then it means frequent)
							c = []
	return Ck

"""FrequentItemsets function to compute all frequent itemsets"""
#to have new L all the time

def FrequentItemsets():
	k = 2
	Lk_1 = []
	Lk = []
	L = []
	count = 0
	NumberOfTransactions = 0
	for item in L1:
		Lk_1.append(item)
	while Lk_1 != []:
		Ck = []
		Lk = []
		Ck = Apriori(Lk_1, k-1)
		#print "-------------------------CANDIDATE %d-ITEMSET---------------------" % k
		#print "Ck: %s" % Ck
		#print "------------------------------------------------------------------"
		for c in Ck:
			count = 0
			NumberOfTransactions = 0
			s = set(c)
			for TransactionList in Dataset:
				NumberOfTransactions += 1
				t = set(TransactionList)
				if s.issubset(t) == True:
					count += 1
			if (100 * count/NumberOfTransactions) >= MinSupport:
				c.sort()
				Lk.append(c)
		Lk_1 = []
		print ("-----------------------frequent %d-itemset------------------------" % k)
		print (Lk)
		print ("********************************************************************")
		for l in Lk:
			Lk_1.append(l)
		k += 1
		if Lk != []:
			L.append(Lk)
	
	return L
	 
		
"""FindAssociationRules function to mine and print all the association rules with given support and confidence value"""

def FindAssociationRules():
	num = 1
	L= FrequentItemsets()
	print ("---------------------ASSOCIATION RULES------------------")
	print ("RULES \t SUPPORT \t CONFIDENCE")
	print ("--------------------------------------------------------")

#So here basically you are generating the rules on frequent itemset
	for list in L:
		for l in list:
			length = len(l)
			count = 1
			while count < length: 
				r = FindSubsets(l,count)
				count += 1
				for item in r:
					supportof_associative_itemset_1 = 0 #this is support of {x,y}
					supportof_associative_itemset_2 = 0 #this is support of {y}
					s = []#associative_itemset_1
					m = []#associative_itemset_2
					for i in item:
						s.append(i)
					for TransactionList in Dataset:
						if set(s).issubset(set(TransactionList)) == True:
							supportof_associative_itemset_1 += 1
						if set(l).issubset(set(TransactionList)) == True:
							supportof_associative_itemset_2 += 1
					if 100*supportof_associative_itemset_2/supportof_associative_itemset_1 >= MinConfidence:
						for index in l:
							if index not in s:
								m.append(index)
						print ("Association Rule %d. : %s ==> %s %d %d" %(num, s, m, 100*supportof_associative_itemset_2/len(Dataset), 100*supportof_associative_itemset_2/supportof_associative_itemset_1))
						num += 1  

FindAssociationRules()   
