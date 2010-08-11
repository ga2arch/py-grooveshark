import urllib2
import httplib2
import hashlib
import uuid
import json
import inspect

listen_url = 'http://listen.grooveshark.com/'
cowbell_url = 'https://cowbell.grooveshark.com/service.php'
six_hex = hashlib.md5('Groovepy').hexdigest()[0:6]
groove_salt = 'quitStealinMahShit'
client_revision = '20100412.81'
header = {}
header['user-agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)'

class GrooveCommands:
	def __init__(self, session_id, secret_key, uuid):
		self.session_id = session_id
		self.uuid = uuid
		self.secret_key = secret_key
		self.postdata = {"header":
							{"session":self.session_id,
							 "uuid":self.uuid,
							 "client":"gslite",
							 "clientRevision":client_revision},
						"parameters":None,
						"token":None,
						"method":'%s'
						}

	def this_command(self):
		return inspect.stack()[1][3]

	def gen_token_command(self, method):
		tosha = '%s:%s:%s:%s' % (method, self.token, groove_salt, six_hex)
		m = hashlib.sha1(tosha).hexdigest()
		return m
	
	def getCommunicationToken(self):
		parameters = {'secretKey':self.secret_key}
		self.postdata['parameters'] = parameters
		self.postdata['method'] = self.this_command()
		return json.dumps(self.postdata)
		

class Grooveshark:
	def __init__(self):
		self.session_id = None
		self.secret_key = None
		self.token = None
		self.uuid = str(uuid.uuid4())

	def setup(self):
		self.get_session_id()
		self.get_secret_key()

		self.cmds = GrooveCommands(self.session_id, self.secret_key, self.uuid)
		
		self.get_token()
		self.uuid = str(uuid.uuid4())

		
	def get_session_id(self):
		req = urllib2.urlopen(listen_url)
		headers = req.headers.values()
		r = headers[2].split('=')[1]
		phpsessid = r.split(';')[0]
		self.session_id = phpsessid

	def get_secret_key(self):
		m = hashlib.md5(self.session_id)
		self.secret_key = m.hexdigest()

	def get_token(self):
		http = httplib2.Http()
		postdata = self.cmds.getCommunicationToken()
		req = urllib2.urlopen(cowbell_url, postdata)
		request, reply = http.request(cowbell_url, 'POST', headers=header, 
									  body=postdata)
		
		self.token = json.loads(reply)['result']

	
		
g = Grooveshark()
g.setup()

print g.session_id
print g.secret_key
print g.token
