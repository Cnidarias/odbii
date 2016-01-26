# odbii

So this is a long lasting projekt about building a functional On Board Computer for my 1996 Audi A4.
<br>
The name is given aafter the new Standard On Board Diagnostics II which has become the standard protocol for talking to the cars ECU's - it was standardized to control cars emissions.<br>

As it turns out though, my car is old enough, that OBDII did not exist back then and actually uses the <h5>KW 1281</h5> protcoll.
<br>
The settings and demands of this project are rather specific - here is what it currently does:

<ul>
<li>Can connect to the cars ecu (using python kw1281.py) In the file it specifies which address it should use for the ECU - implemented to run as a thread</li>
<li>Display a GUI which updates the RPM, Speed as well as usuage parameters provided by kw1281.py (usuage python gui.py)</li>
<li>Spotify client, lets you see all your playlists and lets you play one (does not show active song, pause and the likes implemented but not available in the gui as of now) (command line version python spotifyPython -- important need to login using command line version before starting gui.py as credientials are stored by spotify to just use relogin)</li>
<li>Working on visualizing the sound - to set LED Strips according to currently playing sound - hard</li>
</ul>
