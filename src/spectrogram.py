import torch
import torchaudio.transforms as torch_trans
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
                "window_size": ("FLOAT", {"default": 25.000, "min": 0.001, "max": 100000.000, "step": 0.0011, "tooltip": "The size of each 'frame' in miliseconds."}),
                "hop_size": ("FLOAT", {"default": 15.000, "min": 0.001, "max": 100000.000, "step": 0.001, "tooltip": "The size of the overlap between each 'frames' in miliseconds"}),
                "windowing_func": (
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
        window_size: int,
        hop_size: int,
        windowing_func: str,
        db_norm: float,
        colormap_low: str,
        colormap_mid: str,
        colormap_high: str,
        cutoff_switch: bool,
        scaling_method: str,
        active_db: float,
    ):
        # Defining the base variables for audio
        waveforms = audio["waveform"]
        sampling_rate = audio["sample_rate"]
        audio_np = waveforms.detach().cpu().numpy()
        signal = audio_np[0, 0, :]

        # The framing and windowing process
        raw_frame_length = int(np.round((window_size / 1000.0) * sampling_rate))
        hop_length = int(np.round((hop_size / 1000.0) * sampling_rate))
        frames = np.lib.stride_tricks.sliding_window_view(signal, window_shape=raw_frame_length, axis=-1)[::hop_length]
        windowing_func = getattr(np, windowing_func.lower().strip())
        windowed_frames = frames * windowing_func(raw_frame_length)

        # Zero-padding the frame to a power of two for FFT performance
        p2_fft = 2 ** int(np.ceil(np.log2(raw_frame_length)))

        # The FFT and spectrogram functions
        complex_spectra = np.fft.rfft(windowed_frames, n=p2_fft)
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

            mel_points = np.linspace(0, mel_max, mel_num +2)
            hz_points = 700.0 * (10.0 ** (mel_points / 2595.0) - 1.0)
            freq_indices = (hz_points / nyquist) * (freq_num - 1)

            mel_matrix = np.zeros((mel_num, freq_num), dtype=np.float32)
            for i in range(1, mel_num + 1):
                left, center, right = freq_indices[i - 1], freq_indices[i], freq_indices[i + 1]
                bins = np.arange(int(np.floor(left)), int(np.ceil(right)) + 1)
                bins = bins[(bins >= 0) & (bins < freq_num)]

                up_mask = (bins >= left) & (bins <= center)
                down_mask = (bins > center) & (bins <= right)

                if center > left:
                    mel_matrix[i - 1, bins[up_mask]] = (bins[up_mask] - left) / (center - left)
                if right > center:
                    mel_matrix[i - 1, bins[down_mask]] = (right - bins[down_mask]) / (right - center)

            db_spectrogram = np.dot(mel_matrix, magnitude_spectra)
            db_spectrogram = 20 * np.log10(db_spectrogram + 1e-10)
            db_spectrogram_norm = np.maximum(db_spectrogram, np.max(db_spectrogram) - db_norm)

        # Colormap
        if cutoff_switch:
            colormap_db = self.crop_spectrogram_dimensions(db_spectrogram_norm, active_db)
        else:
            colormap_db = db_spectrogram_norm
        rgb_array = self.color_mapper(np.flipud(colormap_db), colormap_low, colormap_mid, colormap_high)
        colormap_tensor = torch.from_numpy(rgb_array).unsqueeze(0)

        return (colormap_tensor,)


