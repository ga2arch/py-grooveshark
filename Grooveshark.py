import urllib2
import httplib2
import hashlib
import uuid
import json
import inspect
import random
import string 

listen_url = 'http://listen.grooveshark.com/'
cowbell_url = 'https://cowbell.grooveshark.com/service.php'
groove_salt = 'quitStealinMahShit'
client_revision = '20100412.81'

class GrooveMethods:
	def __init__(self, session_id, secret_key, token, uuid):
		self.session_id = session_id
		self.secret_key = secret_key
		self.token = token
		self.uuid = uuid.upper()

	def set_token(self, token):
		self.token = token
	
	def build_postdata(self, parameters, method):
		postdata = {"header":
						{"session":self.session_id,
						 "uuid":self.uuid,
						 "client":"gslite",
						 "country":{"CC1":"0","CC4":"0","CC2":"2199023255552","ID":"106","CC3":"0"},
						 "clientRevision":client_revision},
					"parameters":parameters,
					"token":self.gen_token_command(method),
					"method":method
					}
		return json.dumps(postdata)

	def this_method(self):
		return inspect.stack()[1][3]

	def gen_token_command(self, method):
		six_hex = ''.join(random.choice(string.hexdigits) for n in range(6))
		tosha = '%s:%s:%s:%s' % (method, self.token, groove_salt, six_hex.lower())
		print tosha
		m = hashlib.sha1(tosha).hexdigest()
		token = six_hex.lower() + m
		return token
		
	def getCommunicationToken(self):
		parameters = {'secretKey':self.secret_key}
		postdata = self.build_postdata(parameters, self.this_method())
		return postdata

	def getSearchResults(self):
		parameters = {"query":"lol2","type":"Songs"}
		postdata = self.build_postdata(parameters, self.this_method())
		return postdata

	def getStreamKeyFromSongIDEx(self):
		parameters = {"prefetch":'false',"country":{"CC1":"0","CC4":"0","CC2":"2199023255552","ID":"106","CC3":"0"},"songID":26384045,"mobile":'false'}
		postdata = self.build_postdata(parameters, self.this_method())
		return postdata
		
class Grooveshark:
	def __init__(self):
		self.session_id = None
		self.secret_key = None
		self.token = None
		self.uuid = str(uuid.uuid4())
		self.headers = {}
		self.headers['user-agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)'

	def setup(self):
		self.get_session_id()
		self.get_secret_key()

		self.cmds = GrooveMethods(self.session_id, self.secret_key, self.token, self.uuid)
		
		self.get_token()
		self.uuid = str(uuid.uuid4())

	def run_method(self, method, *args):
		global cowbell_url
		postdata = getattr(self.cmds, method)(*args)
		http = httplib2.Http()
		req = urllib2.urlopen(cowbell_url, postdata)
		request, reply = http.request(cowbell_url, 'POST', headers=self.headers, 
									  body=postdata)
		if method == 'getCommunicationToken':
			self.headers['Cookie'] = request['set-cookie']
		print reply
		return json.loads(reply)
		
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
		result = self.run_method('getCommunicationToken')['result']
		print result
		self.token = result
		self.cmds.set_token(result) 

	def tag(self):
		result = self.run_method('getSearchResults')
		print result
		
		
g = Grooveshark()
g.setup()
g.run_method('getStreamKeyFromSongIDEx')
