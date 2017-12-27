import csv
import time
import sys
import argparse
from multiprocessing import Process
sys.path.append('../')

from analysis import Analyzer 

def generateSymbols():
	exchangeList = ['amex','nasdaq','nyse','otc']

	allSymbols = open('symbols.csv', 'a')
	writer = csv.writer(allSymbols)

	sortedSymbols = list()
	for exchange in exchangeList:
		with open(exchange + '.csv', 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if(len(row)):
					sortedSymbols.append([row[0]])

	sortedSymbols.sort()
	for symbol in sortedSymbols:
		writer.writerow(symbol)

	allSymbols.close()


def generateSMA10x50():
	al = Analyzer()
	with open('smacross.txt', 'a') as s:
		with open('symbols.csv') as f:
			content = f.read().splitlines()
			for line in content:
				try:
					cross = al.smaCross(line, 10, 50)
					print line + ', ' + repr(cross)
					s.write(line + ', ' + repr(cross) + '\n')
				
				except (ValueError, IndexError):
					print line + ', ERR'
					s.write(line + ', ERR\n')
					continue


def processSMAWorker(al, symbolList, low, hi, c1, c2):
	for i in range(low, hi):
		try: 
			print (symbolList[i], al.smaCross(symbolList[i], c1, c2))
			time.sleep(1)
		except(ValueError):
			print(symbolList[i], 'ERR')
			time.sleep(2)
			continue
		except(IndexError):
			continue

def generateSomeSMA10x50(al, num):		
	if __name__ == '__main__':
		with open('smacross.txt', 'a') as s:
			with open('/home/ryanq2/Desktop/WinterProject/symbols/symbols.csv') as f:
				content = f.read().splitlines()
				p2 = Process(target=processSMAWorker, args=(al, content, 0, num/2, 10, 50,))
				p2.start()
				
				processSMAWorker(al, content, num/2, num, 10, 50,)
				p2.join()
			
def generateOneSMA10x50(symbol, al):
	return al.smaCross(symbol, 10, 50)


parser = argparse.ArgumentParser()
parser.add_argument('symbol', metavar='s', type=str)
parser.add_argument('analysis', metavar='a', type=str)
parser.add_argument('number', metavar='n', type=int)
args = parser.parse_args()	

al = Analyzer('7ZPUDRX84HS7NLN7')
print generateSomeSMA10x50(al, args.number)
