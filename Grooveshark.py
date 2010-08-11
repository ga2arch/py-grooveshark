import urllib2
import hashlib
import uuid

listen_url = 'http://listen.grooveshark.com/'
cowbell_url = 'http://cowbell.grooveshark.com/service.php'

class Grooveshark:
	def __init__(self):
		self.sessionID = None
		self.secretKEY = None
		self.uuid = uuid.uuid4()
		
	def getSessionID(self):
		req = urllib2.urlopen(listen_url)
		headers = req.headers.values()
		r = headers[2].split('=')[1]
		phpsessid = r.split(';')[0]
		self.sessionID = phpsessid

	def getSecretKEY(self):
		m = hashlib.md5(self.sessionID)
		self.secretKEY = m.hexdigest()
		

g = Grooveshark()
g.getSessionID()
g.getSecretKEY()

print g.sessionID
print g.secretKEY