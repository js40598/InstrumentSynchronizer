import matplotlib.pyplot as plt
from random import randint
import time
# to extend with bpm
def generate_samples(frequency=44100, length=10):
    # insert beats frequently
    if frequency % 2 == 0:
        values = [0] * int(frequency / 2) + [1] + [0] * int(frequency / 2 - 1)
    else:
        values = [0] * int(frequency / 2) + [1] + [0] * int(frequency / 2)
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


def start_time():
    return time.time()


def show_time(start_time):
    return time.time() - start_time
