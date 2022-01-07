#!/usr/bin/env python3
from .basic import _Basic_class
import time
import threading
import pyaudio
import numpy as np

class Music(_Basic_class):
    MUSIC_BEAT = 500
    MUSIC_DIR = '/home/pi/Music/'
    SOUND_DIR = '/home/pi/Sound/'

    NOTES = {
        "Low C": 261.63,
        "Low C#": 277.18,
        "Low D": 293.66,
        "Low D#": 311.13,
        "Low E": 329.63,
        "Low F": 349.23,
        "Low F#": 369.99,
        "Low G": 392.00,
        "Low G#": 415.30,
        "Low A": 440.00,
        "Low A#": 466.16,
        "Low B": 493.88,
        "Middle C": 523.25,
        "Middle C#": 554.37,
        "Middle D": 587.33,
        "Middle D#": 622.25,
        "Middle E": 659.25,
        "Middle F": 698.46,
        "Middle F#": 739.99,
        "Middle G": 783.99,
        "Middle G#": 830.61,
        "Middle A": 880.00,
        "Middle A#": 932.33,
        "Middle B": 987.77,
        "High C": 1046.50,
        "High C#": 1108.73,
        "High D": 1174.66,
        "High D#": 1244.51,
        "High E": 1318.51,
        "High F": 1396.91,
        "High F#": 1479.98,
        "High G": 1567.98,
        "High G#": 1661.22,
        "High A": 1760.00,
        "High A#": 1864.66,
        "High B": 1975.53,
    }

    def __init__(self):
        import pygame
        self.pygame = pygame
        self.pygame.mixer.init()

    @property
    def MUSIC_LIST(self):
        from os import listdir
        return listdir(self.MUSIC_DIR)
        
    @property
    def SOUND_LIST(self):
        from os import listdir
        return listdir(self.SOUND_DIR)
        

    def note(self, n):
        try:
            n = self.NOTES[n]
            return n
        except:
            raise ValueError("{} is not a note".format(n))
    
    def beat(self, b):
        b = float(b)
        b = b * self.MUSIC_BEAT
        return b
    
    def tempo(self, *args):
        if len(args) == 0:
            return int(60.0 / (self.MUSIC_BEAT / 1000.0))
        else:
            try:
                tempo = int(args[0])
                self.MUSIC_BEAT = int((60.0 / tempo) * 1000.0)
                return tempo
            except:
                raise ValueError("tempo must be int not {}".format(args[0]))

    def sound_play(self, file_name):
        self.music_set_volume(80)
        self.pygame.mixer.music.load(file_name)
        self.pygame.mixer.music.play()

    def sound_effect_play(self, file_name):
        # file_name = self.SOUND_DIR + file_name
        music = self.pygame.mixer.Sound(str(file_name))
        time_delay = round(music.get_length(), 2)
        music.play()
        time.sleep(time_delay)

    def sound_effect_threading(self, file_name):
        # file_name = './sound/' + file_name
        obj = MyThreading(self.sound_effect_play, file_name=file_name)
        obj.start()

    def background_music(self, file_name, loops=-1, start=0.0, volume=50):#-1:continue
        if loops <= 0:
            loops = 0
        volume = round(volume/100.0, 2)
        # file_name = self.MUSIC_DIR + str(file_name)
        self.pygame.mixer.music.load(str(file_name))
        self.pygame.mixer.music.play(loops-1, start)

    def music_set_volume(self, value=50):
        value = round(value/100.0, 2)
        self.pygame.mixer.music.set_volume(value)

    def music_stop(self):
        self.pygame.mixer.music.stop()

    def music_pause(self):
        self.pygame.mixer.music.pause()

    def music_unpause(self):
        self.pygame.mixer.music.unpause()

    def sound_length(self, file_name):
        music = self.pygame.mixer.Sound(str(file_name))
        return round(music.get_length(),2)
    
    def play_tone_for(self, freq, duration):
        p = pyaudio.PyAudio()
        volume = 1 # range [0.0, 1.0]
        fs = 44100 # sampling rate, Hz, must be integer
        duration /= 2000 # devide 2 for half tone up half rest, divide 1000 for ms to s 
        _duration = duration * 4
        # generate samples, note conversion to float32 array
        samples = (np.sin(2*np.pi*np.arange(fs*_duration)*freq/fs)).astype(np.float32)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)

        # play. May repeat with different volume values (if done interactively) 
        stream.write(volume*samples)

        # stream.stop_stream()
        # stream.close()
        time.sleep(duration)


class MyThreading(threading.Thread):

    def __init__(self, func, **arg):
        super(MyThreading,self).__init__()
        self.func = func
        self.arg = arg

    def run(self):
        self.func(**self.arg)


