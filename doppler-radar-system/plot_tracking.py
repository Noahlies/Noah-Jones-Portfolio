import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


CSV_PATH = "data/tracking_results.csv"

FREQ_OUTPUT = "images/frequency_tracking.png"
VEL_OUTPUT = "images/velocity_tracking.png"
CONF_OUTPUT = "images/confidence_tracking.png"
SHIFT_OUTPUT = "images/frequency_shift_tracking.png"
MOTION_OUTPUT = "images/motion_detection_tracking.png"


def load_tracking_data(csv_path):
    iterations = []
    raw_frequencies = []
    filtered_frequencies = []
    raw_velocities = []
    filtered_velocities = []
    confidence_scores = []
    frequency_shifts = []
    motion_detected = []

    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            iterations.append(int(row["iteration"]))
            raw_frequencies.append(float(row["peak_frequency_hz"]))
            filtered_frequencies.append(float(row["filtered_frequency_hz"]))
            raw_velocities.append(float(row["velocity_mps"]))
            filtered_velocities.append(float(row["filtered_velocity_mps"]))
            confidence_scores.append(float(row["confidence_score"]))
            frequency_shifts.append(float(row["frequency_shift_hz"]))
            motion_detected.append(1 if row["motion_detected"] == "True" else 0)

    return (
        iterations,
        raw_frequencies,
        filtered_frequencies,
        raw_velocities,
        filtered_velocities,
        confidence_scores,
        frequency_shifts,
        motion_detected
    )


def plot_frequency(iterations, raw_frequencies, filtered_frequencies):
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, raw_frequencies, marker="o", label="Raw frequency")
    plt.plot(iterations, filtered_frequencies, marker="o", label="Filtered frequency")
    plt.xlabel("Iteration")
    plt.ylabel("Frequency (Hz)")
    plt.title("Raw vs Filtered Peak Frequency Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FREQ_OUTPUT, dpi=150)
    plt.close()


def plot_velocity(iterations, raw_velocities, filtered_velocities):
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, raw_velocities, marker="o", label="Raw velocity")
    plt.plot(iterations, filtered_velocities, marker="o", label="Filtered velocity")
    plt.xlabel("Iteration")
    plt.ylabel("Velocity Estimate (m/s)")
    plt.title("Raw vs Filtered Velocity Estimate Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(VEL_OUTPUT, dpi=150)
    plt.close()


def plot_confidence(iterations, confidence_scores):
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, confidence_scores, marker="o")
    plt.axhline(y=2.0, linestyle="--", label="SNR confidence threshold")
    plt.xlabel("Iteration")
    plt.ylabel("Confidence Score")
    plt.title("Signal Confidence Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(CONF_OUTPUT, dpi=150)
    plt.close()


def plot_frequency_shift(iterations, frequency_shifts):
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, frequency_shifts, marker="o")
    plt.axhline(y=15.0, linestyle="--", label="Motion threshold")
    plt.xlabel("Iteration")
    plt.ylabel("Frequency Shift from Baseline (Hz)")
    plt.title("Doppler Frequency Shift Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(SHIFT_OUTPUT, dpi=150)
    plt.close()


def plot_motion_detection(iterations, motion_detected):
    plt.figure(figsize=(10, 5))
    plt.step(iterations, motion_detected, where="mid")
    plt.yticks([0, 1], ["No motion", "Motion"])
    plt.xlabel("Iteration")
    plt.ylabel("Motion Detection")
    plt.title("Motion Detection Decision Over Time")
    plt.tight_layout()
    plt.savefig(MOTION_OUTPUT, dpi=150)
    plt.close()


def main():
    (
        iterations,
        raw_frequencies,
        filtered_frequencies,
        raw_velocities,
        filtered_velocities,
        confidence_scores,
        frequency_shifts,
        motion_detected
    ) = load_tracking_data(CSV_PATH)

    plot_frequency(iterations, raw_frequencies, filtered_frequencies)
    plot_velocity(iterations, raw_velocities, filtered_velocities)
    plot_confidence(iterations, confidence_scores)
    plot_frequency_shift(iterations, frequency_shifts)
    plot_motion_detection(iterations, motion_detected)

    print(f"Saved frequency tracking plot: {FREQ_OUTPUT}")
    print(f"Saved velocity tracking plot: {VEL_OUTPUT}")
    print(f"Saved confidence tracking plot: {CONF_OUTPUT}")
    print(f"Saved frequency shift plot: {SHIFT_OUTPUT}")
    print(f"Saved motion detection plot: {MOTION_OUTPUT}")


if __name__ == "__main__":
    main()
