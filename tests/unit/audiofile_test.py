from unittest import TestCase
from instrsyn.AudioFile import AudioFile
from instrsyn.Metronome import Metronome
from scipy.io.wavfile import write
import os


class AudioFileTest(TestCase):
    def setUp(self):
        m = Metronome(44100, 10, 60)
        write(os.path.join('unittest_samples', 'generated_metronome.wav'), m.frequency, m.samples)

    def tearDownClass(self=None):
        os.remove(os.path.join('unittest_samples', 'generated_metronome.flv'))
        os.remove(os.path.join('unittest_samples', 'generated_metronome.ogg'))
#         os.remove(os.path.join('unittest_samples', 'generated_metronome.raw'))
        os.remove(os.path.join('unittest_samples', 'generated_metronome.wav'))
        os.remove(os.path.join('unittest_samples', 'generated_metronome.mp3'))

    def test_create_audio_file(self):
        test_file_directory = os.path.join('unittest_samples', 'generated_metronome.wav')
        a = AudioFile(test_file_directory)
        self.assertEqual(a.directory, test_file_directory)
        self.assertEqual(a.format, 'wav')

    def test_convert_audio_file(self):
        test_file_directory = os.path.join('unittest_samples', 'generated_metronome.wav')
        a = AudioFile(test_file_directory)
        a.convert('flv')
        self.assertEqual(a.format, 'flv')
        a.convert('ogg')
        self.assertEqual(a.format, 'ogg')
        a.convert('mp3')
        self.assertEqual(a.format, 'mp3')
#         a.convert('raw')
#         self.assertEqual(a.format, 'raw')
        print('now')
        a.convert('wav')
        self.assertEqual(a.format, 'wav')


