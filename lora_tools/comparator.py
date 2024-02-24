import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['agg.path.chunksize'] = 10000  # or any value greater than 100

# Function to compute FFT for a given file
def compute_fft(file_path):
    # Read the data from the file
    data = np.fromfile(file_path, dtype=np.complex64)

    # Reshape the data into a 2D array (assuming each entry represents IQ samples)
    num_samples = len(data)
    num_samples_per_channel = num_samples // 2
    iq_data = np.reshape(data, (2, num_samples_per_channel), order='F')  # Assuming IQ interleaved

    # Compute the FFT over the entire duration with threshold filter
    fs = 10e6  # Sample rate (10 MHz)
    f_c = 868e6  # Central frequency (868 MHz)
    fft_data = np.fft.fft(iq_data[0] + 1j * iq_data[1])
    fft_freq = np.fft.fftfreq(len(fft_data), d=1/fs) + f_c

    # Shift FFT frequencies to have central frequency at 868 MHz
    fft_freq_shifted = np.fft.fftshift(fft_freq) 
    fft_mag = np.fft.fftshift(10*np.log10(np.abs(fft_data) / len(fft_data)))

    return fft_freq_shifted, fft_mag

# Files to process
file_paths = ['c1-lora-short.dat', 'c2-lora-short.dat', 'c3-lora-short.dat', 'c4-lora-short.dat']
labels = ['C1', 'C2', 'C3', 'C4']

# Plot FFT for each file
plt.figure(figsize=(10, 6))
for file_path, label in zip(file_paths, labels):
    fft_freq, fft_mag = compute_fft(file_path)
    plt.plot(fft_freq, fft_mag, label=label)

# Apply threshold filter
threshold = -60  # Threshold value in dB
plt.ylim(threshold, None)  # Adjust y-axis limit to the threshold
plt.xlabel('Frequency (Hz)')
plt.ylabel('Relative amplitude (dB)')
plt.title('FFT Normalized - Threshold: {} dB)'.format(threshold))
plt.grid(True)
plt.legend()
plt.show()
