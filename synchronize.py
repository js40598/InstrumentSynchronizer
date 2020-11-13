import numpy as np
import matplotlib.pyplot as plt
from random import randint
import time

# error = [9142, 51599, 132194, 175471, 207431, 221248, 294734, 320637, 393402, 406803]
# error = [24284, 84777, 123941, 155164, 198087, 262887, 292665, 345826, 359059, 426262]
# error =
# 9142 53242 97342 141442 173402 199359 273742 299645 361942 375343

def generate_expected_beat_indexes(framerate, bpm, first_beat_index, number_of_beats):
    return [int(x * framerate * 60 / bpm + first_beat_index) for x in range(0, number_of_beats)]


def detect_peaks(samples, length, bpm=60, framerate=44100):
    # for every beat partition (avg amount of samples per beat)
    partition_start = 0
    partition_range = int(framerate * (60 / bpm))
    partition_end = int(framerate * (60 / bpm))
    beat_indexes = []
    while partition_start < len(samples) and len(beat_indexes) < length:
#         print('start: ', partition_start)
#         print('end: ', partition_end)
        # find highest value in partition
        beat_value = max(samples[partition_start:partition_end])
        # save it's index as beat index
        beat_indexes.append(samples[partition_start:partition_end].index(beat_value) + partition_start)
        partition_start = partition_end
        partition_end = partition_end + partition_range
    return beat_indexes


# to extend with bpm
def generate_samples(frequency=44100, length=10):
    # insert beats frequently
    if frequency % 2 == 0:
        values = [0] * int(frequency / 2) + [1] + [0] * int(frequency / 2 - 1)
    # clone beat to fit length
    values = length * values
    # beat indexes auto generated
    indexes = [x for x in range(0, len(values))]
    return values, indexes


def display_plot(values, indexes):
    plt.plot(indexes, values)
    plt.show()


def generate_random_samples(frequency=44100, bpm=60, length=10):
    # to correct beats add noise
    random_indexes = []
    for _ in range(0, length):
        random_indexes.append(randint(0, frequency-1))
#     ### testing
#     # if found in testing exact array that makes some errors pass it here, to check it out
#     random_indexes = [9142, 51599, 132194, 175471, 207431, 221248, 294734, 320637, 393402, 406803]
#     for i in range(0, length):
#         random_indexes[i] = random_indexes[i] - frequency * i
#     ### /testing
    values = frequency * length * [0]
    for i in range(0, length):
        values[frequency*i+random_indexes[i]] = 1
    return values, random_indexes


def synchronize(indexes, values, frequency):
    start_index = indexes[0]
    end_index = indexes[1]
    # for every beat
    for i in range(1, len(indexes)):
        diff = end_index - start_index
#         print('i: ', i, 'diff: ', diff-frequency)
#         print('start index: ', start_index, 'end index: ', end_index)
        if diff == 0:
            pass
        # if beat is later than expected
        elif diff > frequency:
            # delete where lowest values in blocks of 100 samples to optimize
            # if blocks of 100 will not synchronize beat to exact value delete diff modulo 100
            if (diff - frequency) % 100 != 0:
                min_value = min(values[start_index:end_index])
                pop_index = values[start_index:end_index].index(min_value)
                for j in range(0, (diff - frequency) % 100):
                    values.pop(start_index + pop_index)

            # begin deleting blocks
            min_value = min(values[start_index:end_index])
            pop_index = values[start_index:end_index].index(min_value)
            for j in range(0, int((diff-frequency)/100)):
                for k in range(0, 100):
                    values.pop(start_index + pop_index)
    #         for j in range(0, diff-frequency):
    #             min_value = min(random_values[start_index:end_index-j])
    #             pop_index = random_values[start_index:end_index-j].index(min_value)
    #             random_values.pop(i * frequency + pop_index)
            # correct values of beats, as list of values is modified
            for j in range(i, len(indexes)):
                indexes[j] = indexes[j] - (diff - frequency)
        # if beat is too early
        elif diff < frequency:
            min_value = min(values[start_index:end_index])
            insert_index = values[start_index:end_index].index(min_value)

            # extend lowest values to synchronize
            for j in range(0, frequency-diff):
                values.insert(start_index + insert_index, 0)

            # correct values of beats, as list of values is modified
            for j in range(i, len(indexes)):
                indexes[j] += frequency - diff

        start_index = indexes[i]
        try:
            end_index = indexes[i+1]
        except IndexError:
            end_index = len(values)
    return values, indexes

