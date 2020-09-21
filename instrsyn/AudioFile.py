from scipy.io.wavfile import read
from instrsyn.round_seconds_by_frequency import round_seconds_by_frequency
import matplotlib.pyplot as plt
from pydub import AudioSegment
import os
import numpy as np


class AudioFile:
    def __init__(self, directory):
        self.directory = directory
        self.format = directory.split('.')[-1]
        self.audio = self.read_audio()
        self.samplesleft, self.samplesright = self.read_audio_samples()
        self.framerate = self.audio[0]

    def convert(self, goto, delete_file=False):
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
        if delete_file:
            os.remove(self.directory)
        self.format = goto
        self.directory = list(self.directory)
        self.directory[-3:] = self.format
        self.directory = ''.join(list(self.directory))

    def read_audio(self):
        if self.format != 'wav':
            self.convert('wav')
        return read(self.directory)

    def read_audio_samples(self):
        if isinstance(self.audio[1][0], np.ndarray):
            return self.audio[1].T
        else:
            return [self.audio[1], self.audio[1]]

    def display_plot(self, start_at_second, end_at_second):
        start_at_second = round_seconds_by_frequency(self.framerate, start_at_second)
        end_at_second = round_seconds_by_frequency(self.framerate, end_at_second)
        audio_length = end_at_second - start_at_second

        plt.plot([x / self.framerate for x in range(0, int(audio_length * self.framerate))],
                 self.samplesright[int(start_at_second * self.framerate): int(self.framerate * end_at_second)],
                 linewidth=0.5)

        plt.plot([x / self.framerate for x in range(0, int(audio_length * self.framerate))],
                 self.samplesleft[int(self.framerate * start_at_second): int(self.framerate * end_at_second)],
                 linewidth=0.5)

        plt.ylabel("Amplitude")
        plt.xlabel("Time [s]")
        plt.title("Sample Wav")
        plt.show()


#     def detect_notes(self):
#         #self.sampleblocks = np.array(self.audio[1])
#         possible_bpm = [200, 183, 164, 129, 112, 90, 79, 65, 57, 52, 51, 45, 35]
#         possible_bps = [x/60 for x in possible_bpm]
#         total_beats = possible_bps[0] * len(self.audio[1]) / self.framerate
#         total_full_beats = int(total_beats)
#         holder = []
#         print(len(self.audio[1]), 'here')
#         print(total_beats)
#         for i in range(len(self.audio[1]), int((total_full_beats * self.framerate) / possible_bps[0]), -1):
#             holder.append(i)
#             self.audio[1][:-1]
#         print(self.audio[1].reshape(total_full_beats, -1))
#
#     def detect_tempo(self):
#         count = 0
#         length = len(self.samplesleft)
#         numOfWin = length / (43 * 1024)
#         numOfWin = int(numOfWin)
#         newNumSamp = numOfWin * (43 * 1024)
#         yLeft = self.samplesleft[0:newNumSamp]
#         yRight = self.samplesright[0:newNumSamp]
#         LReshapedData = np.array(yLeft).reshape(1024, numOfWin * 43)
#         RReshapedData = np.array(yRight).reshape(1024, numOfWin * 43)
#         EWin = np.zeros(43)
#         for i in range(43, 0, -1):
#             Eseg = sum(np.power(LReshapedData[:, i], 2) + np.power(RReshapedData[:, i], 2))
#             EWin[43-i] = Eseg
#         for i in range(43, numOfWin * 43):
#             Eseg = sum(np.power(LReshapedData[:, i], 2) + np.power(RReshapedData[:, i], 2))
#             avgE = sum(EWin) / 43
#             VarE = sum(np.power(np.add(EWin, avgE), 2)) / 43
#             C = (-0.0025714 * VarE) + 1.5142857
#             if EWin[0] > abs(C)*avgE:
#                 count += 1
#             EWin = np.append(EWin[1:42], Eseg)
#         tsec = newNumSamp / self.framerate
#         tmin = tsec / 60
#         numBPM = count/tmin
#         print(numBPM)
