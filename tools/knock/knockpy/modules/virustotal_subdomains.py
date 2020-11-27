import json
import urllib.request, urllib.parse, urllib.error

def get_subdomains(domain, apikey):
	url = 'https://www.virustotal.com/vtapi/v2/domain/report'
	parameters = {'domain': domain, 'apikey': apikey}
	try:
		response = urllib.request.urlopen('%s?%s' % (url, urllib.parse.urlencode(parameters))).read()
		response_dict = json.loads(response)
		return response_dict['subdomains']
	except:
		return False
