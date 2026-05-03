import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_spectrum(frequencies, magnitudes, peak_frequency, output_path, max_display_freq=3000):
    plt.figure(figsize=(10, 5))
    plt.plot(frequencies, magnitudes)

    peak_magnitude = magnitudes[(abs(frequencies - peak_frequency)).argmin()]
    plt.scatter([peak_frequency], [peak_magnitude])
    plt.annotate(
        f"Peak: {peak_frequency:.1f} Hz",
        xy=(peak_frequency, peak_magnitude),
        xytext=(peak_frequency + 100, peak_magnitude),
        arrowprops=dict(arrowstyle="->")
    )

    plt.xlim(0, max_display_freq)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("FFT Frequency Spectrum")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

