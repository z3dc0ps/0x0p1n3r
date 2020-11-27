import nimporter
import faster_than_requests as requests
import nimporter


try:
	r=requests.head("https://elk-mika.nokia.com/")
	print(r.get('status'))
	res=str(r.get('headers'))
	print(str(res))

except nimporter.SslError:
	print("error")
except:
	print("other")


"""	
except:
	r=requests.head("http://dev-on-business.nokia.com")
	print(r.get('status'))
	res=str(r.get('headers'))
	print(str(res))
"""
