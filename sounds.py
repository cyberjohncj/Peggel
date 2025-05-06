### STANDARD LIBRARIES
import os

from random import choice

### THIRD-PARTY LIBRARIES
import pygame

from pygame import mixer

#pygame.init()
mixer.init()

mp3_path_list = []
folder_path = "resources/sounds/tracks"
for file in os.listdir(folder_path):
    if file.endswith(".mp3"):
        mp3_path_list.append(str(os.path.join(folder_path, file)))

track_is_playing = False

cannon_shot = mixer.Sound("resources/sounds/cannon_shot.ogg")

### Peg Hits
peghit1 = mixer.Sound("resources/sounds/peghit_low.ogg")
peghit2 = mixer.Sound("resources/sounds/peghit.ogg")

def play_track(file_path: str, loop: bool = True):
    global track_is_playing

    try:
        mixer.music.load(file_path)
        mixer.music.play(-1 if loop else 0)
        track_is_playing = True
        return True
    except Exception as e:
        print(f"[Console]: No file '{file_path}' found in working directory.")
        return False

def stop_track():
    global track_is_playing

    mixer.music.stop()
    track_is_playing = False

def play_random_track():
    stop_track()
    try:
        random_track = choice(mp3_path_list)

        track_playing = play_track(random_track, True)
        if not track_playing:
            return False
        return True
    except IndexError:
        print("[Console]: No .mp3 files were found in /resources/sounds/tracks.")
        return False
    except Exception as e:
        print("[Console]: There was a problem trying to get an .mp3 file from /resources/sounds/tracks.", e)
        return False

    
