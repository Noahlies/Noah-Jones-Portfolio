import argparse
import csv
import json
from datetime import datetime

from data_acquisition import record_audio
from signal_processing import (
    load_wav,
    compute_fft,
    detect_peak,
    detect_top_peaks,
    doppler_to_velocity,
    smooth_signal,
    calculate_confidence
)
from visualization import plot_spectrum


def parse_args():
    parser = argparse.ArgumentParser(
        description="FFT-based Doppler radar signal processing pipeline"
    )

    parser.add_argument("--input", default="data/test_1000hz.wav")
    parser.add_argument("--output", default="images/fft_output.png")
    parser.add_argument("--source", choices=["file", "mic"], default="file")
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--min-freq", type=float, default=20)
    parser.add_argument("--max-freq", type=float, default=3000)
    parser.add_argument("--display-max", type=float, default=3000)
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=0.3)

    return parser.parse_args()


def process_signal(args, input_path, output_path):
    sample_rate, data = load_wav(input_path)

    ignore_bands = [
        (55, 65),
        (115, 125),
        (175, 185),
        (295, 305),
        (415, 425),
        (535, 545),
    ]

    frequencies, magnitudes = compute_fft(data, sample_rate)
    magnitudes = smooth_signal(magnitudes, window_size=7)

    peak_frequency, peak_magnitude = detect_peak(
        frequencies,
        magnitudes,
        min_freq=args.min_freq,
        max_freq=args.max_freq,
        ignore_bands=ignore_bands
    )

    top_peaks = detect_top_peaks(
        frequencies,
        magnitudes,
        min_freq=args.min_freq,
        max_freq=args.max_freq,
        num_peaks=5,
        min_spacing_hz=20,
        ignore_bands=ignore_bands
    )

    velocity = doppler_to_velocity(peak_frequency)
    confidence = calculate_confidence(peak_magnitude, top_peaks)

    plot_spectrum(
        frequencies,
        magnitudes,
        peak_frequency,
        output_path,
        max_display_freq=args.display_max
    )

    return sample_rate, peak_frequency, peak_magnitude, top_peaks, velocity, confidence


def save_results_json(output_path, args, input_path, sample_rate, peak_frequency, peak_magnitude, top_peaks, velocity, confidence, baseline_frequency, frequency_shift, motion_detected):
    results = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "input_source": args.source,
        "input_file": input_path,
        "sample_rate_hz": sample_rate,
        "search_range_hz": {
            "min": args.min_freq,
            "max": args.max_freq
        },
        "detected_peak": {
            "frequency_hz": round(float(peak_frequency), 2),
            "magnitude": round(float(peak_magnitude), 2)
        },
        "top_detected_frequencies": [
            {
                "rank": rank,
                "frequency_hz": round(float(freq), 2),
                "magnitude": round(float(mag), 2)
            }
            for rank, (freq, mag) in enumerate(top_peaks, start=1)
        ],
        "velocity_estimate_mps": round(float(velocity), 4),
        "confidence_score": round(float(confidence), 2),
        "signal_status": "VALID" if confidence >= 2.0 else "LOW CONFIDENCE / NOISE",
        "baseline_frequency": round(float(baseline_frequency), 2),
        "frequency_shift": round(float(frequency_shift), 2),
        "motion_detected": bool(motion_detected)
    }

    with open(output_path, "w") as file:
        json.dump(results, file, indent=4)

    return output_path


def append_tracking_csv(
    csv_path,
    iteration,
    timestamp,
    peak_frequency,
    filtered_frequency,
    peak_magnitude,
    velocity,
    filtered_velocity,
    confidence,
    baseline_frequency,
    frequency_shift,
    motion_detected
):
    file_exists = False

    try:
        with open(csv_path, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(csv_path, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "iteration",
                "timestamp",
                "peak_frequency_hz",
                "filtered_frequency_hz",
                "peak_magnitude",
                "velocity_mps",
                "filtered_velocity_mps",
                "confidence_score",
                "signal_status",
                "baseline_frequency_hz",
                "frequency_shift_hz",
                "motion_detected"
            ])

        writer.writerow([
            iteration,
            timestamp,
            round(float(peak_frequency), 2),
            round(float(filtered_frequency), 2),
            round(float(peak_magnitude), 2),
            round(float(velocity), 4),
            round(float(filtered_velocity), 4),
            round(float(confidence), 2),
            "VALID" if confidence >= 2.0 else "LOW CONFIDENCE / NOISE",
            round(float(baseline_frequency), 2),
            round(float(frequency_shift), 2),
            bool(motion_detected)
        ])


