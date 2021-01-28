from scipy.io.wavfile import read, write
from instrsyn.Metronome import Metronome
import matplotlib.pyplot as plt
import numpy as np
import time
from instrsyn.AudioFile import AudioFile
from instrsyn.Synchronizer import Synchronizer
from instrsyn.round_seconds_by_frequency import round_seconds_by_frequency
from instrsyn.bpm_detection import get_file_bpm
import os


def generate_metronome_with_provided_tick(tick_file_directory='samples/sounds/tick.wav',
                                          output_directory='samples/metronome/custom/generated_metronome.wav',
                                          frequency=44100,
                                          length=10,
                                          tempo=60,
                                          stereo=False):
    tick_file = AudioFile(tick_file_directory)
    metronome = Metronome(frequency, length, tempo, tick_file.read_audio_samples().T, stereo)
    write(output_directory, metronome.frequency, metronome.samples)


def read_file(file_directory,
              print_framerate=True,
              print_samplesleft=True):
    a = AudioFile(file_directory)
    if print_framerate:
        print('framerate:', a.framerate)
    if print_samplesleft:
        print(a.samplesleft)
    return a

start_time = time.time()

# FILE_DIRECTORY = 'samples/recorded_wav/60.wav'
# FILE_DIRECTORY = 'samples/metronome/generated_metronome.wav'

# # Metronome(frequency, duration_seconds, bpm, stereo=True)
# # creates metronome object
# # write('file/directory', frequency, array_of_samples)
# # selves: bpm, frequency, duration, samples, stereo

# m = Metronome(44100, 10, 60, False)
# print('samples: ', m.samples)
# print('highest sample: ', max(m.samples))
# write(FILE_DIRECTORY, m.frequency, m.samples)


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

# a = AudioFile(FILE_DIRECTORY)
# print('framerate:', a.framerate)
# a.display_plot(0)
# print(a.samplesleft)
# print('here', a.read_audio_samples().T)

# generate_metronome_with_provided_tick()

FILE_DIRECTORY = 'samples/metronome/custom/generated_metronome.wav'

a = read_file(FILE_DIRECTORY)
# a.convert('wav')
a.display_plot(0, 10)



# # get_file_bpm(path, params = None) params={'win_s': int,          # win_s
# #                                           'hop_s': int,          # h
# #                                           'samplerate': int})    # sample
# # return bpm of file (float)
bpm = 60
# bpm = get_file_bpm(a.directory, params={'win_s': 256,
#                                         'hop_s': 16,
#                                         'samplerate': a.framerate
#                                         })
print('bpm: ', bpm)

s = Synchronizer(a.framerate, int(bpm), list(a.samplesleft))

s.synchronize()

write('samples/synchronized/synchronized10sec.wav', s.framerate, np.array(s.synchronized_samples))

sa = read_file('samples/synchronized/synchronized10sec.wav')
sa.display_plot(0, 10)
print(sa.framerate)

print('beat indexes synchronized: ', s.beat_indexes)


print("--- %s seconds ---" % (time.time() - start_time))
