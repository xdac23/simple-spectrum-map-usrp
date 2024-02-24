import numpy as np
import matplotlib.pyplot as plt

# Step 1: Read the data from the file
file_path = 'c4-lora-short.dat'
data = np.fromfile(file_path, dtype=np.complex64)

# Step 2: Reshape the data into a 2D array (assuming each entry represents IQ samples)
num_samples = len(data)
num_samples_per_channel = num_samples // 2
iq_data = np.reshape(data, (2, num_samples_per_channel), order='F')  # Assuming IQ interleaved

# Step 3: Compute the spectrogram
fs = 10e6  # Sample rate (10 MHz)
f_c = 868e6  # Central frequency (868 MHz)
spectrogram, frequencies, times, _ = plt.specgram(iq_data[0] + 1j * iq_data[1], NFFT=1024, Fs=fs, Fc=f_c)

# Normalize the spectrogram
spectrogram_normalized = 10 * np.log10(spectrogram / np.max(spectrogram))  # Normalize to the maximum power

# Step 4: Create a 3D plot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Create grid for plotting
T, F = np.meshgrid(times, frequencies)

# Plot 3D surface
surf = ax.plot_surface(T, F, spectrogram_normalized, cmap='viridis', linewidth=0, antialiased=False)

# Set labels and title
ax.set_xlabel('Time (s)')
ax.set_ylabel('Frequency (Hz)')
ax.set_zlabel('Relative Power')
ax.set_title('3D Spectrum (Normalized)')

# Add colorbar
fig.colorbar(surf, ax=ax, label='Power (dB)')

plt.show()
