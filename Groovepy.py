from mutagen.mp3 import MP3
import hashlib
import uuid
import json
import urllib2
import random 
import urllib
import os

songid = 26613819

class Groovepy:
    def __init__(self):
        self.headers = {}
        self.headers['Content-Type'] = 'application/json'
        self.headers['User-Agent'] = 'Mozilla/5.0 (compatible; Windows NT 5.1) Groovepy/1.0'

    def setup(self):
        resp = urllib2.urlopen('http://listen.grooveshark.com')
        self.session = resp.headers.values()[2].split('=')[1].split(';')[0]
        self.secretkey = hashlib.md5(self.session).hexdigest()
        self.uuid = str(uuid.uuid4()).upper()
        self.raw_token = self.get_raw_token()
        self.country = self.get_country()
        
    def get_raw_token(self):
        header = dict(client='gslite', uuid=self.uuid, session=self.session, clientRevision='20100412.81')
        params = dict(secretKey=self.secretkey)
        data = dict(header=header, method='getCommunicationToken', parameters=params)
        data_json = json.dumps(data)
        req = urllib2.Request('https://cowbell.grooveshark.com/service.php',data_json,headers=self.headers)
        resp = urllib2.urlopen(req)
        return json.loads(resp.read())['result']

    def gen_comm_token(self, method):
        method = method
        seed = "%06x" % random.getrandbits(24)
        tosha = '%s:%s:quitStealinMahShit:%s' % (method, self.raw_token, seed)
        gen_token = seed + hashlib.sha1(tosha).hexdigest()
        return gen_token

    def get_country(self):
        method = 'getCountry'
        gen_token = self.gen_comm_token(method)
        header = dict(client='gslite', uuid=self.uuid, session=self.session,
                      token=gen_token, clientRevision='20100412.81')
        data = dict(header=header, method=method, parameters={})
        data_json = json.dumps(data)
        req = urllib2.Request('http://cowbell.grooveshark.com/more.php?' + method,data_json,headers=self.headers)
        resp = urllib2.urlopen(req)
        return json.loads(resp.read())['result']

    def get_stream_key(self, song_id):
        method = 'getStreamKeyFromSongIDEx'
        gen_token = self.gen_comm_token(method)
        header = dict(client='gslite', uuid=self.uuid, session=self.session,
                      token=gen_token, clientRevision='20100412.81', country=self.country)
        params = dict(songID=26384161,  prefetch=False, mobile=False, country=self.country)
        data = dict(header=header, method=method, parameters=params)
        data_json = json.dumps(data)
        req = urllib2.Request('http://cowbell.grooveshark.com/more.php?' + method,data_json,headers=self.headers)
        resp = urllib2.urlopen(req)
        result = json.loads(resp.read())['result']
        return result['ip'], result['streamKey']

    def download_song_id(self, song_id):
        ip, streamkey = self.get_stream_key(song_id)
        data = dict(streamKey=streamkey)
        resp = urllib2.urlopen('http://%s/stream.php' % (ip,), urllib.urlencode(data))
        rawfile = '%s.mp3' % (streamkey,)
        f = open(rawfile, 'wb')
        f.write(resp.read())
        f.close()
        filemp3 = MP3(rawfile)
        os.rename(rawfile, '%s - %s.mp3' % (str(filemp3['TPE1']), str(filemp3['TIT2'])))

g = Groovepy()
g.setup()
g.download_song_id(songid)