import http.client
import ssl

conns = http.client.HTTPConnection("jimmisimon.in")
conns.request("HEAD", "/")
res = conns.getresponse()
head = res.getheaders()
print(head)
if "Server" in head:
	print("server available")
else:
	print("no server")
