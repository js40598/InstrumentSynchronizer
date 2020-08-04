from unittest import TestCase
from instrsyn.AudioFile import AudioFile
import os
import definitions


class AudioFileTest(TestCase):
    def test_create_audio_file(self):
        test_file_directory = 'samples/testsamples/45.mp3'
        a = AudioFile(test_file_directory)
        self.assertEqual(a.directory, test_file_directory)
        self.assertEqual(a.format, 'mp3')

    def test_convert_audio_file(self):
        test_file_directory = os.path.join('unittest_samples', '45.mp3')
        a = AudioFile(test_file_directory)
        a.convert('flv')
        self.assertEqual(a.format, 'flv')
        a.convert('ogg')
        self.assertEqual(a.format, 'ogg')
        a.convert('mp3')
        self.assertEqual(a.format, 'mp3')
#        a.convert('raw')
#        self.assertEqual(a.format, 'raw')
        a.convert('wav')
        self.assertEqual(a.format, 'wav')
        os.remove(os.path.join('unittest_samples', '45.flv'))
        os.remove(os.path.join('unittest_samples', '45.ogg'))
#        os.remove(os.path.join('unittest_samples', '45.raw'))
        os.remove(os.path.join('unittest_samples', '45.wav'))


