import numpy as np
import matplotlib.pyplot as plt
from random import randint
import time


def generate_expected_beat_indexes(framerate, bpm, first_beat_index, number_of_beats):
    return [int(x * framerate * 60 / bpm + first_beat_index) for x in range(0, number_of_beats)]


def detect_peaks(samples, bpm=60, framerate=44100):
    partition_start = 0
    partition_range = int(framerate * (60 / bpm))
    partition_end = int(framerate * (60 / bpm))
    beat_indexes = []
    while partition_start < len(samples):
        # find highest value in partition
        beat_value = max(samples[partition_start:partition_end])
        beat_indexes.append(samples[partition_start:partition_end].index(beat_value) + partition_start)
        partition_start = partition_end
        partition_end = partition_end + partition_range
    return beat_indexes


def generate_samples(frequency=44100, length=10):
    if frequency % 2 == 0:
        values = [0] * int(frequency / 2) + [1] + [0] * int(frequency / 2 - 1)
    values = length * values
    indexes = [x for x in range(0, len(values))]
    print('length: ', len(values))
    return values, indexes


def display_plot(values, indexes):
    plt.plot(indexes, values)
    plt.show()


def generate_random_samples(frequency=44100, bpm=60, length=10):
    random_indexes = []
    for _ in range(0, length):
        random_indexes.append(randint(0, frequency-1))
    values = frequency * length * [0]
    for i in range(0, length):
        values[frequency*i+random_indexes[i]] = 1
    return values, random_indexes


def synchronize(values, indexes, expected_indexes):
    pass


# a, b = generate_samples()

# display_plot(a, b)

random_values, random_indexes = generate_random_samples(44100, 60, 10)


beat_indexes = detect_peaks(random_values, 60, 44100)

expected_beat_indexes = generate_expected_beat_indexes(44100, 60, beat_indexes[0], len(beat_indexes))


print('beat indexes: ', beat_indexes)
# print('beat  values: ', [random_values[index] for index in beat_indexes])
print('expected beat indexes: ', expected_beat_indexes)
print('beats found: ', len(expected_beat_indexes))

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

start_index = beat_indexes[0]
end_index = beat_indexes[1]
frequency = 44100
for i in range(1, len(beat_indexes)-1):
    diff = end_index - start_index
    print('i: ', i, 'diff: ', diff-frequency)
    print('start index: ', start_index, 'end index: ', end_index)
    if diff == 0:
        pass

    elif diff > frequency:
        if (diff - frequency) % 100 == 0:
            min_value = min(random_values[start_index:end_index])
            pop_index = random_values[start_index:end_index].index(min_value)
            for j in range(0, (diff-frequency)/100):
                for k in range(0, 100):
                    random_values.pop(i * frequency + pop_index)
        else:
            min_value = min(random_values[start_index:end_index])
            pop_index = random_values[start_index:end_index].index(min_value)
            for j in range(0, (diff - frequency) % 100):
                random_values.pop(i * frequency + pop_index)

            min_value = min(random_values[start_index:end_index])
            pop_index = random_values[start_index:end_index].index(min_value)
            for j in range(0, int((diff-frequency)/100)):
                for k in range(0, 100):
                    random_values.pop(i * frequency + pop_index)
#         for j in range(0, diff-frequency):
#             min_value = min(random_values[start_index:end_index-j])
#             pop_index = random_values[start_index:end_index-j].index(min_value)
#             random_values.pop(i * frequency + pop_index)

        for j in range(i, len(beat_indexes)):
            beat_indexes[j] = beat_indexes[j] - (diff - frequency)

    elif diff < frequency:
        min_value = min(random_values[start_index:end_index])
        insert_index = random_values[start_index:end_index].index(min_value)

        for j in range(0, frequency-diff):
            random_values.insert(i * frequency + insert_index, 0)

        for j in range(i, len(beat_indexes)):
            beat_indexes[j] += frequency - diff

    start_index = beat_indexes[i]
    try:
        end_index = beat_indexes[i+1]
    except IndexError:
        end_index = start_index + frequency


print('corrected values', detect_peaks(random_values, 60, 44100))
