import torch
import numpy as np


class SpectrogramEncoder:
    CATEGORY = "ARG Toolkit/Steganography/Analysis"

    @classmethod
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": (
                    "AUDIO",
                    {
                        "forceInput": True,
                        "tooltip": "The audio file to generate the spectrogram from",
                    },
                ),
                "window_size": ("INT", {"default": 25, "step": 1, "tooltip": "The size of each 'frame' in miliseconds."}),
                "hop_size": ("INT", {"default": 15, "step": 1, "tooltip": "The size of the overlap between each 'frames' in miliseconds"}),
                "windowing_shape": (
                    ["Hanning", "Bartlett", "Blackman", "Hamming"],
                    {
                        "default": "Hanning",
                        "tooltip": "The windowing function to use. Unless you know what you're doing, leave this as default.",
                    },
                ),
                "scaling_method": (
                    ["Linear", "Quadratic", "Logarithmic", "Logarithmic Mel"],
                    {
                        "default": "Logarithmic",
                        "tooltip": "The scaling method used for the spectrogram.",
                    },
                ),
                "db_norm": (
                    "FLOAT",
                    {
                        "default": 80.0,
                        "min": 0.0,
                        "max": 255.0,
                        "tooltip": "The silence floor to the given volume (in negative) below peak volume.",
                    },
                ),
                "cutoff_switch": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Enable/Disable the trimming of empty vertical space in the spectrogram. This is mostly to save space when making spectrograms.",
                    },
                ),
            },
            "optional": {
                "colormap_low": ("STRING", {"default": "#000000", "tooltip": "The color of the lowest point of the spectrogram."}),
                "colormap_mid": ("STRING", {"default": "#B73779", "tooltip": "The color of the middle point of the spectrogram."}),
                "colormap_high": ("STRING", {"default": "#FCFDBF", "tooltip": "The color of the highest point of the spectrogram."}),
                "active_db": (
                    "FLOAT",
                    {
                        "default": 60.0,
                        "min": 0.0,
                        "max": 255.0,
                        "tooltip": "If `cutoff_switch` is set to True, this will define the active dB range from 0 to not cut off.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("spectrogram",)
    FUNCTION = "execute"

    def hex_to_rgb_float(self, hex_str: str) -> tuple[float, float, float]:
        cleaned_hex = hex_str.lstrip("#")
        if len(cleaned_hex) != 6:
            raise ValueError(f"Invalid hex string '{cleaned_hex}'. Must be 6 characters long.")
        return tuple(int(cleaned_hex[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

    def color_mapper(self, matrix: np.ndarray, colormap_low: str, colormap_mid: str, colormap_high: str):
        db_min, db_max = matrix.min(), matrix.max()
        normalized_db = (matrix - db_min) / (db_max - db_min + 1e-10)

        low_r, low_g, low_b = self.hex_to_rgb_float(colormap_low)
        mid_r, mid_g, mid_b = self.hex_to_rgb_float(colormap_mid)
        high_r, high_g, high_b = self.hex_to_rgb_float(colormap_high)

        anchors = [0.0, 0.5, 1.0]

        channel_r = np.interp(normalized_db, anchors, [low_r, mid_r, high_r])
        channel_g = np.interp(normalized_db, anchors, [low_g, mid_g, high_g])
        channel_b = np.interp(normalized_db, anchors, [low_b, mid_b, high_b])

        return np.stack([channel_r, channel_g, channel_b], axis=-1).astype(np.float32)

    def crop_spectrogram_dimensions(self, db_spectrogram: np.ndarray, active_range_db: float) -> np.ndarray:
        peak_val = np.max(db_spectrogram)
        threshold = peak_val - active_range_db

        row_maxes = np.max(db_spectrogram, axis=1)
        active_rows = np.where(row_maxes > threshold)[0]

        col_maxes = np.max(db_spectrogram, axis=0)
        active_cols = np.where(col_maxes > threshold)[0]
        if len(active_rows) == 0 or len(active_cols) == 0:
            return db_spectrogram

        row_cutoff = active_rows[-1] + 1
        col_start = active_cols[0]
        col_end = active_cols[-1] + 1

        return db_spectrogram[:row_cutoff, col_start:col_end]

    def execute(
        self,
        audio,
        window_size,
        hop_size,
        windowing_shape,
        db_norm,
        colormap_low,
        colormap_mid,
        colormap_high,
        cutoff_switch,
        scaling_method,
        active_db,
    ):
        # Defining the base variables for audio
        waveforms = audio["waveform"]
        sampling_rate = audio["sample_rate"]
        audio_np = waveforms.detach().cpu().numpy()
        signal = audio_np[0, 0, :]

        # The framing and windowing process
        raw_frame_length = int(np.round((window_size / 1000.0) * sampling_rate))
        hop_length = int(np.round((hop_size / 1000.0) * sampling_rate))
        frames = np.lib.stride_tricks.sliding_window_view(signal, window_shape=raw_frame_length)[::hop_length]
        windowing_func = getattr(np, windowing_shape.lower().strip())
        windowed_frames = frames * windowing_func(raw_frame_length)

        # Zero-padding the frame to a power of two for FFT performance
        p2_fft = 2 ** int(np.ceil(np.log2(raw_frame_length)))

        # The FFT and spectrogram functions
        complex_spectra = np.fft.rfft(windowed_frames, n=p2_fft, axis=-1)
        magnitude_spectra = np.abs(complex_spectra).T

        # Scaling function
        if scaling_method == "Logarithmic":
            db_spectrogram = 20 * np.log10(magnitude_spectra + 1e-10)
            db_spectrogram_norm = np.maximum(db_spectrogram, np.max(db_spectrogram) - db_norm)
        elif scaling_method == "Linear":
            db_spectrogram_norm = magnitude_spectra
        elif scaling_method == "Quadratic":
            db_spectrogram_norm = magnitude_spectra**2
        elif scaling_method == "Logarithmic Mel":
            freq_num = magnitude_spectra.shape[0]
            nyquist = sampling_rate / 2.0

            mel_max = 2595.0 * np.log10(1.0 + nyquist / 700)
            hz_per_bin = sampling_rate / p2_fft
            mel_num = int(np.round(mel_max / (2595.0 * np.log10(1.0 + hz_per_bin / 700.0))))
            mel_num = int(np.clip(mel_num, 32, p2_fft // 2 + 1))

            mel_points = np.linspace(0, mel_max, mel_num)
            hz_points = 700.0 * (10.0 ** (mel_points / 2595.0) - 1.0)
            freq_indices = np.clip((hz_points / nyquist * (freq_num - 1)).astype(int), 0, freq_num - 1)

            db_spectrogram = magnitude_spectra[freq_indices, :]
            db_spectrogram = 20 * np.log10(magnitude_spectra + 1e-10)
            db_spectrogram_norm = np.maximum(db_spectrogram, np.max(db_spectrogram) - db_norm)
        # Colormap
        if cutoff_switch:
            colormap_db = self.crop_spectrogram_dimensions(db_spectrogram_norm, active_db)
        else:
            colormap_db = db_spectrogram_norm
        rgb_array = self.color_mapper(np.flipud(colormap_db), colormap_low, colormap_mid, colormap_high)
        colormap_tensor = torch.from_numpy(rgb_array).unsqueeze(0)

        return (colormap_tensor,)


NODE_CLASS_MAPPINGS = {
    "SpectrogramEncoder": SpectrogramEncoder,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SpectrogramEncoder": "Audio to Spectrogram",
}
