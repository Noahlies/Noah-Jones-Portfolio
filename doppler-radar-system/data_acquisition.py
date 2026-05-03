import subprocess
import os


def record_audio(output_path, duration=5, device="hw:3,0", sample_rate=48000, channels=2):
    """
    Records audio using arecord and saves to output_path
    """

    command = [
        "arecord",
        "-D", device,
        "-f", "S16_LE",
        "-r", str(sample_rate),
        "-c", str(channels),
        "-d", str(duration),
        output_path
    ]

    print(f"Recording {duration}s of audio to {output_path}...")
    subprocess.run(command, check=True)

    if not os.path.exists(output_path):
        raise RuntimeError("Recording failed: file not created")

    print("Recording complete.")
