import os, requests, spotipy

class SpotifyModule:
    def __init__(self, config, time_range):
        self.invalid = False
        self.calls = 0
        self.config = config
        self.time_range = time_range
        self.unique_albums = {}

        if config is not None and 'Spotify' in config and 'client_id' in config['Spotify'] \
            and 'client_secret' in config['Spotify'] and 'redirect_uri' in config['Spotify']:

            client_id = config['Spotify']['client_id']
            client_secret = config['Spotify']['client_secret']
            redirect_uri = config['Spotify']['redirect_uri']
            if client_id != "" and client_secret != "" and redirect_uri != "":
                try:
                    os.environ["SPOTIPY_CLIENT_ID"] = client_id
                    os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
                    os.environ["SPOTIPY_REDIRECT_URI"] = redirect_uri

                    scope = "user-top-read"
                    self.auth_manager = spotipy.SpotifyOAuth(scope=scope, open_browser=False)
                    print(self.auth_manager.get_authorize_url())
                    self.sp = spotipy.Spotify(auth_manager=self.auth_manager, requests_timeout=10)
                    self.isPlaying = False
                except Exception as e:
                    print(e)
                    self.invalid = True
            else:
                print("[Spotify Module] Empty Spotify client id or secret")
                self.invalid = True
        else:
            print("[Spotify Module] Missing config parameters")
            self.invalid = True

    def get_top_albums(self):
        if self.invalid:
            return
        try:
            tracks_resp = self.sp.current_user_top_tracks(limit=20, offset=0, time_range=self.time_range)
            tracks = tracks_resp['items']

            if (len(tracks)):
                for track in tracks:
                    # Parse the response for artist and album data
                    artist = track['artists'][0]['name']
                    if len(track['artists']) >= 2:
                        artist = artist + ", " + track['artists'][1]['name']

                    album_name = track['album']['name']
                    art_url = track['album']['images'][0]['url']

                    # Make the requests for all the album art images now, so
                    # it doesn't need to be done each refresh of the screen
                    image = requests.get(art_url).content

                    self.unique_albums[album_name] = {'artist': artist, 'album': album_name, 'art_url': art_url, 'image': image}

                albums = []
                for album in self.unique_albums.items():
                    albums.append(album[1])
                return albums
        except Exception as e:
            print(e)
