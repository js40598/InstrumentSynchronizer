from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import os
import numpy as np
from pydub import AudioSegment
import time


class AudioFile:
    def __init__(self, directory):
        self.directory = directory
        self.format = directory.split('.')[-1]

    def convert(self, goto):
        exto = os.path.splitext(self.directory)[0] + '.' + goto
        if self.format == 'mp3':
            exfrom = AudioSegment.from_mp3(self.directory)
        elif self.format == 'wav':
            exfrom = AudioSegment.from_wav(self.directory)
        elif self.format == 'flv':
            exfrom = AudioSegment.from_flv(self.directory)
        elif self.format == 'ogg':
            exfrom = AudioSegment.from_ogg(self.directory)
        elif self.format == 'raw':
            exfrom = AudioSegment.from_raw(self.directory)
        exfrom.export(exto, format=goto)
        print('Audio succesfully converted from {} to {}'.format(self.format, goto))
        self.format = goto

    def read_audio_samples(self):
        if self.format != 'wav':
            self.convert('wav')
        self.audio = read(self.directory)
        print(self.audio)
        self.framerate = self.audio[0]
        self.samples = self.audio[1]
        self.samplesleft = []
        self.samplesright = []
        for x in self.samples:
            self.samplesleft.append(x[1])
            self.samplesright.append(x[0])

    def display_plot(self, start_at_second, end_at_second):
        start_at_second = round_seconds_by_frequency(self.framerate, start_at_second)
        end_at_second = round_seconds_by_frequency(self.framerate, end_at_second)
        audio_length = end_at_second - start_at_second
        plt.plot([x/self.framerate for x in range(0, int(audio_length * self.framerate))],
                 self.samplesright[int(start_at_second * self.framerate): int(self.framerate * end_at_second)],
                 linewidth=0.5)

        plt.plot([x/self.framerate for x in range(0, int(audio_length * self.framerate))],
                 self.samplesleft[int(start_at_second * self.framerate): int(self.framerate * end_at_second)],
                 linewidth=0.5)

        plt.ylabel("Amplitude")
        plt.xlabel("Time [s]")
        plt.title("Sample Wav")
        plt.show()

    def detect_notes(self):
        for sampleblock in self.samplesleft:
            pass
        for sample in self.samplesleft:
            pass
        pass

    def detect_tempo(self):
        pass




def round_seconds_by_frequency(framerate, seconds):
    seconds = framerate * seconds
    seconds = int(seconds)
    seconds = seconds / framerate
    return seconds


a = AudioFile('samples/sax.wav')

start_time = time.time()
a.read_audio_samples()
print("--- %s seconds ---" % (time.time() - start_time))
#a.display_plot(0, 1)