class SpectrogramDecoder:
    CATEGORY = "ARG Toolkit/Steganography/Analysis"

    @classmethod
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"forceInput": True,"tooltip": "The spectrogram image to decode into audio."}),
                "image_type": (
                    "BOOLEAN",
                    {
                        "label_on": "Spectrogram",
                        "label_off": "Image",
                        "default": True,
                        "tooltip": "The type of image fed into the model. `Spectrogram` flips the image to correct for orientation, `Image` does not.",
                    }
                ),
                "channel": (
                    ["colormap", "channel_red", "channel_green", "channel_blue", "luminance"],
                    {
                        "default": "luminance",
                        "tooltip": "The color channel used to collapse and deconstruct the image. For spectrograms with a known colormap, use `colormap`, otherwise use `luminance` or any of the RGB channels.",
                    }
                ),
                "window_size": ("FLOAT", {"default": 25.000, "min": 0.001, "max": 100000.000, "step": 0.0011, "tooltip": "The size of each 'frame' in miliseconds."}),
                "hop_size": ("FLOAT", {"default": 15.000, "min": 0.001, "max": 100000.000, "step": 0.001, "tooltip": "The size of the overlap between each 'frames' in miliseconds"}),
                "windowing_func": (
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
                    }
                ),
                "autogain": (
                    "BOOLEAN", 
                    {
                        "tooltip": "For Linear and Quadratic scaling method, dynamically scale the amplitude based on the peak. If disabled, use `max_amp` to define it instead. If used with Logarithmic Mel scaling, will enable area normalization if used with `mel_scale=slaney`.",
                    }
                ),
                "top_db": (
                    "FLOAT",
                    {
                        "default": 80.0,
                        "min": 0.0,
                        "max": 255.0,
                        "tooltip": "The dynamic range (in negative dB) to scale against for both Logarithmic scaling methods.",
                    },
                ),
                "sampling_rate": ("INT", {"max": 384000, "min":100, "default": 44100, "step": 1, "tooltip": "The target sample rate for the audio file."}),
                "max_iter": ("INT", {"min": 1, "max": 1024, "default": 32, "tooltip": "Maximum iteration to run the Griffin-Lim algorithm for."}),
                "gl_momentum": ("FLOAT", {"min": 0.00, "max": 2.00, "default": 0.99, "step": 0.01, "tooltip": "For use with Fast Griffin-Lim. 0 disables Fast Griffin-Lim."})
            },
            "optional": {
                "colormap_low": ("STRING", {"default": "#000000", "tooltip": "The color of the lowest point of the spectrogram.",}),
                "colormap_mid": ("STRING", {"default": "#B73779", "tooltip": "The color of the middle point of the spectrogram.",}),
                "colormap_high": ("STRING", {"default": "#FCFDBF", "tooltip": "The color of the highest point of the spectrogram.",}),
                "max_amp": ("FLOAT", {"step": 0.1, "min": 0.0, "max": 1.0, "default": 1.0, "tooltip": "If `autogain is disabled, this defines the maximum amplitude to scale with in Linear and Quadratic scaling.",}),
                "mel_scale": ("BOOLEAN", {"label_off": "htk", "label_on": "slaney", "default": False, "tooltip": "Mel scaling method to use."}),
            },
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "execute"

    def colormap_collapse(self, image, colormap_low, colormap_mid, colormap_high):
        c1 = torch.tensor([int(colormap_low[i : i + 2], 16) for i in (1, 3, 5)], dtype=torch.float32) / 255.0
        c2 = torch.tensor([int(colormap_mid[i : i + 2], 16) for i in (1, 3, 5)], dtype=torch.float32) / 255.0
        c3 = torch.tensor([int(colormap_high[i : i + 2], 16) for i in (1, 3, 5)], dtype=torch.float32) / 255.0

        vec12, vec23 = c2 - c1, c3 - c2
        len12_sq, len23_sq = torch.sum(vec12**2), torch.sum(vec23**2)

        diff1 = image - c1
        t1 = torch.clamp(torch.sum(diff1 * vec12, dim=-1) / (len12_sq + 1e-8), 0.0, 1.0) * 0.5

        diff2 = image - c2
        t2 = torch.clamp(torch.sum(diff2 * vec23, dim=-1) / (len23_sq + 1e-8), 0.0, 1.0) * 0.5 + 0.5

        dist1 = torch.norm(image - (c1 + t1.unsqueeze(-1) / 0.5 * vec12), dim=-1)
        dist2 = torch.norm(image - (c2 + (t2.unsqueeze(-1) - 0.5) / 0.5 * vec23), dim=-1)

        norm_val = torch.where(dist1 < dist2, t1, t2)
        return norm_val

    def execute(self, image, image_type, window_size, hop_size, windowing_func, autogain, max_amp, max_iter, top_db, sampling_rate, gl_momentum, scaling_method, mel_scale, channel, colormap_low, colormap_mid, colormap_high):
        # Rotate the image in case it's a spectrogram
        if image_type:
            image = torch.flip(image, dims=[1])
        elif not image_type:
            image = image

        raw_frame_length = int(np.round((window_size / 1000.0) * sampling_rate))
        hop_length = int(np.round((hop_size / 1000.0) * sampling_rate))
        p2_fft = 2 ** int(np.ceil(np.log2(raw_frame_length)))
        n_stft = (p2_fft//2)+1


        # Channel collapse
        if channel == "colormap":
            norm = self.colormap_collapse(image, colormap_low, colormap_mid, colormap_high)
        elif channel == "luminance":
            weights = torch.tensor([0.299, 0.587, 0.114]) # Luminance value based on ITU-R BT.601 perceptual weights.
            norm = torch.sum(image * weights, dim=-1)
        elif channel == "channel_red":
            norm = image[..., 0]
        elif channel == "channel_green":
            norm = image[..., 1]
        elif channel == "channel_blue":
            norm = image[..., 2]

        # Scaling the array
        if scaling_method in ["Linear", "Quadratic"]:
            if scaling_method == "Linear":
                image_peak = torch.max(norm)
            elif scaling_method == "Quadratic":
                image_peak = torch.max(norm**2)

            if autogain and image_peak>0:
                magnitude = (norm/image_peak) * 1.0
            else:
                magnitude = norm * max_amp
        elif scaling_method == "Logarithmic":
            log_mag = torch.pow(10.0, ((norm * top_db) - top_db)/20)
            magnitude = torch.clamp(log_mag, min=0.0)
        elif scaling_method == "Logarithmic Mel":
            log_mag = torch.pow(10.0, ((norm * top_db) - top_db)/20)
            lin_mag = torch.clamp(log_mag, min=0.0)
            inverse_scale = torch_trans.InverseMelScale(n_stft=n_stft, n_mels=norm.shape[1], sample_rate=sampling_rate, f_min=0.0, f_max=sampling_rate/2, norm="slaney" if autogain==True else None, mel_scale="htk" if mel_scale==False else "slaney")
            magnitude = inverse_scale(lin_mag)

        # Griffin-Lim
        windowing = {
            "Hanning": torch.hann_window,
            "Hamming": torch.hamming_window,
            "Blackman": torch.blackman_window,
            "Bartlett": torch.bartlett_window,
        }
        windowing_func = windowing.get(windowing_func)  

        griffin_lim = torch_trans.GriffinLim(n_fft=p2_fft, win_length=raw_frame_length, hop_length=hop_length, window_fn=windowing_func, n_iter=max_iter, momentum=gl_momentum, power=1.0)
        waveform = griffin_lim(magnitude)
        max_val = torch.max(torch.abs(waveform))
        if max_val > 1e-8 :
            waveform = waveform / max_val
        waveform = waveform.unsqueeze(0).cpu()
        final_audio = {"waveform": waveform, "sample_rate": sampling_rate}

        return (final_audio,)


NODE_CLASS_MAPPINGS = {
    "SpectrogramEncoder": SpectrogramEncoder,
    "SpectrogramDecoder": SpectrogramDecoder,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SpectrogramEncoder": "Audio to Spectrogram",
    "SpectrogramDecoder": "Spectrogram to Audio",
}
