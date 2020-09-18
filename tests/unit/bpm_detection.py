from unittest import TestCase
from instrsyn.Metronome import Metronome
from instrsyn.bpm_detection import get_file_bpm
from scipy.io.wavfile import write
import os


class BpmDetectionTest(TestCase):
    def test_bpm_detection(self):
        test_file_directory = os.path.join('unittest_samples', 'generated_metronome.wav')
        for i in range(60, 180):
            m = Metronome(44100, 15, i)
            write(test_file_directory, m.frequency, m.samples)
            self.assertEqual(int(abs(get_file_bpm(test_file_directory,
                                              params={'win_s': 256,
                                              'hop_s': 16,
                                              'samplerate': m.frequency
                                              }) - i)), 0)




