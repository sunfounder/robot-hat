#!/usr/bin/env python3
from .basic import _Basic_class
import time
import threading
import pyaudio
import os
import struct
import math
from .utils import enable_speaker, disable_speaker

class Music(_Basic_class):
    """Play music, sound affect and note control"""

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    KEY_G_MAJOR = 1
    KEY_D_MAJOR = 2
    KEY_A_MAJOR = 3
    KEY_E_MAJOR = 4
    KEY_B_MAJOR = 5
    KEY_F_SHARP_MAJOR = 6
    KEY_C_SHARP_MAJOR = 7

    KEY_F_MAJOR = -1
    KEY_B_FLAT_MAJOR = -2
    KEY_E_FLAT_MAJOR = -3
    KEY_A_FLAT_MAJOR = -4
    KEY_D_FLAT_MAJOR = -5
    KEY_G_FLAT_MAJOR = -6
    KEY_C_FLAT_MAJOR = -7

    KEY_SIGNATURE_SHARP = 1
    KEY_SIGNATURE_FLAT = -1

    WHOLE_NOTE = 1
    HALF_NOTE = 1/2
    QUARTER_NOTE = 1/4
    EIGHTH_NOTE = 1/8
    SIXTEENTH_NOTE = 1/16

    NOTE_BASE_FREQ = 440
    """Base note frequency for calculation (A4)"""
    NOTE_BASE_INDEX = 69
    """Base note index for calculation (A4) MIDI compatible"""

    NOTES = [
        None,  None, None,  None, None, None,  None, None,  None, None,  None, None,
        None,  None, None,  None, None, None,  None, None,  None, "A0", "A#0", "B0",
        "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
        "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
        "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
        "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
        "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
        "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6",
        "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7",
        "C8"]
    """Notes name, MIDI compatible"""

    def __init__(self):
        import warnings
        warnings_bk = warnings.filters
        warnings.filterwarnings("ignore")
        # close welcome message of pygame, and the value must be <str> 
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1" 
        import pygame
        warnings.filters = warnings_bk
        """Initialize music"""
        self.pygame = pygame
        self.pygame.mixer.init()
        self.time_signature(4, 4)
        self.tempo(120, 1/4)
        self.key_signature(0)
        #
        enable_speaker()

    def time_signature(self, top: int = None, bottom: int = None):
        """
        Set/get time signature

        :param top: top number of time signature
        :type top: int
        :param bottom: bottom number of time signature
        :type bottom: int
        :return: time signature
        :rtype: tuple
        """
        if top == None and bottom == None:
            return self._time_signature
        if bottom == None:
            bottom = top
        self._time_signature = (top, bottom)
        return self._time_signature

    def key_signature(self, key: int = None):
        """
        Set/get key signature

        :param key: key signature use KEY_XX_MAJOR or String "#", "##", or "bbb", "bbbb"
        :type key: int/str
        :return: key signature
        :rtype: int
        """
        if key == None:
            return self._key_signature
        if isinstance(key, str):
            if "#" in key:
                key = len(key)*self.KEY_SIGNATURE_SHARP
            elif "b" in key:
                key = len(key)*self.KEY_SIGNATURE_FLAT
        self._key_signature = key
        return self._key_signature

    def tempo(self, tempo=None, note_value=QUARTER_NOTE):
        """
        Set/get tempo beat per minute(bpm)

        :param tempo: tempo
        :type tempo: float
        :param note_value: note value(1, 1/2, Music.HALF_NOTE, etc)
        :return: tempo
        :rtype: int
        """
        if tempo == None and note_value == None:
            return self._tempo
        try:
            self._tempo = (tempo, note_value)
            self.beat_unit = 60.0 / tempo
            return self._tempo
        except:
            raise ValueError("tempo must be int not {}".format(tempo))

    def beat(self, beat):
        """
        Calculate beat delay in seconds from tempo

        :param beat: beat index
        :type beat: float
        :return: beat delay
        :rtype: float
        """
        beat = beat / self._tempo[1] * self.beat_unit
        return beat

    def note(self, note, natural=False):
        """
        Get frequency of a note

        :param note_name: note name(See NOTES)
        :type note_name: string
        :param natural: if natural note
        :type natural: bool
        :return: frequency of note
        :rtype: float
        """
        if isinstance(note, str):
            if note in self.NOTES:
                note = self.NOTES.index(note)
            else:
                raise ValueError(
                    f"note {note} not found, note must in Music.NOTES")
        if not natural:
            note += self.key_signature()
            note = min(max(note, 0), len(self.NOTES)-1)
        note_delta = note - self.NOTE_BASE_INDEX
        freq = self.NOTE_BASE_FREQ * (2 ** (note_delta / 12))
        return freq

    def sound_play(self, filename, volume=None):
        """
        Play sound effect file

        :param filename: sound effect file name
        :type filename: str
        """
        sound = self.pygame.mixer.Sound(filename)
        if volume is not None:
            # attention: 
            #   The volume of sound and music is separate, 
            # and the volume of different sound objects is also separate.
            sound.set_volume(round(volume/100.0, 2))
        time_delay = round(sound.get_length(), 2)
        sound.play()
        time.sleep(time_delay)

    def sound_play_threading(self, filename, volume=None):
        """
        Play sound effect in thread(in the background)

        :param filename: sound effect file name
        :type filename: str
        :param volume: volume 0-100, leave empty will not change volume
        :type volume: int
        """
        obj = threading.Thread(name="Sound Play Thread", target=self.sound_play, kwargs={
                               "filename": filename, "volume": volume})
        obj.start()

    def music_play(self, filename, loops=1, start=0.0, volume=None):
        """
        Play music file

        :param filename: sound file name
        :type filename: str
        :param loops: number of loops, 0:loop forever, 1:play once, 2:play twice, ...
        :type loops: int
        :param start: start time in seconds
        :type start: float
        :param volume: volume 0-100, leave empty will not change volume
        :type volume: int
        """
        if volume is not None:
            self.music_set_volume(volume)
        self.pygame.mixer.music.load(filename)
        self.pygame.mixer.music.play(loops, start)

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

    def music_resume(self):
        """Resume music"""
        self.pygame.mixer.music.unpause()

    def music_unpause(self):
        """Unpause music(resume music)"""
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
        return round(music.get_length(), 2)

    def get_tone_data(self, freq: float, duration: float):
        """
        Get tone data for playing

        :param freq: frequency
        :type freq: float
        :param duration: duration in seconds
        :type duration: float
        :return: tone data
        :rtype: list
        """
        """
        Credit to: Aditya Shankar & Gringo Suave https://stackoverflow.com/a/53231212/14827323
        """
        duration /= 2.0
        frame_count = int(self.RATE * duration)

        remainder_frames = frame_count % self.RATE
        wavedata = []

        for i in range(frame_count):
            a = self.RATE / freq  # number of frames per wave
            b = i / a
            # explanation for b
            # considering one wave, what part of the wave should this be
            # if we graph the sine wave in a
            # displacement vs i graph for the particle
            # where 0 is the beginning of the sine wave and
            # 1 the end of the sine wave
            # which part is "i" is denoted by b
            # for clarity you might use
            # though this is redundant since math.sin is a looping function
            # b = b - int(b)

            c = b * (2 * math.pi)
            # explanation for c
            # now we map b to between 0 and 2*math.PI
            # since 0 - 2*PI, 2*PI - 4*PI, ...
            # are the repeating domains of the sin wave (so the decimal values will
            # also be mapped accordingly,
            # and the integral values will be multiplied
            # by 2*PI and since sin(n*2*PI) is zero where n is an integer)
            d = math.sin(c) * 32767
            e = int(d)
            wavedata.append(e)

        for i in range(remainder_frames):
            wavedata.append(0)

        number_of_bytes = str(len(wavedata))
        wavedata = struct.pack(number_of_bytes + 'h', *wavedata)

        return wavedata

    def play_tone_for(self, freq, duration):
        """
        Play tone for duration seconds

        :param freq: frequency, you can use NOTES to get frequency
        :type freq: float
        :param duration: duration in seconds
        :type duration: float
        """
        """
        Credit to: Aditya Shankar & Gringo Suave https://stackoverflow.com/a/53231212/14827323
        """
        p = pyaudio.PyAudio()
        frames = self.get_tone_data(freq, duration)
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS,
                        rate=self.RATE, output=True)
        stream.write(frames)
        # stream.stop_stream()
        # stream.close()
