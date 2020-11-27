import requests

for i in range(25):
	r=requests.get("http://jimmisimon.in/")
	print(r.status_code)
