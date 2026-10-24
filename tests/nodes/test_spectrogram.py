from src.spectrogram import SpectrogramEncoder, SpectrogramDecoder
import torch
import numpy as np


# Test suite for spectrogram.py
class TestSpectrogramEncoder:
    def setup_method(self):
        self.encoder = SpectrogramEncoder()

    # Test hex_to_rgb_float helper method
    def test_hex_to_rgb_float_valid(self):
        # Test with valid hex colors
        result = self.encoder.hex_to_rgb_float("#FF0000")
        assert result == (1.0, 0.0, 0.0)

        result = self.encoder.hex_to_rgb_float("#00FF00")
        assert result == (0.0, 1.0, 0.0)

        result = self.encoder.hex_to_rgb_float("#0000FF")
        assert result == (0.0, 0.0, 1.0)

        result = self.encoder.hex_to_rgb_float("#FFFFFF")
        assert result == (1.0, 1.0, 1.0)

        result = self.encoder.hex_to_rgb_float("#000000")
        assert result == (0.0, 0.0, 0.0)

    def test_hex_to_rgb_float_invalid(self):
        # Test with invalid hex colors
        try:
            self.encoder.hex_to_rgb_float("#FF")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

        try:
            self.encoder.hex_to_rgb_float("#GGGGGG")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

        try:
            self.encoder.hex_to_rgb_float("#FF000000")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    # Test color_mapper helper method
    def test_color_mapper_basic(self):
        # Create a simple test matrix
        matrix = np.array([[0.0, 0.5, 1.0], [0.2, 0.7, 0.9]])

        # Test with default colormap
        result = self.encoder.color_mapper(
            matrix,
            "#000000",  # low
            "#B73779",  # mid
            "#FCFDBF",  # high
        )

        # Check shape and type
        assert result.shape == (2, 3, 3)  # height, width, RGB
        assert result.dtype == np.float32

        # Check that values are normalized between 0 and 1
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    # Test crop_spectrogram_dimensions helper method
    def test_crop_spectrogram_dimensions_basic(self):
        # Create a test spectrogram with some active and inactive regions
        db_spectrogram = np.array(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, -20.0, -15.0, -10.0, 0.0],
                [0.0, -30.0, -25.0, -20.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        )

        # Test with active_range_db = 20 (should cut off values below -40)
        result = self.encoder.crop_spectrogram_dimensions(db_spectrogram, 20.0)

        # The result should be cropped to the active region
        # This is a basic test - the exact shape depends on the threshold logic
        assert result.shape[0] <= db_spectrogram.shape[0]
        assert result.shape[1] <= db_spectrogram.shape[1]

    def test_crop_spectrogram_dimensions_empty(self):
        # Test with all values below threshold
        db_spectrogram = np.array(
            [
                [-50.0, -60.0, -70.0],
                [-55.0, -65.0, -75.0],
            ]
        )

        result = self.encoder.crop_spectrogram_dimensions(db_spectrogram, 20.0)
        # Should return original when no active region found
        np.testing.assert_array_equal(result, db_spectrogram)

    # Test execute method with simple parameters
    def test_execute_logarithmic_scaling(self):
        # Create a minimal mock audio input
        audio = {
            "waveform": torch.randn(1, 1, 22050),  # 1 channel, 1 sec of audio at 22050 Hz
            "sample_rate": 22050,
        }

        # Test with logarithmic scaling
        result = self.encoder.execute(audio=audio, window_size=25.0, hop_size=15.0, windowing_func="Hanning", db_norm=80.0, colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF", cutoff_switch=False, scaling_method="Logarithmic", active_db=60.0, mel_scale=False, slaney_norm=False)

        # Should return a tensor (spectrogram)
        spectrogram_tensor = result[0]
        assert isinstance(spectrogram_tensor, torch.Tensor)
        assert len(spectrogram_tensor.shape) == 4  # (batch, height, width, channels)

    def test_execute_linear_scaling(self):
        # Create a minimal mock audio input
        audio = {"waveform": torch.randn(1, 1, 22050), "sample_rate": 22050}

        # Test with linear scaling
        result = self.encoder.execute(audio=audio, window_size=25.0, hop_size=15.0, windowing_func="Hanning", db_norm=80.0, colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF", cutoff_switch=False, scaling_method="Linear", active_db=60.0, mel_scale=False, slaney_norm=False)

        # Should return a tensor
        spectrogram_tensor = result[0]
        assert isinstance(spectrogram_tensor, torch.Tensor)

    def test_execute_quadratic_scaling(self):
        # Create a minimal mock audio input
        audio = {"waveform": torch.randn(1, 1, 22050), "sample_rate": 22050}

        # Test with quadratic scaling
        result = self.encoder.execute(audio=audio, window_size=25.0, hop_size=15.0, windowing_func="Hanning", db_norm=80.0, colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF", cutoff_switch=False, scaling_method="Quadratic", active_db=60.0, mel_scale=False, slaney_norm=False)

        # Should return a tensor
        spectrogram_tensor = result[0]
        assert isinstance(spectrogram_tensor, torch.Tensor)

    def test_execute_logarithmic_mel_scaling(self):
        # Create a minimal mock audio input
        audio = {"waveform": torch.randn(1, 1, 22050), "sample_rate": 22050}

        # Test with logarithmic mel scaling
        result = self.encoder.execute(audio=audio, window_size=25.0, hop_size=15.0, windowing_func="Hanning", db_norm=80.0, colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF", cutoff_switch=False, scaling_method="Logarithmic Mel", active_db=60.0, mel_scale=False, slaney_norm=False)

        # Should return a tensor
        spectrogram_tensor = result[0]
        assert isinstance(spectrogram_tensor, torch.Tensor)

    def test_execute_with_cutoff(self):
        # Create a minimal mock audio input
        audio = {"waveform": torch.randn(1, 1, 22050), "sample_rate": 22050}

        # Test with cutoff enabled
        result = self.encoder.execute(audio=audio, window_size=25.0, hop_size=15.0, windowing_func="Hanning", db_norm=80.0, colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF", cutoff_switch=True, scaling_method="Logarithmic", active_db=60.0, mel_scale=False, slaney_norm=False)

        # Should return a tensor
        spectrogram_tensor = result[0]
        assert isinstance(spectrogram_tensor, torch.Tensor)

    def test_execute_different_windowing_functions(self):
        # Create a minimal mock audio input
        audio = {"waveform": torch.randn(1, 1, 22050), "sample_rate": 22050}

        # Test with different windowing functions
        for window_func in ["Hanning", "Bartlett", "Blackman", "Hamming"]:
            result = self.encoder.execute(audio=audio, window_size=25.0, hop_size=15.0, windowing_func=window_func, db_norm=80.0, colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF", cutoff_switch=False, scaling_method="Logarithmic", active_db=60.0, mel_scale=False, slaney_norm=False)

            # Should return a tensor
            spectrogram_tensor = result[0]
            assert isinstance(spectrogram_tensor, torch.Tensor)

    def test_execute_with_mel_scale(self):
        # Create a minimal mock audio input
        audio = {"waveform": torch.randn(1, 1, 22050), "sample_rate": 22050}

        # Test with mel_scale enabled
        result = self.encoder.execute(audio=audio, window_size=25.0, hop_size=15.0, windowing_func="Hanning", db_norm=80.0, colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF", cutoff_switch=False, scaling_method="Logarithmic Mel", active_db=60.0, mel_scale=True, slaney_norm=False)

        # Should return a tensor
        spectrogram_tensor = result[0]
        assert isinstance(spectrogram_tensor, torch.Tensor)

    def test_execute_with_slaney_norm(self):
        # Create a minimal mock audio input
        audio = {"waveform": torch.randn(1, 1, 22050), "sample_rate": 22050}

        # Test with slaney_norm enabled
        result = self.encoder.execute(audio=audio, window_size=25.0, hop_size=15.0, windowing_func="Hanning", db_norm=80.0, colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF", cutoff_switch=False, scaling_method="Logarithmic Mel", active_db=60.0, mel_scale=True, slaney_norm=True)

        # Should return a tensor
        spectrogram_tensor = result[0]
        assert isinstance(spectrogram_tensor, torch.Tensor)


class TestSpectrogramDecoder:
    def setup_method(self):
        self.decoder = SpectrogramDecoder()

    # Test colormap_collapse helper method
    def test_colormap_collapse_basic(self):
        # Create a simple test image
        image = torch.rand(10, 10, 3)  # 10x10 RGB image

        result = self.decoder.colormap_collapse(
            image,
            "#000000",  # low
            "#B73779",  # mid
            "#FCFDBF",  # high
        )

        # Should return a normalized value between 0 and 1
        assert result.shape == (10, 10)
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_colormap_collapse_single_channel(self):
        # Test with single channel image (3D with 1 channel)
        image = torch.rand(5, 5, 3)

        result = self.decoder.colormap_collapse(
            image,
            "#FF0000",  # red low
            "#00FF00",  # green mid
            "#0000FF",  # blue high
        )

        assert result.shape == (5, 5)
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    # Test execute method with different channels
    def test_execute_luminance_channel(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)  # Height, Width, RGB

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=False, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Linear", mel_scale=False, channel="luminance", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict
        assert isinstance(audio_dict["waveform"], torch.Tensor)
        assert isinstance(audio_dict["sample_rate"], int)

    def test_execute_channel_red(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=False, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Linear", mel_scale=False, channel="channel_red", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_channel_green(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=False, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Linear", mel_scale=False, channel="channel_green", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_channel_blue(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=False, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Linear", mel_scale=False, channel="channel_blue", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_colormap_channel(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=False, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Linear", mel_scale=False, channel="colormap", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_with_autogain(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=True, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Linear", mel_scale=False, channel="luminance", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_logarithmic_scaling(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=False, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Logarithmic", mel_scale=False, channel="luminance", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_quadratic_scaling(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=False, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Quadratic", mel_scale=False, channel="luminance", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_logarithmic_mel_scaling(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=True, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Logarithmic Mel", mel_scale=False, channel="luminance", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_with_mel_scale(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=False, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Logarithmic Mel", mel_scale=True, channel="luminance", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_with_slaney_norm(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        result = self.decoder.execute(
            image=image, window_size=25.0, hop_size=15.0, windowing_func="Hanning", autogain=True, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Logarithmic Mel", mel_scale=True, channel="luminance", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
        )

        # Should return audio
        audio_dict = result[0]
        assert "waveform" in audio_dict
        assert "sample_rate" in audio_dict

    def test_execute_different_windowing_functions(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        # Test with different windowing functions
        for window_func in ["Hanning", "Bartlett", "Blackman", "Hamming"]:
            result = self.decoder.execute(
                image=image, window_size=25.0, hop_size=15.0, windowing_func=window_func, autogain=False, max_amp=1.0, max_iter=32, top_db=80.0, sampling_rate=22050, gl_momentum=0.99, scaling_method="Linear", mel_scale=False, channel="luminance", colormap_low="#000000", colormap_mid="#B73779", colormap_high="#FCFDBF"
            )

            # Should return audio
            audio_dict = result[0]
            assert "waveform" in audio_dict
            assert "sample_rate" in audio_dict

    def test_execute_different_max_iter(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        # Test with different max_iter values
        for max_iter in [1, 8, 32, 64]:
            result = self.decoder.execute(
                image=image,
                window_size=25.0,
                hop_size=15.0,
                windowing_func="Hanning",
                autogain=False,
                max_amp=1.0,
                max_iter=max_iter,
                top_db=80.0,
                sampling_rate=22050,
                gl_momentum=0.99,
                scaling_method="Linear",
                mel_scale=False,
                channel="luminance",
                colormap_low="#000000",
                colormap_mid="#B73779",
                colormap_high="#FCFDBF",
            )

            # Should return audio
            audio_dict = result[0]
            assert "waveform" in audio_dict
            assert "sample_rate" in audio_dict

    def test_execute_different_gl_momentum(self):
        # Create a mock spectrogram image
        image = torch.rand(513, 513, 3)

        # Test with different gl_momentum values
        for gl_momentum in [0.5, 0.9, 0.99]:
            result = self.decoder.execute(
                image=image,
                window_size=25.0,
                hop_size=15.0,
                windowing_func="Hanning",
                autogain=False,
                max_amp=1.0,
                max_iter=32,
                top_db=80.0,
                sampling_rate=22050,
                gl_momentum=gl_momentum,
                scaling_method="Linear",
                mel_scale=False,
                channel="luminance",
                colormap_low="#000000",
                colormap_mid="#B73779",
                colormap_high="#FCFDBF",
            )

            # Should return audio
            audio_dict = result[0]
            assert "waveform" in audio_dict
            assert "sample_rate" in audio_dict
