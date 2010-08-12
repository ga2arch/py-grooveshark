from groovepy import Groovepy
import urllib2

def download_song_by_id(song_id, ip, streamkey):
    data = 'streamKey=%s' % (streamkey, )
    resp = urllib2.urlopen('http://%s/stream.php' % (ip,), data)
    rawfile = '%s.mp3' % (streamkey,)
    f = open(rawfile, 'wb')
    f.write(resp.read())
    f.close()
    #filemp3 = MP3(rawfile)
    #os.rename(rawfile, '%s - %s.mp3' % (str(filemp3['TPE1']), str(filemp3['TIT2'])))

g = Groovepy()
songid = 26613819
params = dict(songID=songid, prefetch=False, mobile=False, country=None)
result = g.run_method('getStreamKeyFromSongIDEx', params)
download_song_by_id(songid, result['ip'], result['streamKey'])