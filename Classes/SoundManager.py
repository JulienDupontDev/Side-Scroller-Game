import pygame

pygame.mixer.init()


class SoundManager(object):
    def __init__(self):
        self.sounds = {}
        self.soundsPlaying = []

    def load_sounds(self, sounds):
        for sound in sounds:
            self.sounds[sound] = pygame.mixer.Sound(sounds[sound])

    def play_sound(self, sound, forcePlay=False):
        if sound not in self.soundsPlaying or forcePlay:
            self.sounds[sound].play()
            self.soundsPlaying.append(sound)

    def stop_sound(self, sound):
        if sound in self.soundsPlaying:
            self.sounds[sound].stop()
            self.soundsPlaying.remove(sound)

    # add sound
    def add_sound(self, sound):
        self.sounds[sound] = pygame.mixer.Sound(sound)
