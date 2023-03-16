import os, inspect, sys, time, configparser, argparse
from PIL import Image

import spotify_client
import spotify_module


def main():
    canvas_width = 64
    canvas_height = 64

    # get arguments
    parser = argparse.ArgumentParser(
                    prog='RpiMatrixSpotifySlideshow',
                    description='Displays album art of a user\'s top tracks on an LED matrix')

    parser.add_argument('-e', '--emulated', action='store_true', help='Run in a matrix emulator')
    parser.add_argument('-t', '--timerange', default='s', choices=['s', 'm', 'l'], help='Time range to use when fetching top Spotify tracks.')
    args = parser.parse_args()

    is_emulated = args.emulated

    if args.timerange == 'm':
        time_range = 'medium_term'
    elif args.timerange == 'l':
        time_range = 'long_term'
    else:
        time_range = 'short_term'

    print("Emulated: " + str(is_emulated))
    print("Time range: " + time_range)

    # switch matrix library import if emulated
    if is_emulated:
        from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
    else:
        from rgbmatrix import RGBMatrix, RGBMatrixOptions

    # get config
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    sys.path.append(currentdir+"/rpi-rgb-led-matrix/bindings/python")

    config = configparser.ConfigParser()
    parsed_configs = config.read('../config.ini')

    if len(parsed_configs) == 0:
        print("no config file found")
        sys.exit()

    # connect to Spotify and create display image
    modules = {'spotify': spotify_module.SpotifyModule(config, time_range)}
    app_list = [spotify_client.SpotifyScreen(config, modules)]

    # setup matrix
    options = RGBMatrixOptions()
    options.hardware_mapping = config.get('Matrix', 'hardware_mapping', fallback='regular')
    options.rows = canvas_width
    options.cols = canvas_height
    options.brightness = 100 if is_emulated else config.getint('Matrix', 'brightness', fallback=100)
    options.gpio_slowdown = config.getint('Matrix', 'gpio_slowdown', fallback=1)
    options.limit_refresh_rate_hz = config.getint('Matrix', 'limit_refresh_rate_hz', fallback=0)
    options.drop_privileges = False
    matrix = RGBMatrix(options=options)

    black_screen = Image.new("RGB", (canvas_width, canvas_height), (0, 0, 0))

    # generate image
    while True:
        time.sleep(5)
        frame = app_list[0].generate_frame()

        if frame is None:
            frame = black_screen

        matrix.SetImage(frame)
        time.sleep(0.08)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted with Ctrl-C')
        sys.exit(0)
