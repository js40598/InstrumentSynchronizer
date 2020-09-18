from unittest import TestCase
from instrsyn.Metronome import Metronome
import os


class MetronomeTest(TestCase):
    def test_metronome_init(self):
        test_file_directory = os.path.join('unittest_samples', 'generated_metronome.wav')
        m = Metronome(44100, 10, 60)
        self.assertEqual(m.duration, len(m.samples) / 44100)
        self.assertEqual(m.duration, 10)
        self.assertEqual(m.frequency, 44100)
        self.assertEqual(m.bpm, 60)
        counter = 0
        for sample in m.samples:
            if list(sample) == [-208900000, -316200000]:
                counter += 1
        self.assertEqual(m.bpm, counter / 10 * 60)

    def test_metronome_init(self):
        test_file_directory = os.path.join('unittest_samples', 'generated_metronome.wav')
        m = Metronome(44100, 10, 60)