counter = 0
fcounter = 0
times = []

# brute force testing
while True:
    start_time = time.time()

    # a, b = generate_samples()

    # display_plot(a, b)

    random_values, random_indexes = generate_random_samples(44100, 60, 10)

    beat_indexes = detect_peaks(random_values, 10, 60, 44100)

    expected_beat_indexes = generate_expected_beat_indexes(44100, 60, beat_indexes[0], len(beat_indexes))


    # print('beat indexes         : ', beat_indexes)
    # # print('beat  values: ', [random_values[index] for index in beat_indexes])
    # print('expected beat indexes: ', expected_beat_indexes)
    # print('beats found: ', len(expected_beat_indexes))

    # synchronize(values, indexes, expected_indexes, frequency)
    # frequency = 44100
    # start_index = 0
    # end_index = beat_indexes[0]
    # for i in range(0, len(beat_indexes)):
    #     diff = beat_indexes[i] - expected_beat_indexes[i]
    #     if diff == 0:
    #         pass
    #     elif diff < 0:
    #         min_value = min(random_values[start_index:end_index])
    #         insert_index = random_values[start_index:end_index].index(min_value)
    #         for _ in range(0, abs(diff)):
    #             random_values.insert(i*frequency+insert_index, min_value)
    #     elif diff > 0:
    #         diff = beat_indexes[i] - expected_beat_indexes[i]
    #         for _ in range(0, diff):
    # #            min_value = min(random_values[start_index:end_index])
    #             pop_index = random_values[start_index:end_index].index(0)
    #             random_values.pop(i*frequency+pop_index)
    #     start_index = expected_beat_indexes[i]
    #     try:
    #         end_index = expected_beat_indexes[i+1]
    #     except IndexError:
    #         end_index = len(random_values)
    # # backwards
    # start_index = beat_indexes[-2]
    # end_index = beat_indexes[-1]
    # for i in range(2, len(beat_indexes)):
    #     diff = beat_indexes[-i] - expected_beat_indexes[-i]
    #     print('i: ', i, 'diff: ', diff)
    #     print('start index: ', start_index, 'end index: ', end_index)
    #     if diff == 0:
    #         pass
    #     elif diff < 0:
    #         min_value = min(random_values[start_index:end_index])
    #         insert_index = random_values[start_index:end_index].index(min_value)
    #         for _ in range(0, abs(diff)):
    #             random_values.insert(i*frequency+insert_index, min_value)
    #     elif diff > 0:
    #         diff = beat_indexes[i] - expected_beat_indexes[i]
    #         for _ in range(0, diff):
    # #            min_value = min(random_values[start_index:end_index])
    #             pop_index = random_values[start_index:end_index].index(0)
    #             random_values.pop(i*frequency+pop_index)
    #     start_index = beat_indexes[-i-1]
    #     try:
    #         end_index = beat_indexes[-i]
    #     except IndexError:
    #         end_index = len(random_values)

    random_values_synchronized, random_indexes_synchronized = synchronize(beat_indexes, random_values, 44100)
    # print('expected beat indexes: ', expected_beat_indexes)
    # print('synchronized indexes : ', random_indexes_synchronized)
    # print('corrected values: ', detect_peaks(random_values_synchronized, 10, 60, 44100))
    v1 = 1
    v2 = 1
    if random_indexes_synchronized != expected_beat_indexes:
        print(beat_indexes)
        print('run failed')
        v1 = 0

    for index in random_indexes_synchronized:
        if random_values_synchronized[index] != 1:
            print('wrong value, run failed')
            print(beat_indexes)
            v2 = 0

    if v1 == 1 and v2 == 1:
        counter += 1
    else:
        fcounter += 1
    times.append((time.time() - start_time))

    print('runs passed: ', counter)
    print('runs failed: ', fcounter)
    print('average single run time: ', round(sum(times)/len(times), 2), 'seconds')

# runs passed:  259
# runs failed:  0
# average single run time:  12.28 seconds
