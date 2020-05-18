import os
from pydub import AudioSegment


source = 'samples/sax.mp3'

class AudioFile():
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
        exfrom.export(exto, format = goto)
        print('Audio succesfully converted from {} to {}'.format(self.format, goto))
        self.format = goto



a = AudioFile(source)
a.convert('wav')##options: mp3, wav, flv, ogg, raw
