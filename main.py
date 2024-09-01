import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
def find_time(json_input):
    def calc_amplitude(audio_paths,time):
        signal,sr = librosa.load(audio_paths,sr=None)
        index=int(time*sr)
        return signal[index]
    audio_path_array=json_input["file_paths"]
    audio_path = audio_path_array[0]
    signal, sr = librosa.load(audio_path, sr=None) 

    # normalize
    peak_amplitude = np.max(np.abs(signal))

    normalized_signal = signal / peak_amplitude

    # Parameters for Short time fourier transform
    n_fft = 2048  # Number of samples per frame (window size)
    hop_length = 512  # Number of samples between frames

    # stft
    D = librosa.stft(normalized_signal, n_fft=n_fft, hop_length=hop_length)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    # Calculate the energy 
    energy = np.sum(np.abs(D), axis=0)

    energy_peaks, properties = find_peaks(energy, height=0.6 * np.max(energy))

    peak_times = librosa.frames_to_time(energy_peaks, sr=sr, hop_length=hop_length)

    # Plot the STFT spectrogram for visualization not needed in machine
    # plt.figure(figsize=(14, 6))
    # librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log')
    # plt.colorbar(format='%+2.0f dB')
    # plt.title('STFT Spectrogram')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Frequency (Hz)')

    # # Overlay the detected peaks on the spectrogram
    # for peak_time in peak_times:
    #     plt.axvline(x=peak_time, color='r', linestyle='--', label=f'Gunshot Detected at {peak_time:.2f}s')

    # plt.legend()
    # plt.show()

    # # Plot the energy and detected peaks for visualization
    # plt.figure(figsize=(14, 6))
    # times = librosa.times_like(energy, sr=sr, hop_length=hop_length)
    # plt.plot(times, energy, label='Energy')
    # plt.plot(peak_times, energy[energy_peaks], "x", label='Detected Peaks', color='r')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Energy')
    # plt.title('Energy and Detected Peaks')
    # plt.legend()
    # plt.show()

    max_amplitude = float('-inf')
    max_index = -1

    for i, path in enumerate(audio_path_array):
        current_amplitude = calc_amplitude(path, peak_times[0])
        print(current_amplitude)
        if current_amplitude > max_amplitude:
            max_amplitude = current_amplitude
            max_index = i  

    index_direction_hash={
        0:"NORTH",
        1:"NORTH EAST",
        2:"SOUTH EAST",
        3:"SOUTH",
        4:"SOUTH WEST",
        5:"NORTH WEST"
    }
    print(f"The index of the maximum amplitude element is: {max_index}")
    print(f"The maximum amplitude is: {max_amplitude}")
    print(f"Direction is {index_direction_hash[max_index]}")
    return{
        "Direction":index_direction_hash[max_index],
        "index":max_index
    }