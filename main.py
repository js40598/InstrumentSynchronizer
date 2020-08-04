from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np
import time
from instrsyn.AudioFile import AudioFile
from instrsyn.round_seconds_by_frequency import round_seconds_by_frequency
from instrsyn.bpm_detection import get_file_bpm
import os

samples = {
    '45': 'samples/metronome/45.mp3',
    '52': 'samples/metronome/52.mp3',
    '57': 'samples/metronome/57.mp3',
    '61': 'samples/metronome/61.mp3',
    '65': 'samples/metronome/65.mp3',
    '79': 'samples/metronome/79.mp3',
    '90': 'samples/metronome/90.mp3',
    '112': 'samples/metronome/112.mp3',
    '129': 'samples/metronome/129.mp3',
    '164': 'samples/metronome/164.mp3',
    '183': 'samples/metronome/183.mp3',
    '200': 'samples/metronome/200.mp3',
}
test_file_directory = 'tests/unit/unittest_samples/45.mp3'

a = AudioFile(test_file_directory)
a.convert('wav')
for key, value in samples.items():
    start_time = time.time()

    a = AudioFile(value)
    a.read_audio_samples()
    a.display_plot(0, 1)
    bpm = get_file_bpm(a.directory, params={'win_s': 128,
                                            'hop_s': 32,
                                            'samplerate': a.framerate
                                            })
    print('BPM expected: ', key, '\nBPM detected: ', bpm)
    print("--- %s seconds ---" % (time.time() - start_time))



