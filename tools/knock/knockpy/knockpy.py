#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules import zonetransfer
from modules import header
from modules import resolve
from modules import wildcard
from modules import save_report
from modules import virustotal_subdomains

from urllib.parse import urlparse

import sys
import json
import os.path
import datetime
import argparse

__author__='Gianni \'guelfoweb\' Amato'
__version__='4.1.1'
__url__='https://github.com/guelfoweb/knock'
__description__='''\
___________________________________________

knock subdomain scan
knockpy v.'''+__version__+'''
Author: '''+__author__+'''
Github: '''+__url__+'''
___________________________________________
'''
__epilog__='''
example:
  knockpy domain.com
  knockpy domain.com -w wordlist.txt
  knockpy -r domain.com or IP
  knockpy -c domain.com
  knockpy -j domain.com

For virustotal subdomains support you can setting your API KEY in the
config.json file.
 
'''



def init(text, resp=False):
	if resp:
		print(text)
	else:
		print((text),end='')

def main():
	parser = argparse.ArgumentParser(
		formatter_class = argparse.RawTextHelpFormatter,
		prog = 'knockpy',
		epilog = __epilog__)

	parser.add_argument('domain', help = 'target to scan, like domain.com')
	parser.add_argument('-w', help = 'specific path to wordlist file',
					nargs = 1, dest = 'wordlist', required = False)
	parser.add_argument('-r', '--resolve', help='resolve single ip or domain name',
						action = 'store_true', required = False)
	parser.add_argument('-c', '--csv', help = 'save output in csv',
						action = 'store_true', required = False)
	parser.add_argument('-f', '--csvfields', help = 'add fields name to the first row of csv output file',
						action = 'store_true', required = False)
	parser.add_argument('-j', '--json', help = 'export full report in JSON',
						action = 'store_true', required = False)

						
	args = parser.parse_args()
	
	target = args.domain
	wlist = args.wordlist
	resolve_host = args.resolve
	save_scan_csv = args.csv
	save_scan_csvfields = args.csvfields
	save_scan_json = args.json

	

	'''
	start
	'''
	time_start = str(datetime.datetime.now())

	'''
	parse target domain
	'''
	if target.startswith("http") or target.startswith("ftp"):
		parsed_uri = urlparse(target)
		target = '{uri.netloc}'.format(uri = parsed_uri)

	'''
	check for virustotal subdomains
	'''
	
	subdomain_list = []

	_ROOT = os.path.abspath(os.path.dirname(__file__))
	config_file = os.path.join(_ROOT, '', 'config.json')

	if os.path.isfile(config_file):
		with open(config_file) as data_file:    
			apikey = json.load(data_file)
			try:
				apikey_vt = apikey['virustotal']
				if apikey_vt != '':
					virustotal_list = virustotal_subdomains.get_subdomains(target, apikey_vt)
					if virustotal_list:
						print((json.dumps(virustotal_list,indent=4,separators=(',',':'))))
						for item in virustotal_list:
							subdomain = item.replace('.'+target, '')
							if subdomain not in subdomain_list:
								subdomain_list.append(subdomain)
					else:
						init('NOT Found', True)
				else:
					init('VirusTotal API_KEY not found', True)
					init('\tVirusTotal API_KEY not found', True)
					virustotal_list = []
			except:
				init('VirusTotal API_KEY not found', True)
				init('\tVirusTotal API_KEY not found', True)
				virustotal_list = []
	else:
		init('CONFIG FILE NOT FOUND', True)
		init('\tCONFIG FILE NOT FOUND', True)
		virustotal_list = []

	

if __name__ == '__main__':
	main()
