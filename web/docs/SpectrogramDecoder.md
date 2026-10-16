# Spectrogram to Audio

Reconstructs an audio signal from a spectrogram image.

Source library: `torchaudio`, `torch`

## Overview

This node is the inverse of the Audio to Spectrogram node. It takes a spectrogram image (or any arbitrary image if you know what you're doing) and reconstructs the original audio waveform using the Griffin-Lim phase reconstruction algorithm. The Griffin-Lim algorithm iteratively estimates the phase information that was lost when the spectrogram was created, allowing reasonable audio reconstruction from magnitude-only data.

## Parameters

- **image**: The input spectrogram image (`IMAGE` type). Must be provided as a forced input.
- **window_size**: (FLOAT) The analysis frame size in milliseconds. Must match the value used when creating the spectrogram. Default: 25.0.
- **hop_size**: (FLOAT) The frame overlap in milliseconds. Must match the original. Default: 15.0.
- **windowing_func**: The windowing function used. Must match the original. Default: **Hanning**.
- **autogain**: (BOOLEAN) When `True`, normalizes the audio to prevent clipping. Default: `True`.
- **max_amp**: (FLOAT) Maximum amplitude scaling factor. Default: 1.0.
- **max_iter**: (INT) The number of Griffin-Lim iterations. More iterations improve phase accuracy but take longer. Default: 32.
- **top_db**: (FLOAT) The minimum dB threshold for magnitude values. Default: 80.0.
- **sampling_rate**: (INT) The sample rate of the output audio in Hz. Default: 22050.
- **gl_momentum**: (FLOAT) The Griffin-Lim momentum parameter. Default: 0.99.
- **scaling_method**: The scaling method used when creating the spectrogram. Must match the original.
    - **Linear**, **Quadratic**, **Logarithmic**, **Logarithmic Mel**.
- **mel_scale**: (BOOLEAN) The Mel scale method used. Must match the original: `htk` (off) or `slaney` (on).
- **channel**: How to extract the audio channel from the image.
    - **colormap**: Uses the colormap-based intensity.
    - **luminance**: Uses ITU-R BT.601 perceptual luminance weights.
    - **channel_red**: Uses the red channel.
    - **channel_green**: Uses the green channel.
    - **channel_blue**: Uses the blue channel.

### Optional Parameters

- **colormap_low**: (STRING) Hex color for low intensity. Default: `#000000`.
- **colormap_mid**: (STRING) Hex color for mid intensity. Default: `#B73779`.
- **colormap_high**: (STRING) Hex color for high intensity. Default: `#FCFDBF`.

## Outputs

- **audio**: The reconstructed audio as an `AUDIO` object, containing a waveform and sample rate.

## Additional Considerations

- Reconstruction quality depends on the number of Griffin-Lim iterations and how closely the parameters match the original encoding.
