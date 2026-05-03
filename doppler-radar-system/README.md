# Raspberry Pi Doppler Radar Signal Processing System

## Overview
This project implements an end-to-end Doppler radar signal processing pipeline using a Raspberry Pi and an HB100 microwave radar module. The system captures analog Doppler return signals, performs FFT-based spectral analysis, and detects motion based on frequency shift relative to a baseline.

## System Architecture
- HB100 Doppler Radar Module (10.525 GHz)
- LM358 Analog Amplifier (signal conditioning)
- HiFiBerry ADC (audio digitization, 48 kHz)
- Raspberry Pi 4 (processing + control)
- Python signal processing pipeline

## Processing Pipeline
1. Capture IF signal from radar module
2. Amplify analog signal (LM358)
3. Digitize via ADC (WAV @ 48 kHz)
4. Compute FFT
5. Extract dominant frequency peak
6. Compare against baseline frequency
7. Detect motion via thresholded frequency shift

## Motion Detection Logic
- Baseline frequency established at system start
- Motion detected when:
  frequency_shift > 15 Hz

## Example Results
- Baseline frequency: ~95 Hz
- Motion event: +30–70 Hz shift
- Motion correctly classified using thresholding

## Outputs
- JSON files: structured signal analysis results
- CSV log: time-series tracking data
- Plots:
  - frequency_shift_tracking.png
  - motion_detection_tracking.png
  - fft_loop_*.png

## Key Features
- Real-time signal acquisition
- FFT-based Doppler extraction
- Velocity estimation
- Motion classification
- Data logging (JSON + CSV)
- Visualization pipeline

## Technologies
- Python (NumPy, Matplotlib)
- Raspberry Pi (Linux)
- Analog signal conditioning (LM358)
- Signal processing (FFT)

## Future Improvements
- Hardware filtering to reduce 60 Hz interference
- Higher resolution ADC (I2C-based)
- Real-time streaming visualization
- Multi-target detection
