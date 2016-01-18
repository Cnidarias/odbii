import spotify
import threading

logged_in_event = threading.Event()

def connection_state_listener( session ):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in_event.set()


session = spotify.Session()

audio = spotify.AlsaSink( session )

loop = spotify.EventLoop( session )
loop.start()

session.on( spotify.SessionEvent.CONNECTION_STATE_UPDATED, connection_state_listener )

session.login( 'cnidarias', 'cml2ZXRpbmc=' )

logged_in_event.wait()

print session.connection.state
print session.user
session.get_published_playlists()
while len( session.playlist_container ) == 0:
    session.process_events()


shortestTime = 150000 
trackToSave = None
for playlist in session.playlist_container:
    playlist.load()
    print playlist.name


playList = session.playlist_container[0].load()

for t in playList.tracks:
    t.load()
    print t.name + u' ' + str( t.duration 

    session.player.load( t )

session.player.play()

while session.player.state == spotify.PlayerState.PLAYING:
    continue