def print_signal_results(sample_rate, peak_frequency, peak_magnitude, velocity, confidence, filtered_frequency=None, filtered_velocity=None):
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Detected peak frequency: {peak_frequency:.2f} Hz")

    if filtered_frequency is not None:
        print(f"Filtered frequency: {filtered_frequency:.2f} Hz")

    print(f"Peak magnitude: {peak_magnitude:.2f}")
    print(f"Velocity estimate: {velocity:.3f} m/s")

    if filtered_velocity is not None:
        print(f"Filtered velocity estimate: {filtered_velocity:.3f} m/s")

    print(f"Confidence score: {confidence:.2f}")

    if confidence >= 2.0:
        print("Signal status: VALID")
    else:
        print("Signal status: LOW CONFIDENCE / NOISE")



def main():
    args = parse_args()
    baseline_magnitude = None
    baseline_frequency = None


    print("Doppler Radar Signal Processing Pipeline")
    print("----------------------------------------")


    if args.loop:
        if args.source != "mic":
            raise ValueError("Loop mode currently requires --source mic")

        filtered_frequency = None

        for i in range(1, args.iterations + 1):
            record_path = f"data/live_capture_{i}.wav"
            output_path = f"images/fft_loop_{i}.png"

            print(f"\nIteration {i}/{args.iterations}")
            record_audio(record_path, duration=args.duration)

            sample_rate, peak_frequency, peak_magnitude, top_peaks, velocity, confidence = process_signal(
                args,
                record_path,
                output_path
            )

            if baseline_magnitude is None:
                baseline_magnitude = peak_magnitude
                baseline_frequency = peak_frequency
                frequency_shift = 0.0
                motion_detected = False
            else:
                frequency_shift = abs(peak_frequency - baseline_frequency)
                motion_detected = frequency_shift > 15

            if filtered_frequency is None:
                filtered_frequency = peak_frequency
            else:
                filtered_frequency = args.alpha * peak_frequency + (1 - args.alpha) * filtered_frequency

            filtered_velocity = doppler_to_velocity(filtered_frequency)

            print_signal_results(
                sample_rate,
                peak_frequency,
                peak_magnitude,
                velocity,
                confidence,
                filtered_frequency,
                filtered_velocity
            )


            print(f"Baseline magnitude: {baseline_magnitude:.2f}")
            print(f"Baseline frequency: {baseline_frequency:.2f} Hz")
            print(f"Frequency shift: {abs(peak_frequency - baseline_frequency):.2f} Hz")
            print(f"Motion detected: {'YES' if motion_detected else 'NO'}")


            print(f"Saved plot: {output_path}")

            json_path = output_path.replace(".png", ".json")
            save_results_json(
                json_path,
                args,
                record_path,
                sample_rate,
                peak_frequency,
                peak_magnitude,
                top_peaks,
                velocity,
                confidence,
                baseline_frequency,
		frequency_shift,
		motion_detected
            )

            print(f"Saved results: {json_path}")

            timestamp = datetime.now().isoformat(timespec="seconds")
            append_tracking_csv(
                "data/tracking_results.csv",
                i,
                timestamp,
                peak_frequency,
                filtered_frequency,
                peak_magnitude,
                velocity,
                filtered_velocity,
                confidence,
                baseline_frequency,
                frequency_shift,
                motion_detected
            )
            print("Updated tracking CSV: data/tracking_results.csv")

    else:
        if args.source == "mic":
            input_path = "data/live_capture.wav"
            record_audio(input_path, duration=args.duration)
        else:
            input_path = args.input

        sample_rate, peak_frequency, peak_magnitude, top_peaks, velocity, confidence = process_signal(
            args,
            input_path,
            args.output
        )

        print(f"Input source: {args.source}")
        print(f"Input file: {input_path}")
        print(f"Search range: {args.min_freq:.1f} Hz to {args.max_freq:.1f} Hz")

        print_signal_results(
            sample_rate,
            peak_frequency,
            peak_magnitude,
            velocity,
            confidence
        )

        print("Top detected frequencies:")
        for rank, (freq, mag) in enumerate(top_peaks, start=1):
            print(f"  {rank}. {freq:.2f} Hz | magnitude: {mag:.2f}")

        print(f"Saved plot: {args.output}")

        json_path = args.output.replace(".png", ".json")
        save_results_json(
            json_path,
            args,
            input_path,
            sample_rate,
            peak_frequency,
            peak_magnitude,
            top_peaks,
            velocity,
            confidence
        )
        print(f"Saved results: {json_path}")


if __name__ == "__main__":
    main()

