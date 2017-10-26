#!/usr/bin/python
import sys

class entry:

	name = 0
	data1 = 0
	data2 = 0
	data3 = 0
	data4 = 0
	data5 = 0
	data6 = 0
	data7 = 0
	data8 = 0
	data9 = 0
	data10 = 0

	def __init__(self, name, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10):
		self.name = name
		self.data1 = float(data1)
		self.data2 = float(data2)
		self.data3 = float(data3)
		self.data4 = float(data4)
		self.data5 = float(data5)
		self.data6 = float(data6)
		self.data7 = float(data7)
		self.data8 = float(data8)
		self.data9 = float(data9)
		self.data10 = float(data10)
	def __str__(self):
		return "Name: " + str(self.name) + " " + str(self.data1) + " " + str(self.data2) + " " + str(self.data3) + " " + str(self.data4) + " " + str(self.data5) + " " + str(self.data6) + " " + str(self.data7) + " " + str(self.data8) + " " + str(self.data9) + " " + str(self.data10)

def main():
	filename = sys.argv[1]
	fileIn = open(filename)
	contents = fileIn.readlines()

	#print(" ")
	#print(contents)
	print(" ")

	lookupTable = {}
	output1 = {}
	output2 = {}
	a_split = []
	countTable1 = {}
	countTable2 = {}
	keys = []
	pStrs = []
	kStrs = []
	discrepancyCount = 0;
	for line in contents:
		lineData = line.split() 
		
		key = lineData[0]
		
		exists = lookupTable.get(key, -1)
		if exists == -1:
			print("NEW")
			lookupTable[key] = []
			keys.append(key)
			
		newEntry = entry(lineData[1], lineData[2], lineData[3], lineData[4], lineData[5], lineData[6], lineData[7], lineData[8], lineData[9], lineData[10], lineData[11])
		lookupTable[key].append(newEntry)
		
	fileIn.close()
	print(" ")

	#for key in keys:
		#for thisEntry in lookupTable[key]:
			#print(key, thisEntry)

	print(" ")
 	#checking e-value
	for key in keys:
		print("Now analyzing keys(e-value): " + key)
		smallestEvalue = lookupTable[key][0].data9
		output1[key] = lookupTable[key][0]

		for thisEntry in lookupTable[key]:
			if thisEntry.data9 < smallestEvalue:
				smallestEvalue = thisEntry.data9
				output1[key] = thisEntry


	#checking Bitscore
	for key in keys:
		print("Now analyzing keys(bitscore): " + key)
		largestBitscore = lookupTable[key][0].data10
		output2[key] = lookupTable[key][0]

		for thisEntry in lookupTable[key]:
			if largestBitscore < thisEntry.data10:
				largestBitscore = thisEntry.data10
				output2[key] = thisEntry

	print("\nPrinting results...")
	for key in keys:
		print(key)
		print(output1[key])
		print(output2[key])

	print("\nCreating files...")
	filename = sys.argv[2]
	fKeys = open(filename, 'a+')
	filename = sys.argv[3]
	fCounts1 = open(filename, 'a+')
	filename = sys.argv[4]
	fCounts2 = open(filename, 'a+')

	print("\nChecking key similarity...")	
	for key in keys:
		#if output1[key] == output2[key]:
		#print("Same key!")
		print(key + " " + str(output1[key]))
		fKeys.write('{} {}\n'.format(key, output1[key]))
		
		a = lookupTable[key][0].name
		a_split = a.split(':')
		kStr = a[-6:]
		kStrs.append(kStr)
		print("Split value: " + str(a_split[0]))
		print("K value: " + kStr)
		
		#counting string before colon
		pStr = a_split[0]
		exists = countTable1.get(pStr, -1)
		if exists == -1:
			print("New string")
			countTable1[pStr] = 1
			pStrs.append(pStr)
		else:
			countTable1[pStr] = countTable1[pStr] + 1

		#counting string at end
		exists = countTable2.get(kStr, -1)
		if exists == -1:
			print("New K string")
			countTable2[kStr] = 1
		else:
			countTable2[kStr] = countTable2[kStr] + 1

		#else:
			#discrepancyCount = discrepancyCount + 1
			#print("Not the same!!!")
			#print(key)
			#fKeys.write('{}\n'.format(key))

	#print("Number of discrepancies: " + str(discrepancyCount))
	#fKeys.write('Number of discrepancies: {}\n'.format(discrepancyCount))
	for pStr in pStrs:
		fCounts1.write('{}: {}\n'.format(pStr, countTable1[pStr]))
	for kStr in kStrs:
		fCounts2.write('{}: {}\n'.format(kStr, countTable2[kStr]))

	#Counting organisms and KO values
	
	fKeys.close()
	fCounts1.close()
	fCounts2.close()


if __name__ == "__main__":
	main()
