#!/usr/bin/env python

from __future__ import unicode_literals

import cmd
import logging
import threading

import spotify


class Commander(cmd.Cmd):

    doc_header = "Commands"
    prompt = "spotify> "

    logger = logging.getLogger("shell.commander")

    def __init__(self, shouldCommander):
        if shouldCommander:
            cmd.Cmd.__init__(self)
        self.shouldReturn = False
        if not shouldCommander:
            self.shouldReturn = True

        self.PlayList = []
        self.currentSong = 0

        self.logged_in = threading.Event()
        self.logged_out = threading.Event()
        self.logged_out.set()

        self.session = spotify.Session()
        self.session.on(
            spotify.SessionEvent.CONNECTION_STATE_UPDATED,
            self.on_connection_state_changed,
        )
        self.session.on(spotify.SessionEvent.END_OF_TRACK, self.on_end_of_track)

        try:
            self.audio_driver = spotify.AlsaSink(self.session)
        except ImportError:
            self.logger.warning("No audio sink found; audio playback unavailable.")

        self.event_loop = spotify.EventLoop(self.session)
        self.event_loop.start()

    def on_connection_state_changed(self, session):
        if session.connection.state is spotify.ConnectionState.LOGGED_IN:
            self.logged_in.set()
            self.logged_out.clear()
        elif session.connection.state is spotify.ConnectionState.LOGGED_OUT:
            self.logged_in.clear()
            self.logged_out.set()

    def on_end_of_track(self, session):
        self.session.player.play(False)
        self.logger.info("SONG ENDED")
        if self.PlayList:
            if self.currentSong < len(self.PlayList):
                self.play_nextSong()

    def precmd(self, line=""):
        if line:
            self.logger.debug("New command: %s", line)
        return line

    def emptyline(self):
        pass

    def do_debug(self, line=""):
        "Show more logging output"
        print("Logging at DEBUG level")
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    def do_info(self, line=""):
        "Show normal logging output"
        print("Logging at INFO level")
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    def do_warning(self, line=""):
        "Show less logging output"
        print("Logging at WARNING level")
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)

    def do_EOF(self, line=""):
        "Exit"
        if self.logged_in.is_set():
            print("Logging out...")
            self.session.logout()
            self.logged_out.wait()
        self.event_loop.stop()
        print("")
        return True

    def do_login(self, line=""):
        "login <username> <password>"
        tokens = line.split(" ", 1)
        if len(tokens) != 2:
            self.logger.warning("Wrong number of arguments")
            return
        username, password = tokens
        self.session.login(username, password, remember_me=True)
        self.logged_in.wait()
        if self.shouldReturn:
            return "Logging in"

    def do_relogin(self, line=""):
        "relogin -- login as the previous logged in user"
        try:
            self.session.relogin()
            self.logged_in.wait()
        except spotify.Error as e:
            self.logger.error(e)
        if self.shouldReturn:
            return "Relogging"

    def do_forget_me(self, line=""):
        "forget_me -- forget the previous logged in user"
        self.session.forget_me()

    def do_logout(self, line=""):
        "logout"
        self.session.logout()
        self.logged_out.wait()

    def do_whoami(self, line=""):
        "whoami"
        if self.logged_in.is_set():
            self.logger.info(
                "I am %s aka %s. You can find me at %s",
                self.session.user.canonical_name,
                self.session.user.display_name,
                self.session.user.link,
            )
        else:
            self.logger.info(
                "I am not logged in, but I may be %s", self.session.remembered_user
            )

    def do_get_Playlist(self, line=""):
        "Get Playlists of the currently logged in user"
        if not self.logged_in.is_set():
            self.logger.warning("You must be logged in to play")
            return
        try:
            self.session.get_published_playlists()
            while len(self.session.playlist_container) <= 0:
                self.session.process_events()

            returnString = []
            self.logger.info("Playlists:")
            for playlist in self.session.playlist_container:
                plList = playlist.load()
                self.logger.info("[%s] %s", plList.link, plList.name)
                arr = []
                arr.append(plList.link)
                arr.append(plList.name)
                returnString.append(arr)

        except spotify.Error as e:
            self.logger.warning(e)
            return
        if self.shouldReturn:
            return returnString

    def do_play_playlist(self, line):
        if not self.logged_in.is_set():
            self.logger.warning("You must be logged in to play")
            return
        try:
            playlist = self.session.get_playlist(line)
            playlist.load()
        except (ValueError, spotify.Error) as e:
            self.logger.warning(e)

        self.logger.info("Playlist %s loaded", playlist.name)
        playlist.set_autolink_tracks

        self.PlayList = []

        returnString = []

        for track in playlist.tracks:
            ltrack = track.load()
            self.logger.info(
                "[%s] %s - %s ", ltrack.link, ltrack.artists[0].name, ltrack.name
            )
            self.PlayList.append(str(ltrack.link))
            arr = []
            arr.append(ltrack.link)
            arr.append(ltrack.name)
            arr.append(ltrack.duration)
            arr.append(ltrack.artists[0].name)
            returnString.append(arr)

        self.currentSong = 0
        self.play_nextSong()
        if self.shouldReturn:
            return returnString

    def play_nextSong(self):
        self.do_play_uri(str(self.PlayList[self.currentSong]))
        self.currentSong += 1

    def do_play_uri(self, line=""):
        "play <spotify track uri>"
        if not self.logged_in.is_set():
            self.logger.warning("You must be logged in to play")
            return
        try:
            track = self.session.get_track(line)
            track.load()
        except (ValueError, spotify.Error) as e:
            self.logger.warning(e)
            return
        self.logger.info("Loading track into player")
        self.session.player.load(track)
        self.logger.info("Playing track")
        self.session.player.play()
        if self.shouldReturn:
            return "Playing Track"

    def do_pause(self, line=""):
        self.logger.info("Pausing track")
        self.session.player.play(False)

    def do_resume(self, line=""):
        self.logger.info("Resuming track")
        self.session.player.play()

    def do_stop(self, line=""):
        self.logger.info("Stopping track")
        self.session.player.play(False)
        self.session.player.unload()

    def do_seek(self, seconds):
        "seek <seconds>"
        if not self.logged_in.is_set():
            self.logger.warning("You must be logged in to seek")
            return
        if self.session.player.state is spotify.PlayerState.UNLOADED:
            self.logger.warning("A track must be loaded before seeking")
            return
        self.session.player.seek(int(seconds) * 1000)

    def do_search(self, query):
        "search <query>"
        if not self.logged_in.is_set():
            self.logger.warning("You must be logged in to search")
            return
        try:
            result = self.session.search(query)
            result.load()
        except spotify.Error as e:
            self.logger.warning(e)
            return
        self.logger.info(
            "%d tracks, %d albums, %d artists, and %d playlists found.",
            result.track_total,
            result.album_total,
            result.artist_total,
            result.playlist_total,
        )
        self.logger.info("Top tracks:")
        returnString = []
        for track in result.tracks:
            self.logger.info(
                "[%s] %s - %s", track.link, track.artists[0].name, track.name
            )

            arr = []
            arr.append(str(track.link))
            arr.append(track.artists[0].name)
            arr.append(track.name)
            returnString.append(arr)

        if self.shouldReturn:
            return returnString


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Commander(True).cmdloop()

    # c = Commander(False)
    # c.do_relogin()
    # q = c.do_search("Imagine Dragons")
    # c.do_logout()
    # print q
