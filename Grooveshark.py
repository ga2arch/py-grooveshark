import urllib2
import uuid

listen_url = 'http://listen.grooveshark.com/'
cowbell_url = 'http://cowbell.grooveshark.com/service.php'

class Grooveshark:
	def __init__(self):
		self.sessionID = None
		self.uuid = uuid.uuid4()
		
	def getSessionID(self):
		req = urllib2.urlopen(listen_url)
		headers = req.headers.values()
		r = headers[2].split('=')[1]
		phpsessid = r.split(';')[0]
		self.sessionID = phpsessid

	

g = Grooveshark()
g.getSessionID()