from alpha_vantage.techindicators import TechIndicators
from download import Downloader

import json
import csv
import argparse
import requests


#code speed be sure to remove when unnecessary
import timeit

class Analyzer:
	def __init__(self, key):
		self.dl = Downloader(key)
		self.currSymbol	= ""
		self.currData = []

	def updateSymbolList(self, symbol):
		if(symbol != self.currSymbol):
			self.currSymbol = symbol
			self.currData = sorted(self.dl.downloadCompanySymbol(symbol).items(), reverse=True)	
	
	def pprintJson(self, a):
		print json.dumps(a, indent=4, separators=(",", ": "))	

	#@params: symbol = company
	#	c1 = SMA count to be calculated
	#	c2 = SMA count to be calculated
	#returns whether or not the SMA[c1] has crossed SMA[c2]
	def smaCrossOld(self, symbol, c1, c2):
		#Two requests... May be better to do calculations manually
		smalist1 = sorted(self.dl.ti.get_sma(symbol, interval='daily', time_period=c1)[0].items(), reverse=True)
		smalist2 = sorted(self.dl.ti.get_sma(symbol, interval='daily', time_period=c2)[0].items(), reverse=True)		
		
		#Stored as (Date, Dict('SMA'=Value))
		todayc1 = float(smalist1[0][1]['SMA'])
		yestc1 = float(smalist1[1][1]['SMA'])
		
	
		todayc2 = float(smalist2[0][1]['SMA'])
		yestc2 = float(smalist2[1][1]['SMA'])

		if (todayc1 < todayc2) == (yestc1 < yestc2):	
			return False
		return True


 	#@params: symbol = company
	#	c1 = SMA count to be calculated
	#	c2 = "	"	"	"
	#@requires: c2 > c1, 0 < c2 < 99, 0 < c1 < 99
	#On average 3x faster than smaCrossOld
	def smaCross(self, symbol, c1, c2):
		self.updateSymbolList(symbol)	
		c = '4. close'		

		#sym[DATE][1][VALUE]
		#DATE from 0 being today, 1 being yesterday
		#VALUE being open, close, high, low...
		sum1, sum2 = 0, 0
		for i in range (1, c2):
			close = float(self.currData[i][1][c])
			if i < c1:
				sum1 += close 
			sum2 += close
		
		#today and yesterday's SMA[C1] and SMA[C2]
		todayc1 = (sum1 + float(self.currData[0][1][c]))/c1
		yestc1 = (sum1 + float(self.currData[c1][1][c]))/c1
		
		todayc2 = (sum2 + float(self.currData[0][1][c]))/c2
		yestc2 = (sum2 + float(self.currData[c2][1][c]))/c2	

		if (todayc1 < todayc2) == (yestc1 < yestc2):	
			return False
		return True
	
	#@params: symbol = company
	#	time = max high reached in past [time] days
	#	margin = % of calculated high to be reached
	#@requires: 1 > margin > 0, time < 100
	#@returns: True if today's high is within [margin] percent of period high
	def max(self, symbol, time, margin):
		self.updateSymbolList(symbol)	
		h = '2. high'
		high = -1

		for i in range(1, time):
			f = float(self.currData[i][1][h])
			if f > high:
				high = f
	
		if float(self.currData[0][1][h]) > (1 - margin)*high:
			return True
		return False

"""	
0N5JVZ3UXYOY0FLJ
7ZPUDRX84HS7NLN7
		
al = Analyzer()
		

start = timeit.default_timer()
print(al.smaCrossOld('AGIN', 10, 50))
stop1 = timeit.default_timer()
#al.smaCross('GOOGL', 10, 50)
#stop2 = timeit.default_timer()
print stop1 - start
#print stop2 - stop1
"""






