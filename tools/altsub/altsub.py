import sys
import argparse
import http.client
import os
import socket
import ssl
from colorama import init
from termcolor import colored
import faster_than_requests as requests
import nimporter
from nimpy import nimpy

parser = argparse.ArgumentParser(description='Find Subdomain from wordlist ')
parser.add_argument('-d','--domain',help='Wordlist of domain',required=True)
args=parser.parse_args()
target = args.domain

if os.path.exists(target) == True:
	with open(target) as f:
		num_lines = 0
		
		with open(target, 'r') as f:
			for line in f:
				num_lines += 1
		with open(target) as f:
			content = f.readlines()     
		content = [x.strip() for x in content]
		total_counts=num_lines
		for i in range(total_counts):
			try:
				https="[HTTPS]"
				http1="https://"
				url = "https://"+content[i]
				r=requests.head(url)
				print(r.get('status'))
				res=str(r.get('headers'))
				print(str(res))
				print(url)
			except:
				http="[HTTP]"
				http1="http://"
				url = "http://"+content[i]
				r=requests.head(url)
				print(r.get('status'))
				res=str(r.get('headers'))
				print(str(res))
				print(url)
				
else:
	print("File Not Available / Check File Name")
