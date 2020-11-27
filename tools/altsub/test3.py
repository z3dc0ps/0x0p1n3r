import http.client

for i in range():
	conn = http.client.HTTPConnection("jimmisimon.in")
	conn.request("HEAD", "/")
	res = conn.getresponse()
	print(res.status)
