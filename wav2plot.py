from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.io

#data_dir = pjoin(dirname(scipy.io.__file__), 'tests', 'data')

wav_fname = pjoin('Mozart-Alla-turca-from-Piano-Sonata-No.-11-in-A-Major-K.-331.wav')
#print(wav_fname[:-4])
# Load the .wav file contents.
samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[0]}")

length = data.shape[0] / samplerate
print(f"length = {length}s")


# Plot the waveform.
import matplotlib.pyplot as plt
import numpy as np

time = np.linspace(0., length, data.shape[0])
plt.plot(time, data[:,0])#, label="Left channel")
#plt.plot(time, data[:, 1], label="Right channel")
#plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title(f'{wav_fname[:-4]}')

plt.show()
#plt.savefig("{}.png".format(wav_fname[:-4]), dpi=300)
