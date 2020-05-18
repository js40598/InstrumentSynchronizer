from scipy.io.wavfile import read
import matplotlib.pyplot as plt

# read audio samples
input_data = read("samples/sax.wav")
audio = input_data[1]
# plot the first 1024 samples
print(len(audio))
plt.plot(audio[0:44100*2])
counter = 0
for a in audio[0: 44100]:
    if a[0] > 0 or a[1] > 0:
        print(a)
        counter += 1
print(counter)
# label the axes
plt.ylabel("Amplitude")
plt.xlabel("Time")
# set the title
plt.title("Sample Wav")
# display the plot
plt.show()