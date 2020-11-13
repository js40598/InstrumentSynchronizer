import matplotlib.pyplot as plt
from random import randint
import time


class Synchronizer:
    def __init__(self, framerate, bpm, samples):
        self.framerate = framerate
        self.bpm = bpm
        self.samples = samples
        self.length = int(len(samples) / framerate)
        self.number_of_beats = int(framerate * self.length * bpm / 60)
        self.beat_indexes = self.detect_peaks()
        self.synchronized_samples, self.synchronized_indexes = self.synchronize()
        self.is_valid = self.validate()

    def detect_peaks(self):
        # for every beat partition (avg amount of samples per beat)
        partition_start = 0
        partition_range = int(self.framerate * (60 / self.bpm))
        partition_end = int(self.framerate * (60 / self.bpm))
        beat_indexes = []
        while partition_start < len(self.samples) and len(beat_indexes) < self.length:
            # find highest value in partition
            beat_value = max(self.samples[partition_start:partition_end])
            # save it's index as beat index
            beat_indexes.append(self.samples[partition_start:partition_end].index(beat_value) + partition_start)
            partition_start = partition_end
            partition_end = partition_end + partition_range
        return beat_indexes

    def generate_expected_beat_indexes(self):
        return [int(x * self.framerate * 60 / self.bpm + self.beat_indexes[0]) for x in range(0, self.number_of_beats)]

    def synchronize(self):
        start_index = self.beat_indexes[0]
        end_index = self.beat_indexes[1]
        # for every beat
        for i in range(1, len(self.beat_indexes)):
            diff = end_index - start_index
            if diff == 0:
                pass
            # if beat is later than expected
            elif diff > self.framerate:
                # delete where lowest values in blocks of 100 samples to optimize
                # if blocks of 100 will not synchronize beat to exact value delete diff modulo 100
                # #  optimize with slices
                if (diff - self.framerate) % 100 != 0:
                    min_value = min(self.samples[start_index:end_index])
                    pop_index = self.samples[start_index:end_index].index(min_value)
                    for j in range(0, (diff - self.framerate) % 100):
                        self.samples.pop(start_index + pop_index)

                # begin deleting blocks
                min_value = min(self.samples[start_index:end_index])
                pop_index = self.samples[start_index:end_index].index(min_value)
                for j in range(0, int((diff - self.framerate) / 100)):
                    for k in range(0, 100):
                        self.samples.pop(start_index + pop_index)
                # correct values of beats, as list of values is modified
                for j in range(i, len(self.beat_indexes)):
                    self.beat_indexes[j] = self.beat_indexes[j] - (diff - self.framerate)
            # if beat is too early
            elif diff < self.framerate:
                min_value = min(self.samples[start_index:end_index])
                insert_index = self.samples[start_index:end_index].index(min_value)

                # extend lowest values to synchronize
                for j in range(0, self.framerate - diff):
                    self.samples.insert(start_index + insert_index, 0)

                # correct values of beats, as list of values is modified
                for j in range(i, len(self.beat_indexes)):
                    self.beat_indexes[j] += self.framerate - diff

            start_index = self.beat_indexes[i]
            try:
                end_index = self.beat_indexes[i + 1]
            except IndexError:
                end_index = len(self.samples)
        return self.samples, self.beat_indexes

    def validate(self):
        for i in range(0, len(self.beat_indexes)):
            if self.samples[self.beat_indexes[i]] != self.synchronized_samples[self.synchronized_indexes[i]]:
                return False
        return True
