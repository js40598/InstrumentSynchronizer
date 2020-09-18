from scipy.io.wavfile import read, write
from instrsyn.Metronome import Metronome
import matplotlib.pyplot as plt
import numpy as np
import time
from instrsyn.AudioFile import AudioFile
from instrsyn.round_seconds_by_frequency import round_seconds_by_frequency
from instrsyn.bpm_detection import get_file_bpm
import os


# # Metronome(frequency, duration_seconds, bpm)
# # creates metronome object
# # write('file/directory', frequency, array_of_samples)
# # selves: bpm, frequency, duration, samples

m = Metronome(44100, 10, 120)
write('samples/metronome/generated_metronome.wav', m.frequency, m.samples)


# # AudioFile('file/directory')
# # creates audio file object
# # methods:
# # convert(goto) gotos: mp3, wav, flv, raw, ogg
# # read_audio_samples() change format if not wav,
# # reads file framerate and samples in stereo if possible
# # display_plot(start_at_second, end_at_second)
# # detect_notes(), detect_tempo() does not work
# # selves: directory, format, audio, framerate, samplesleft, samplesright

a = AudioFile('samples/metronome/generated_metronome.wav')
a.read_audio_samples()
a.display_plot(0, 5)



# # get_file_bpm(path, params = None) params={'win_s': int,          # win_s
# #                                           'hop_s': int,          # h
# #                                           'samplerate': int})    # sample
# # return bpm of file (float)
bpm = get_file_bpm(a.directory, params={'win_s': 256,
                                        'hop_s': 16,
                                        'samplerate': a.framerate
                                        })
print(bpm)
