#!/usr/bin/env python3
from .basic import _Basic_class
import time
import threading
import pyaudio
import numpy as np

class Music(_Basic_class):
    """Play music, sound affect and note control"""

    MUSIC_BEAT = 500
    """Beat delay in miliseconds"""

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
    """Notes frequency dictionary"""

    def __init__(self):
        """Initialize music"""
        import pygame
        self.pygame = pygame
        self.pygame.mixer.init()

    @property
    def MUSIC_LIST(self):
        """Music list"""
        from os import listdir
        return listdir(self.MUSIC_DIR)
        
    @property
    def SOUND_LIST(self):
        """Sound list"""
        from os import listdir
        return listdir(self.SOUND_DIR)
        

    def note(self, n):
        """
        Get frequency of a note
        
        :param n: note index(See NOTES)
        :type n: int
        :return: frequency of note
        :rtype: float
        """
        try:
            n = self.NOTES[n]
            return n
        except:
            raise ValueError("{} is not a note".format(n))
    
    def beat(self, b):
        """
        Get beat delay in miliseconds
        
        :param b: beat index
        :type b: float
        :return: beat delay
        :rtype: float
        """
        b = float(b)
        b = b * self.MUSIC_BEAT
        return b
    
    def tempo(self, *args):
        """
        Set/get tempo beat per minute(bpm)
        
        :param args: tempo
        :type args: float
        :return: tempo
        :rtype: float
        :raises ValueError: if tempo is not a int or float
        """
        if len(args) == 0:
            return int(60.0 / (self.MUSIC_BEAT / 1000.0))
        else:
            try:
                tempo = int(args[0])
                self.MUSIC_BEAT = int((60.0 / tempo) * 1000.0)
                return tempo
            except:
                raise ValueError("tempo must be int not {}".format(args[0]))

    def sound_effect_play(self, filename):
        """
        Play sound effect(mp3, wav) file
        
        :param filename: sound effect file name
        :type filename: str
        """
        music = self.pygame.mixer.Sound(str(filename))
        time_delay = round(music.get_length(), 2)
        music.play()
        time.sleep(time_delay)

    def sound_effect_threading(self, filename, volume=None):
        """
        Play sound effect(mp3, wav) with threading(in the background)
        
        :param filename: sound effect file name
        :type filename: str
        :param volume: volume 0-100, leave empty will not change volume
        :type volume: int
        """
        if volume is not None:
            self.music_set_volume(volume)
        obj = MyThreading(self.sound_effect_play, filename=filename)
        obj.start()

    def sound_play(self, filename, volume=None):
        """
        Play music file(mp3)
        
        :param filename: sound file name
        :type filename: str
        :param volume: volume 0-100, leave empty will not change volume
        :type volume: int
        """
        if volume is not None:
            self.music_set_volume(volume)
        self.pygame.mixer.music.load(filename)
        self.pygame.mixer.music.play()

    def background_music(self, filename, loops=-1, start=0.0, volume=None):#-1:continue
        """
        Play music file(mp3) in the background

        :param filename: music file name
        :type filename: str
        :param loops: number of loops, -1:loop forever, 1:play once, 2:play twice, ...
        :type loops: int
        :param start: start time in seconds
        :type start: float
        :param volume: volume 0-100, leave empty will not change volume
        :type volume: int
        """
        if loops <= 0:
            loops = 0
        if volume is not None:
            self.music_set_volume(volume)
        self.pygame.mixer.music.load(str(filename))
        self.pygame.mixer.music.play(loops-1, start)

    def music_set_volume(self, value):
        """
        Set music volume

        :param value: volume 0-100
        :type value: int
        """
        value = round(value/100.0, 2)
        self.pygame.mixer.music.set_volume(value)

    def music_stop(self):
        """Stop music"""
        self.pygame.mixer.music.stop()

    def music_pause(self):
        """Pause music"""
        self.pygame.mixer.music.pause()

    def music_unpause(self):
        """Unpause music"""
        self.pygame.mixer.music.unpause()

    def sound_length(self, filename):
        """
        Get sound effect length in seconds

        :param filename: sound effect file name
        :type filename: str
        :return: length in seconds
        :rtype: float
        """
        music = self.pygame.mixer.Sound(str(filename))
        return round(music.get_length(),2)
    
    def play_tone_for(self, freq, duration):
        """
        Play tone for duration seconds

        :param freq: frequency, you can use NOTES to get frequency
        :type freq: float
        :param duration: duration in seconds
        :type duration: float
        """
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


