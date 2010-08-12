from groovepy import Groovepy
from mutagen.mp3 import MP3
import urllib2
import os

def search(query):
        params = dict(query=query, type='Songs')
        songs = g.run_method('getSearchResultsEx', params)['result']
        for song in songs:
            s = '%s - %s - %s - %s' % (song['ArtistName'], song['SongName'],
                                       song['AlbumName'], song['SongID'])
            print s

def download_song_by_id(song_id, folder):
    try:
        os.chdir(folder)
    except IOError:
        print 'Wrong folder'
    print 'Downloading song %s' % (song_id)
    params = dict(songID=song_id, prefetch=False, mobile=False, country=None)
    result = g.run_method('getStreamKeyFromSongIDEx', params)
    ip = result['ip']
    streamkey = result['streamKey']
    data = 'streamKey=%s' % (streamkey, )
    resp = urllib2.urlopen('http://%s/stream.php' % (ip,), data)
    rawfile = '%s.mp3' % (streamkey,)
    f = open(rawfile, 'wb')
    f.write(resp.read())
    f.close()
    filemp3 = MP3(rawfile)
    try:
        os.rename(rawfile, '%s.mp3' % (str(filemp3['TIT2'])))
    except Exception:
        pass

def get_playlists_by_user_id( user_id):
    params = dict(userID=user_id)
    playlists = g.run_method('userGetPlaylists', params)['Playlists']
    for playlist in playlists:
        print '%s - %s' % (playlist['Name'], playlist['PlaylistID'])

def get_songs_by_playlist_id(playlist_id):
    params = dict(playlistID=playlist_id)
    songs = g.run_method('playlistGetSongs', params)['Songs']
    for song in songs:
        s = '%s - %s - %s - %s' % (song['ArtistName'], song['Name'],
                                   song['AlbumName'], song['SongID'])
        print s

user_id = 4497783
play_id = 32429393
song_id = 18496982

g = Groovepy()
#search('Fabri Fibra')
#get_songs_by_playlist_id(play_id)
#get_playlists_by_user_id(user_id)
download_song_by_id(song_id, folder)
