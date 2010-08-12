import hashlib
import httplib2
import urllib2
import random
import json
import uuid

class Groovepy:
    def __init__(self):
        self.listen = 'http://listen.grooveshark.com'
        self.cowbell = 'https://cowbell.grooveshark.com'
        self.client_revision = '20100412.82'
        self.country = None
        self.headers = {}
        self.headers['Content-Type'] = 'application/json'
        self.headers['User-Agent'] = 'Mozilla/5.0 (compatible; Windows NT 5.1) Groovepy/1.0'
        self.setup()
        
    def setup(self):
        resp = urllib2.urlopen(self.listen)
        self.session = resp.headers.values()[2].split('=')[1].split(';')[0]
        self.secretkey = hashlib.md5(self.session).hexdigest()
        self.uuid = str(uuid.uuid4()).upper()
        self.raw_token = self.get_raw_token()
        self.country = self.run_method('getCountry')
        
    def get_raw_token(self):
        header = dict(client='gslite', uuid=self.uuid, session=self.session, 
                      clientRevision=self.client_revision)
        params = dict(secretKey=self.secretkey)
        data = dict(header=header, method='getCommunicationToken', parameters=params)
        data_json = json.dumps(data)
        url = '%s/service.php' % (self.cowbell,)
        req = urllib2.Request(url, data_json, headers=self.headers)
        resp = urllib2.urlopen(req)
        return json.loads(resp.read())['result']

    def gen_comm_token(self, method):
        method = method
        seed = "%06x" % random.getrandbits(24)
        tosha = '%s:%s:quitStealinMahShit:%s' % (method, self.raw_token, seed)
        gen_token = seed + hashlib.sha1(tosha).hexdigest()
        return gen_token

    def get_song_name_by_id(self, song_id):
        http = httplib2.Http()
        http.follow_redirects = False
        url = '%s/song/%s' % (self.listen, song_id)
        header, resp = http.request(url)
        raw_name = header['location'].split('/')[2]
        song_name = ' '.join(raw_name.split('+'))
        return song_name
        
    def run_method(self, method, params={}, url='more.php'):
        gen_token = self.gen_comm_token(method)
        
        header = dict(client='gslite', uuid=self.uuid, session=self.session,
                      token=gen_token, clientRevision=self.client_revision)
        if self.country:
            header['country'] = self.country
            params['country'] = self.country
            
        data = dict(header=header, method=method, parameters=params)
        
        data_json = json.dumps(data)
        url = '%s/%s?%s' % (self.cowbell, url, method)
        req = urllib2.Request(url, data_json,headers=self.headers)
        json_resp = urllib2.urlopen(req)
        resp = json.loads(json_resp.read())
        if resp.has_key('fault'):
            raise Exception(resp['fault']['message'], resp['fault']['code'])
        return resp['result']
