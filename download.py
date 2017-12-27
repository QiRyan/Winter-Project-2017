from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

import json
import csv
import argparse
import requests

class Downloader:
	nyse_stock_url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
	nasdaq_stock_url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download"
	amex_stock_url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download"
	otc_stock_url = "http://www.otcmarkets.com/reports/symbol_info.csv?__hstc=139045612.f8b461f9bbbfabe305d395d10d6dac4d.1357141537636.1373314633650.1373574135734.89&__hssc=139045612.4.1373574135734" 
	    
	def __init__(self, key):
        	self.key = key
        	self.ts = TimeSeries(key=self.key, retries=4)
		self.ti = TechIndicators(self.key)

	def downloadCompanySymbol(self, symbol):
        	data, meta = self.ts.get_daily(symbol)
		return data
        
	def downloadSymbolList(self, url, file_name):
        	"""Download and save the content as a csv file"""
        	csv = requests.get(url)
        	if(csv.ok == True):
			with open( file_name, "w") as csv_file:
				csv_file.write(csv.text)

    	def downloadNasdaqSymbols(self):
		self.downloadSymbolList(self.nasdaq_stock_url, "nasdaq.csv")

    	def downloadNyseSymbols(self):
        	self.downloadSymbolList(self.nyse_stock_url, "nyse.csv")

    	def downloadAmexSymbols(self):
        	self.downloadSymbolList(self.amex_stock_url, "amex.csv")

    	def downloadOtcSymbols(self):
        	self.downloadSymbolList(self.otc_stock_url, "otc.csv")

    	#Downloads all symbols from the NASDAQ, NYSE, AMEX, and OTC
	def downloadAllSymbols(self):
        	self.downloadNasdaqSymbols()
        	self.downloadNyseSymbols()
        	self.downloadAmexSymbols()
        	self.downloadOtcSymbols()
"""
	#@params: symbol = company
	#	c1 = SMA count to be calculated
	#	c2 = SMA count to be calculated
	#returns whether or not the SMA[c1] has crossed SMA[c2]
	def smaCross(self, symbol, c1, c2):
		ti = TechIndicators(self.key)
		
		#Two requests...? May be better to do calculations manually
		smalist1 = sorted(ti.get_sma(symbol, interval='daily', time_period=c1)[0].items(), reverse=True)
		smalist2 = sorted(ti.get_sma(symbol, interval='daily', time_period=c2)[0].items(), reverse=True)		
		
		todayc1 = float(smalist1[0][1].values()[0])
		yesterdayc1 = float(smalist1[1][1].values()[0])
		
	
		todayc2 = float(smalist2[0][1].values()[0])
		yesterdayc2 = float(smalist2[1][1].values()[0])


		print "today SMA10: " + repr(todayc1) + ", today SMA50: " + repr(todayc2)
		print "yesterday SMA10: " + repr(yesterdayc1) + ", yesterday SMA50: " + repr(yesterdayc2)

		if (todayc1 < todayc2) == (yesterdayc1 < yesterdayc2):	
			return False
		return True

		#print json.dumps(smalist1, indent=4, separators=(",", ": "))

"""     
