from scipy.io.wavfile import read, write
from instrsyn.Metronome import Metronome
import matplotlib.pyplot as plt
import numpy as np
import time
from instrsyn.AudioFile import AudioFile
from instrsyn.round_seconds_by_frequency import round_seconds_by_frequency
from instrsyn.bpm_detection import get_file_bpm
import os

FILE_DIRECTORY = 'samples/metronome/generated_metronome.wav'


# # Metronome(frequency, duration_seconds, bpm, stereo=True)
# # creates metronome object
# # write('file/directory', frequency, array_of_samples)
# # selves: bpm, frequency, duration, samples, stereo

m = Metronome(44100, 10, 60, True)
print(m.samples)
write(FILE_DIRECTORY, m.frequency, m.samples)


# # AudioFile('file/directory')
# # creates audio file object
# # methods:
# # convert(goto, delete_file) gotos: mp3, wav, flv, raw, ogg,
# # delete_file = True to delete file you are converting from
# # read_audio_samples() change format if not wav,
# # reads file framerate and samples in stereo if possible,
# # does not need to be executed!
# # display_plot(start_at_second, end_at_second)
# # detect_notes(), detect_tempo() does not work
# # selves: directory, format, audio, framerate, samplesleft, samplesright

a = AudioFile(FILE_DIRECTORY)
a.display_plot(0, 200/44100)
print(a.samplesleft)
print(a.samplesright)


# # get_file_bpm(path, params = None) params={'win_s': int,          # win_s
# #                                           'hop_s': int,          # h
# #                                           'samplerate': int})    # sample
# # return bpm of file (float)
bpm = get_file_bpm(a.directory, params={'win_s': 256,
                                        'hop_s': 16,
                                        'samplerate': a.framerate
                                        })

