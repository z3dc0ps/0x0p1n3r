#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script will return the subdomains of a main domain using the funcionality of virustotal
"""
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#Disable warning by SSL certificate
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import urllib.parse
from bs4 import BeautifulSoup
import argparse
from argparse import RawTextHelpFormatter
import xlsxwriter
import sys
import json
import socket



def WhoIP(domain):
	"""
	Function to obtain the IP of the domain - Reverse IP
	"""
	try:

		print (domain)
		ip=""
		try:
			ip = socket.gethostbyname(domain)
		except:
			ip = "0.0.0.0"
	except Exception as e:
		print ("Error in function WhoIP" + str(e))
	finally:
		return ip

def ExportResults(domain,ip,export):
	"""
	This function exports the results in xlsx format
	"""
	row = 0
	col = 0
	try:
		print ("\n")
		if export == "js": 
			#Export the results in json format
			print ("Exporting the results in an json")
			with open ('output.json','w') as f:
				json.dump(domain,f)
		elif (export == "xl"):
			#Export the results in excel format
			print ("\nExporting the results in an excel")
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
	except Exception as e:
		print ("Error in function ExportResults" + str(e))

def VisuResults(subdomain,export):
	"""
	This function shows the subdomains on the screen
	"""
	array_ip=[]
	ip =""
	try:
		for i in subdomain:
			ip = WhoIP(i)
			array_ip.append(ip)
			#print ("\n\t"+i)
	except Exception as e:
		print ("Error in function VisuResults" + str(e))
	finally:
		ExportResults(subdomain,array_ip,export)

def parser_html(data):
	"""
	This function parsers the response and obtain the domain
	"""
	subdomains =[]
	k = None
	try:
		for subdomain in data['data']:
			k = subdomain['id']
			subdomains.append(str(k))
	except Exception as e:
		print ("Error in function parser_html" + str(e))
	finally:	
		"""print (subdomains)	
		exit(1)"""
		return subdomains
def SendRequest(target,export):
	"""
	This function sends the HTTP GET request
	"""
	limit = 40 # the max lenght to look for without API
	url = "https://www.virustotal.com/ui/domains/{0}/subdomains?limit={1}".format(target, limit)
	response = ""
	subdomains = []
	try:
		try:
			#Requests
			#Timeout to verify if the resource is available and verify to ignore SSL certificate
			response=requests.get(url,allow_redirects=True, timeout=15,verify=False)	
		except requests.exceptions.RequestException as e:
			print ("\nError connection to server!",response.url)
			pass	
		except requests.exceptions.ConnectTimeout as e:
			print ("\nError Timeout")
			pass
	except Exception as e:
		print ("Error in function send_request" + str(e))
	finally:
		subdomains = parser_html(response.json())
		VisuResults(subdomains,export)

def main (argv):
	"""
    Main function of this tool
    """
	parser = argparse.ArgumentParser(description='This script obtains subdomains throught VirusTotal', formatter_class=RawTextHelpFormatter)
	parser.add_argument('-e','--export', help="Export the results to a json file (Y/N)\n Format available:\n\t1.json\n\t2.xlsx", required=False)
	parser.add_argument('-d','--domain', help="The domain to search subdomains",required=True)
	args = parser.parse_args()
	target = args.domain
	output=args.export
	export = ""
	if output is None:
		export='N'
	if ((output == 'y') or (output == 'Y')):
		print ("Select the output format:")
		print ("\n\t(js).json")
		print ("\n\t(xl).xlsx")
		export = input()
		if ((export != "js") and (export != "xl")):
			print ("Incorrect output format selected.")
			exit(1)
	SendRequest(target,export)

if __name__ == "__main__":
   main(sys.argv[1:])
