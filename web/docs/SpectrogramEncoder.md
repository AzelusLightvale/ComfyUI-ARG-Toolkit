# Audio to Spectrogram

Generates a spectrogram image from an audio input.

Source library: `torchaudio`, `torch`

## Overview

This node converts an audio signal into a visual spectrogram. A spectrogram is a visual representation of the spectrum of frequencies in a sound signal as it varies over time. It is widely used in audio analysis, music information retrieval, and speech processing. The node uses the Griffin-Lim algorithm to reconstruct a phase estimate from the magnitude spectrogram.

## Parameters

- **audio**: The input audio data (`AUDIO` type). Must be provided as a forced input from an audio source.
- **window_size**: (FLOAT) The size of each analysis frame in milliseconds. Default: 25.0 ms. Affects frequency resolution.
- **hop_size**: (FLOAT) The overlap between consecutive frames in milliseconds. Default: 15.0 ms. Affects time resolution.
- **windowing_func**: The windowing function to apply to each frame.
    - **Hanning**: The default, a smooth window that reduces spectral leakage.
    - **Bartlett**: A triangular window.
    - **Blackman**: A window with lower sidelobes.
    - **Hamming**: A window similar to Hanning but with different sidelobe characteristics.
- **scaling_method**: How to scale the magnitude values.
    - **Linear**: Raw magnitude values.
    - **Quadratic**: Squared magnitude (power).
    - **Logarithmic**: Logarithmic scale, which emphasizes quieter sounds. Default.
    - **Logarithmic Mel**: Logarithmic scale applied to a Mel-frequency representation.
- **db_norm**: (FLOAT) The silence floor in dB below peak volume. Default: 80.0. Values below this threshold are clipped.
- **cutoff_switch**: (BOOLEAN) When `True`, trims empty vertical space in the spectrogram to save visual space. Default: `True`.

### Optional Parameters

- **colormap_low**: (STRING) Hex color for the lowest intensity. Default: `#000000` (black).
- **colormap_mid**: (STRING) Hex color for mid intensity. Default: `#B73779`.
- **colormap_high**: (STRING) Hex color for highest intensity. Default: `#FCFDBF` (yellow).
- **active_db**: (FLOAT) When `cutoff_switch` is `True`, defines the active dB range. Default: 60.0.
- **mel_scale**: (BOOLEAN) Selects the Mel scale method: `htk` (off) or `slaney` (on).
- **slaney_norm**: (BOOLEAN) When `mel_scale` is `slaney` and Slaney's area normalization is known to be enabled, set this to `True`.

## Outputs

- **spectrogram**: The resulting spectrogram as an `IMAGE` object, suitable for display or further image processing.
