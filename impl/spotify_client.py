import requests, time, threading
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

class SpotifyScreen:
    def __init__(self, config, modules):
        self.modules = modules

        self.canvas_width = 64
        self.canvas_height = 64

        self.current_art_url = ''
        self.current_art_img = None

        self.spotify_module = self.modules['spotify']

        self.response = None
        self.response_size = 0
        self.response_iterator = 0;
        self.thread = threading.Thread(target=self.get_top_albums_async)
        self.thread.start()

    def get_top_albums_async(self):
        print("Fetching albums...")
        # delay spotify fetches
        time.sleep(3)
        while True:
            self.response = self.spotify_module.get_top_albums()

            if self.response is not None:
                self.response_size = len(self.response)

            print(str(self.response_size) + " albums fetched!")

            # Fetch only once an hour
            time.sleep(3600)

    def generate_frame(self):
        if self.response is not None:
            if (self.response_iterator >= self.response_size):
                self.response_iterator = 0

            item = self.response[self.response_iterator]
            art_url = item['art_url']
            album = item['album']
            artist = item['artist']
            image = item['image']


            if self.current_art_url != art_url:
                self.current_art_url = art_url
                img = Image.open(BytesIO(image))
                self.current_art_img = img.resize((self.canvas_width, self.canvas_height), resample=Image.LANCZOS)

            frame = Image.new("RGB", (self.canvas_width, self.canvas_height), (0, 0, 0))
            frame.paste(self.current_art_img, (0, 0))

            self.debug(item)

            self.response_iterator = self.response_iterator + 1
            return frame
        else:
            # Not active
            return None

    def debug(self, item):
        print("Displaying " + item['album'] + " - " + item['artist'])
