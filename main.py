# ReactBot for Linux
# This program requires root permission. See the README for more information.

import json
import os
import random
import keyboard
import vlc
import time
import sys

# Reads the config.json file in the local directory, stores it in a dict "config"
with open('config.json') as config_file:
    config: dict = json.load(config_file)

# Serializes the data in config to unique variables, because I think it looks nicer and this program is too short to worry about stuff like that
idle_path: str = config['idle']
phrases_directory: str = config['phrases']
phrase_key: str = config['phrase_key']
quit_key: str = config['quit']
aout: str = config['aout']

# Initializes vlc, with the aout parameter if it was provided in the config
if aout:
    instance: vlc.Instance = vlc.Instance(f'--aout={aout}')
else:
    instance: vlc.Instance = vlc.Instance()
player: vlc.MediaPlayer = instance.media_player_new()

def play_video(path: str) -> None:
    """Plays a video in vlc. Once this function is called, the instance and player have been set up, so we can set the media to whatever path was supplied and play it."""
    media: vlc.Media = instance.media_new(path)
    player.set_media(media)
    player.play()

def play_random_video() -> None:
    """Chooses and plays a random video from the phrases directory as defined in the config."""
    files: list[str] = os.listdir(phrases_directory) # List of paths to each video
    video_files: list[str] = [file for file in files if file.endswith(".mp4")] # Filter those paths by the ones not ending in .mp4 (should remove nothing unless something is wrong)
    if video_files:
        filename: str = random.choice(video_files)
        play_video(phrases_directory + "/" + filename)

def verify_paths() -> None:
    """Checks each entry in config.json to be sure it's valid"""
    if not os.path.exists(idle_path):
        print(f"{idle_path} (idle_path in config) doesn't exist")
        sys.exit()
    if not os.path.exists(phrases_directory):
        print(f"{phrases_directory} (phrases_directory in config) doesn't exist")
        sys.exit()
    # I'm not sure if there's any way to check if the key specified is actually valid
    if phrase_key == "":
        print(f"Phrase key is empty")
        sys.exit()
    if quit_key == "":
        print(f"Quit key is empty. Did you even read the README?")
        sys.exit()

def main() -> None:
    verify_paths() # This function will exit if there are any problems

    # Start ReactBot's initial idle animation
    media: vlc.Media = instance.media_new(idle_path)
    player.set_media(media)
    player.video_set_scale(0.25) # So it fits in the corner of your screen, you can resize it though.
    player.play()
    player.set_fullscreen(False)

    while True:
        if keyboard.is_pressed(phrase_key):
            play_random_video()
            # the keyboard.is_pressed function triggers multiple times a second because human reaction time, so we let this thread sleep to prevent multiple phrases being started at once
            time.sleep(1)
        if keyboard.is_pressed(quit_key):
            break
        time.sleep(0.1) # To limit CPU usage, we only poll for a keypress every 100ms
        if player.get_state() in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]: # This loops the video once the idle animation finishes
            play_video(idle_path)
            continue

    # Cleanly exit once the user presses the quit key, and we break out of the loop
    player.stop()
    sys.exit()

if __name__ == "__main__":
    # Also exit cleanly if we ran through a terminal and we ctrl+c
    try:
        # This checks if we are root, os.geteuid() means get effective user id, and the root user has an effective user id of 0
        if os.geteuid() != 0:
            os.execvp("sudo", ["sudo"] + sys.argv) # Re-run the program as the root user if possible
        main()
    except KeyboardInterrupt:
        player.stop()
        sys.exit(0)
