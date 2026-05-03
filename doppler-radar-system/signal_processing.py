import numpy as np
from scipy.io import wavfile


def load_wav(filepath):
    sample_rate, data = wavfile.read(filepath)

    if len(data.shape) > 1:
        data = data[:, 0]

    return sample_rate, data.astype(float)


def remove_dc_offset(data):
    return data - np.mean(data)


def compute_fft(data, sample_rate):
    import numpy as np

    # Convert to mono if stereo
    if len(data.shape) > 1:
        data = data[:, 0]

    # Apply Hann window
    window = np.hanning(len(data))
    windowed_data = data * window

    # FFT
    fft_result = np.fft.rfft(windowed_data)
    magnitudes = np.abs(fft_result)

    frequencies = np.fft.rfftfreq(len(windowed_data), d=1/sample_rate)

    return frequencies, magnitudes

def apply_ignore_bands(frequencies, magnitudes, ignore_bands):
    filtered_magnitudes = magnitudes.copy()

    for low, high in ignore_bands:
        mask = (frequencies >= low) & (frequencies <= high)
        filtered_magnitudes[mask] = 0

    return filtered_magnitudes


def detect_peak(frequencies, magnitudes, min_freq=20, max_freq=3000, ignore_bands=None):
    if ignore_bands is None:
        ignore_bands = []

    search_magnitudes = apply_ignore_bands(frequencies, magnitudes, ignore_bands)

    mask = (frequencies >= min_freq) & (frequencies <= max_freq)

    search_frequencies = frequencies[mask]
    search_values = search_magnitudes[mask]

    peak_index = search_values.argmax()

    peak_frequency = search_frequencies[peak_index]
    peak_magnitude = search_values[peak_index]

    return peak_frequency, peak_magnitude

def doppler_to_velocity(doppler_frequency, carrier_frequency=10.525e9):
    speed_of_light = 3.0e8
    return (doppler_frequency * speed_of_light) / (2 * carrier_frequency)

def detect_top_peaks(
    frequencies,
    magnitudes,
    min_freq=20,
    max_freq=3000,
    num_peaks=5,
    min_spacing_hz=20,
    ignore_bands=None
):
    if ignore_bands is None:
        ignore_bands = []

    search_magnitudes = apply_ignore_bands(frequencies, magnitudes, ignore_bands)

    mask = (frequencies >= min_freq) & (frequencies <= max_freq)

    search_frequencies = frequencies[mask]
    search_values = search_magnitudes[mask]

    sorted_indices = search_values.argsort()[::-1]

    peaks = []

    for index in sorted_indices:
        frequency = search_frequencies[index]
        magnitude = search_values[index]

        if magnitude <= 0:
            continue

        too_close = False
        for existing_frequency, _ in peaks:
            if abs(frequency - existing_frequency) < min_spacing_hz:
                too_close = True
                break

        if not too_close:
            peaks.append((frequency, magnitude))

        if len(peaks) >= num_peaks:
            break

    return peaks

def smooth_signal(magnitudes, window_size=5):
    import numpy as np

    if window_size < 2:
        return magnitudes

    kernel = np.ones(window_size) / window_size
    smoothed = np.convolve(magnitudes, kernel, mode='same')

    return smoothed


def calculate_confidence(peak_magnitude, top_peaks):
    if len(top_peaks) < 2:
        return 0.0

    second_peak_magnitude = top_peaks[1][1]

    if second_peak_magnitude == 0:
        return 0.0

    return peak_magnitude / second_peak_magnitude


