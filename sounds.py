import pygame

from pygame import mixer

#pygame.init()
mixer.init()

is_music_playing = False

cannon_shot = mixer.Sound("resources/sounds/cannon_shot.ogg")
peghit = mixer.Sound("resources/sounds/peghit.ogg")

def play_music(file_name: str, loop: bool = True):
    global is_music_playing

    try:
        mixer.music.load(f"resources/sounds/{file_name}")
        mixer.music.play(-1 if loop else 0)
        is_music_playing = True
    except Exception as e:
        print(e)

def stop_music():
    global is_music_playing

    mixer.music.stop()
    is_music_playing = False
