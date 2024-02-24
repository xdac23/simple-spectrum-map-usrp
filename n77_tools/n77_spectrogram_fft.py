import numpy as np
import matplotlib.pyplot as plt

# Step 1: Read the data from the file
root_path = '/home/dan/Workspace/Gnuradio_scripts/Measurements/'
file_path = root_path + 'C1/c1-n77-1.dat'
# file_path = 'c1-n77-1.dat'
data = np.fromfile(file_path, dtype=np.complex64)


# Step 2: Reshape the data into a 2D array (assuming each entry represents IQ samples)

span = 5
num_samples = len(data)
num_samples_per_channel = num_samples // 2
iq_data = np.reshape(data, (2, num_samples_per_channel), order='F')  # Assuming IQ interleaved

# Step 3: Compute the spectrogram
fs = 20e6  # Sample rate 
f_c = 3300e6 + (fs * span)  # Central frequency 
print(f"Span 5 from {f_c-10e6} to {f_c+10e6} MHz")
spectrogram, frequencies, times, _ = plt.specgram(iq_data[0] + 1j * iq_data[1], NFFT=1024, Fs=fs, Fc=f_c)

# Step 4: Adjust extent to display the full time range
duration = num_samples / fs
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram')
plt.colorbar(label='Intensity (dB)')
plt.imshow(spectrogram, extent=[0, duration, frequencies[0], frequencies[-1]], aspect='auto', cmap='viridis')

# Step 5: Compute and plot the FFT over the entire duration with threshold filter
fft_data = np.fft.fft(iq_data[0] + 1j * iq_data[1])
fft_freq = np.fft.fftfreq(len(fft_data), d=1/fs) + f_c
fft_mag = 10*np.log10(np.abs(fft_data) / len(fft_data))

plt.figure()
plt.plot(fft_freq, fft_mag)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Relative Amplitude (dB)')
plt.title('Normalized Mag FFT')
plt.grid(True)

plt.show()
