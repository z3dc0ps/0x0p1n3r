#!/usr/bin/env python
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#Disable warning by SSL certificate
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from urlparse import urlparse
from bs4 import BeautifulSoup
import argparse
from argparse import RawTextHelpFormatter
import xlsxwriter
import json
import sys
import socket

def banner():
	print """   
	                  ...-'  |`.  _______                                         
	 .----.     .----.|      |  | \  ___ `'.                      __  __   ___    
	  \    \   /    / ....   |  |  ' |--.\  \                    |  |/  `.'   `.  
	   '   '. /'   /    -|   |  |  | |    \  '     .-''` ''-.    |   .-.  .-.   ' 
	   |    |'    /      |   |  |  | |     |  '  .'          '.  |  |  |  |  |  | 
	   |    ||    |   ...'   `--'  | |     |  | /              ` |  |  |  |  |  | 
	   '.   `'   .'   |         |`.| |     ' .''                '|  |  |  |  |  | 
	    \        /    ` --------\ || |___.' /' |         .-.    ||  |  |  |  |  | 
	     \      /      `---------'/_______.'/  .        |   |   .|__|  |__|  |__| 
	      '----'                  \_______|/    .       '._.'  /                  
	                                             '._         .'                   
	                                                '-....-'`                    
		"""
	print "\n"
	print """** Tool to obtain subdomains throught Virustotal's search
	    ** Author: Ignacio Brihuega Rodriguez a.k.a N4xh4ck5
	    ** DISCLAMER This tool was developed for educational goals. 
	    ** The author is not responsible for using to others goals.
	    ** A high power, carries a high responsibility!
	    ** Version 1.0"""

def help():
	print  """ \nThis script obtains subdomains throught Virustotal's search

	 			Example of usage: python v1d0m.py -d apple.es """

def WhoIP(domain):
	print domain
	ip=""
	try:
		ip = socket.gethostbyname(domain)
	except Exception as e:
		print e
		print "It can't obtain the reverse IP"
		ip = "0.0.0.0"
	return ip

def ExportResults(domain,ip,export):

	print "\n"
	row = 0
	col = 0
	if export == "js": 
		#Export the results in json format
		print "Exporting the results in an json"
		with open ('output.json','w') as f:
			json.dump(ip,f)
	elif (export == "xl"):
		#Export the results in excel format
		print "\nExporting the results in an excel"
		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook('output.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write(row, col, "Domain")
		worksheet.write(row, col+1, "IP")
		row +=1
		for dom in domain:
			col = 0
			worksheet.write(row, col, dom)
			row += 1
		#update row
		row = 1
		for direction_ip in ip:
			col = 1
			worksheet.write(row, col, direction_ip)
			row += 1
		#close the excel
		workbook.close()

def VisuResults(subdomain,export):
	array_ip=[]
	ip =""
	for i in subdomain:
		print "subdomains: "
		ip = WhoIP(i)
		array_ip.append(ip)
		print "\n\t- " + i+ " ["+ip+"]"
	ExportResults(subdomain,array_ip,export)

def parser_html(response):
	subdomains =[]
	i = 0
	soup = BeautifulSoup(response.text, 'html.parser')
	for link_div in soup.findAll('div',{'id':'observed-subdomains'}):
		try:
			for link in link_div.findAll('a',href=True):
				try:
					if (urlparse(link.get('href'))!='' and urlparse(link.get('href')).path.strip()!=''):	
						subdomains.append(urlparse(link.get('href')).path.split("domain/")[1].replace("/information/", "")) 
				except Exception as e:
					print e
					pass

		except Exception as e:
			print e
			pass
	return subdomains
def SendRequest(target,export):
	url ="https://www.virustotal.com/es/domain/"+target+"/information/"
	response = ""
	subdomains = []
	try:
		#Requests
		#Timeout to verify if the resource is available and verify to ignore SSL certificate
		response=requests.get(url,allow_redirects=True, timeout=10,verify=False)	
	except requests.exceptions.RequestException as e:
		print "\nError connection to server!",response.url,
		pass	
	except requests.exceptions.ConnectTimeout as e:
		print "\nError Timeout"
		pass
	subdomains = parser_html(response)
	VisuResults(subdomains,export)

def main (argv):
	parser = argparse.ArgumentParser(description='This script obtains subdomains throught VirusTotal', formatter_class=RawTextHelpFormatter)
	parser.add_argument('-e','--export', help="Export the results to a json file (Y/N)\n Format available:\n\t1.json\n\t2.xlsx", required=False)
	parser.add_argument('-d','--domain', help="The domain to search subdomains",required=True)
	args = parser.parse_args()
	banner()
	help()
	target = args.domain
	output=args.export
	export = ""
	if output is None:
		export='N'
	if ((output == 'y') or (output == 'Y')):
		print "Select the output format:"
		print "\n\t(js).json"
		print "\n\t(xl).xlsx"
		export = raw_input()
		if ((export != "js") and (export != "xl")):
			print "Incorrect output format selected."
			exit(1)
	SendRequest(target,export)

if __name__ == "__main__":
   main(sys.argv[1:])
