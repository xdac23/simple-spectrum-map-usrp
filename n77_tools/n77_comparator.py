import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['agg.path.chunksize'] = 10000  # or any value greater than 100

# Function to compute FFT for a given file
def compute_fft(file_path, span):
    # Read the data from the file
    data = np.fromfile(file_path, dtype=np.complex64)
    # Reshape the data into a 2D array (assuming each entry represents IQ samples)   
    num_samples = len(data)
    num_samples_per_channel = num_samples // 2
    iq_data = np.reshape(data, (2, num_samples_per_channel), order='F')  # Assuming IQ interleaved

    # Compute the FFT over the entire duration with threshold filter
    fs = 20e6  # Sample rate 
    f_c = 3300e6 + (fs * span)  # Central frequency     
    fft_data = np.fft.fft(iq_data[0] + 1j * iq_data[1])
    fft_freq = np.fft.fftfreq(len(fft_data), d=1/fs) + f_c

    # Shift FFT frequencies to have central frequency at 868 MHz
    fft_freq_shifted = np.fft.fftshift(fft_freq) 
    fft_mag = np.fft.fftshift(10*np.log10(np.abs(fft_data) / len(fft_data)))

    return fft_freq_shifted, fft_mag

# Files to process
root_path = '/home/dan/Workspace/Gnuradio_scripts/Measurements/'
file_paths = [root_path + 'C1/c1-n77-'+ str(span) +'.dat', root_path + 'C2/c2-n77-'+ str(span) +'.dat',root_path + 'C3/c3-n77-'+ str(span) +'.dat', root_path + 'C3/c3-n77-'+ str(span) +'.dat']
labels = ['C1', 'C2', 'C3', 'C4']

# Range of spans
span_range = range(1, 3)

# Iterate over the span range
for span in span_range:
    # Plot FFT for each file
    plt.figure(figsize=(12, 8))
    for file_path, label in zip(file_paths, labels):
        fft_freq, fft_mag = compute_fft(file_path, span)
        plt.plot(fft_freq, fft_mag, label=label)

    # Apply threshold filter
    threshold = -58  # Threshold value in dB
    plt.ylim(threshold, None)  # Adjust y-axis limit to the threshold
    plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Relative amplitude (dB)')
    plt.title('FFT Normalized - Threshold: {}dB - Span {}'.format(threshold, span))
    plt.grid(False)
    # Hide frame and y-axis labels
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().tick_params(axis='y', which='both', left=False, labelleft=False)  # Hide y-axis ticks and labels

    # Show only x-axis ticks and labels
    plt.tick_params(axis='x', which='both', bottom=True, labelbottom=True)

    # Save the plot to a file
    plt.savefig('fft_plot_span_{}.png'.format(span))

    # Close the plot to free memory
    plt.close()
