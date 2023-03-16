# rpi-spotify-matrix-display

Displays album art for a user's top tracks on a 64x64 RGB LED matrix

## Spotify Pre-Setup
1. Go to https://developer.spotify.com/dashboard
2. Create an account and/or login
3. Select "Create an app" (name/description does not matter)
4. Copy the generated Client ID and Secret ID for later
5. Lastly, tap "Edit settings" and add `http://localhost:8080/callback` under Redirect URIs

## Setup
1. **Set your Client ID and Secret ID in the config.ini**
2. Update git submodules:
   - `git submodule update --init --recursive`
3. Install emulator dependencies (if not wanting to run emulated, you can skip this step):
   - `pip install RGBMatrixEmulator`
4. Run the app ([see below](#how-to-run))
   - More dependencies may need to be installed via pip depending on your machine
5. Authorize Spotify
   - After running, follow instructions provided in the console. Pasted link should begin with `http://localhost:8080/callback`

## How to Run
You can either run this project in an emulated state (separate window, browser, etc) or on an RGB LED matrix directly. Commands must be run from the `impl/` directory.

- To run emulated (on a PC/laptop):
    - `python3 controller.py -e`
- To run on a matrix (connected to a raspberry pi), run elevated:
    - `sudo python3 controller.py`

Options:
| Argument | Default | Description |
| :- | :- | :- |
|`-e` , `--emulated`| false | Run in a matrix emulator |
|`-t` , `--timerange`| s (short_term) | Time range to use when fetching top Spotify tracks. Options: `s`, `m`, `l` |
|`-h` , `--help`| false | Display help messages for arguments |

## Configuration
Configuration is handled in the `config.ini`.

For Matrix configuration, see https://github.com/hzeller/rpi-rgb-led-matrix#changing-parameters-via-command-line-flags.
More extensive customization can be done in `impl/controller.py` directly.

For Spotify configuration, set the `client_id` and `client_secret` to your own. You may leave `redirect_uri` alone.

## Acknowledgements
This project is adapted from kylejohnsonkj's https://github.com/kylejohnsonkj/rpi-spotify-matrix-display, and depends heavily on hzeller's [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix). Without their awesome work, I wouldn't have been able to start tinkering with this myself.
