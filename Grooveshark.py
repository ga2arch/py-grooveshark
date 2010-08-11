import urllib2
import httplib2
import hashlib
import uuid
import json

listen_url = 'http://listen.grooveshark.com/'
cowbell_url = 'https://cowbell.grooveshark.com/service.php'
six_hex = hashlib.md5('Groovepy').hexdigest()[0:6]
groove_salt = 'quitStealinMahShit'

header = {}
header['user-agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)'

class Grooveshark:
	def __init__(self):
		self.sessionID = None
		self.secretKEY = None
		self.token = None
		self.uuid = str(uuid.uuid4())
		
	def getSessionID(self):
		req = urllib2.urlopen(listen_url)
		headers = req.headers.values()
		r = headers[2].split('=')[1]
		phpsessid = r.split(';')[0]
		self.sessionID = phpsessid

	def getSecretKEY(self):
		m = hashlib.md5(self.sessionID)
		self.secretKEY = m.hexdigest()

	def getToken(self):
		http = httplib2.Http()
		postdata = {"header":
						{"session":self.sessionID,
						 "uuid":self.uuid,
						 "client":"gslite",
						 "clientRevision":"20100412.81"},
					"parameters":
						{"secretKey":self.secretKEY},
					"method":"getCommunicationToken"}
		json_postdata = json.dumps(postdata)
		req = urllib2.urlopen(cowbell_url, json_postdata)
		request, reply = http.request(cowbell_url, 'POST', headers=header, body=json_postdata)
		self.token = json.loads(reply)['result']
		
	def useToken(self, method):
		tosha = '%s:%s:%s:%s' % (method)
		m = hashlib.sha1(method)
		
		

g = Grooveshark()
g.getSessionID()
g.getSecretKEY()
g.getToken()

print g.sessionID
print g.secretKEY
print g.token