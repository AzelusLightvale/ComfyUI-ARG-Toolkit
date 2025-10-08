import os
import inspect
import textwrap

import stegano
import imwatermark
import torch
from PIL import Image
import numpy as np

import folder_paths  # This is dealt with by ComfyUI. If this import is throwing an error, ignore it.

# Every node is inspired heavily by their reference implementations in their GitHub repository, with changes made to best use PyTorch as possible as it's the main way ComfyUI stores data
# For more information, check https://docs.comfy.org/custom-nodes/backend/images_and_masks#images

# TODO: Deduplicate this entire file and convert it to a more reasonable standard, like the rest of the nodes.


class Stegano_LSB_Encode:
    def __init__(self):
        pass

    CATEGORY = "Steganography"
    DESCRIPTION = textwrap.dedent("""Encodes a message in the least significant bit (LSB) of the image. Includes some generators for different steganography methods for harder detection.
    - Library used: [Stegano](https://github.com/cedricbonhomme/Stegano)
    Note that currently, some of the generators (specifically: carmichael, fermat, fibonacci, log_gen, and mersenne) are currently broken and are excluded.
    """)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": (
                    "IMAGE",
                    {},
                ),
                "message": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Input your message here...",
                    },
                ),
                "m": (
                    "INT",
                    {
                        "default": 1,
                        "min": 1,
                        "step": 1,
                        "display": "number",
                        "tooltip": "The primary number used when accessing certain generators. Needed for: LFSR, Ackermann (all variants).",
                    },
                ),
                "n": (
                    "INT",
                    {
                        "default": 2,
                        "min": 1,
                        "step": 1,
                        "display": "number",
                        "tooltip": "The secondary number used when accessing certain generators. Needed for: Ackermann (Slow, Fast).",
                    },
                ),
                "generator_type": (
                    ["None"]
                    + [
                        name
                        for name, _ in inspect.getmembers(stegano.lsb.generators, inspect.isfunction)
                        if name
                        not in [
                            "carmichael",
                            "fermat",
                            "fibonacci",
                            "log_gen",
                            "mersenne",
                        ]
                    ],
                ),  # Extracts the available generators to use with Stegano
                "encoding": (
                    ["UTF-8", "UTF-32LE"],
                    {
                        "default": "UTF-8",
                        "tooltip": "Chooses the encoding format for the message. Only allows standard UTF-8 or a version with UTF-32LE",
                    },
                ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "encode_stego"

    def encode_stego(self, images, message, m, n, generator_type, encoding):
        B, H, W, C = images.shape
        output_images = []
        for i in range(B):
            img_tensor = images[i]  # [H,W,C]
            if img_tensor.dtype == torch.float32:
                img_np = (img_tensor.numpy() * 255).astype(np.uint8)
            else:
                img_np = img_tensor.numpy()
            img_pil = Image.fromarray(img_np)
            generator_func = getattr(stegano.lsb.generators, generator_type)
            if generator_type == "None":
                generator_type = None
            elif generator_type in ["LFSR", "ackermann", "ackermann_naive"]:
                generator_type = generator_func(m=m)
            elif generator_type in ["ackermann_fast", "ackermann_slow"]:
                generator_type = generator_func(m=m, n=n)
            elif generator_type == "shi_tomashi":
                temp_dir = folder_paths.get_temp_directory()
                temp_path = os.path.join(temp_dir, f"image_{i}.png")
                img_pil.save(temp_path)
                generator_type = generator_func(temp_path)
            else:
                generator_type = generator_func()
            img_pil = stegano.lsb.hide(img_pil, message, generator_type, encoding=encoding)
            img_np_out = np.array(img_pil)
            img_tensor_out = torch.from_numpy(img_np_out).float() / 255.0
            output_images.append(img_tensor_out)
        return (torch.stack(output_images, dim=0),)


class Stegano_LSB_Decode:
    def __init__(self):
        pass

    CATEGORY = "Steganography"
    DESCRIPTION = textwrap.dedent("""Decodes a message in the least significant bit (LSB) of the image. Includes some generators for different steganography methods for harder detection.
    - Library used: [Stegano](https://github.com/cedricbonhomme/Stegano)
    Note that currently, some of the generators (specifically: carmichael, fermat, fibonacci, log_gen, and mersenne) are currently broken and are excluded.
    """)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": (
                    "IMAGE",
                    {},
                ),
                "m": (
                    "INT",
                    {
                        "default": 1,
                        "min": 1,
                        "step": 1,
                        "display": "number",
                        "tooltip": "The primary number used when accessing certain generators. Needed for: LFSR, Ackermann (all variants).",
                    },
                ),
                "n": (
                    "INT",
                    {
                        "default": 2,
                        "min": 1,
                        "step": 1,
                        "display": "number",
                        "tooltip": "The secondary number used when accessing certain generators. Needed for: Ackermann (Fast, Slow).",
                    },
                ),
                "generator_type": (
                    ["None"]
                    + [
                        name
                        for name, _ in inspect.getmembers(stegano.lsb.generators, inspect.isfunction)
                        if name
                        not in [
                            "carmichael",
                            "fermat",
                            "fibonacci",
                            "log_gen",
                            "mersenne",
                        ]
                    ],
                ),
                "encoding": (
                    ["UTF-8", "UTF-32LE"],
                    {
                        "default": "UTF-8",
                        "tooltip": "Chooses the encoding format for the message. Only allows standard UTF-8 or a version with UTF-32LE",
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "decode_stego"

    def decode_stego(self, images, m, n, generator_type, encoding):
        B, H, W, C = images.shape
        final_output = []
        for i in range(B):
            img_tensor = images[i]  # [H,W,C]
            if img_tensor.dtype == torch.float32:
                img_np = (img_tensor.numpy() * 255).astype(np.uint8)
            else:
                img_np = img_tensor.numpy()
            img_pil = Image.fromarray(img_np)
            generator_func = getattr(stegano.lsb.generators, generator_type)
            if generator_type == "None":
                generator_type = None
            elif generator_type in ["LFSR", "ackermann", "ackermann_naive"]:
                generator_type = generator_func(m=m)
            elif generator_type in ["ackermann_fast", "ackermann_slow"]:
                generator_type = generator_func(m=m, n=n)
            elif generator_type == "shi_tomashi":
                temp_dir = folder_paths.get_temp_directory()
                temp_path = os.path.join(temp_dir, f"image_{i}.png")
                img_pil.save(temp_path)
                generator_type = generator_func(temp_path)
            else:
                generator_type = generator_func()
            final_output.append(stegano.lsb.reveal(img_pil, generator_type, encoding=encoding))
        return ("".join(final_output),)


class IMWatermarkEncode:
    def __init__(self):
        pass

    CATEGORY = "Steganography"
    DESCRIPTION = textwrap.dedent("""Hides a message of choice into the image. Utilizes discrete wavelet transform (DWT) and discrete cosine transform (DCT) by default, but also includes options for RivaGAN.
    - Library used: [invisible-watermark](https://github.com/ShieldMnt/invisible-watermark/)
    From my own testing, recommended algorithm choice is dwtDctSvd, which includes singular value decomposition to fortify it better at a slight cost of time.
    """)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": (
                    "IMAGE",
                    {},
                ),
                "message": (
                    "STRING",
                    {
                        "default": "Hello World!",
                        "multiline": True,
                        "placeholder": "Input your message here...",
                    },
                ),
                "algorithm": (
                    ["dwtDct", "dwtDctSvd", "rivaGan"],
                    {
                        "tooltip": textwrap.dedent("""In order of appearance:
                    - dwtDct: Discrete wavelet transform + Discrete cosine transform. Works, but unreliable.
                    - dwtDctSvd (Recommended): Same as above, but includes singular value decomposition.
                    - rivaGan: Uses a 32-bit RivaGAN implementation. Slow, experimental, and limited to 32 bits worth of information.
                    """),
                    },
                ),
                "types": (
                    ["bytes", "b16", "bits", "uuid", "ipv4"],
                    {
                        "tooltip": textwrap.dedent("""In order of appearance:
                    - bytes: Transforms message to bytes.
                    - b16: Text -> Byte representation -> Hexadecimal -> Byte representation.
                    - bits: 8 bits = 1 byte. Good for transmitting small binary messages.
                    - UUID: Takes a UUID string and embeds that. Do not use to send messages.
                    - IPv4: Takes an IPv4 address and embeds that.
                    """),
                    },
                ),
                "encoding_format": (
                    [
                        "utf-8",
                        "utf-16",
                        "utf-32",
                        "ascii",
                        "latin-1",
                        "cp1252",
                        "utf-8-sig",
                        "Other",
                    ],
                    {
                        "tooltip": "The encoding format available for text, may yield different results when converting.",
                    },
                ),
            },
            "optional": {
                "other_encoding_format": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": 'If, for some reason, your chosen encoding format is not available in the dropdown, select "Other" in encoding_format and type in your encoding format here. Supports all format written in Python\'s `encoding` module.',
                    },
                )
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "encode_imwatermark"

    def encoding_selector(self, encoding_format, other_encoding_format):
        if encoding_format == "Other":
            encoding_format = other_encoding_format
        return encoding_format

    def encode_imwatermark(self, images, message, algorithm, types, encoding_format, other_encoding_format):
        B, H, W, C = images.shape
        output_images = []
        encoding_format = self.encoding_selector(encoding_format, other_encoding_format)
        if algorithm == "rivaGan":
            imwatermark.WatermarkEncoder().loadModel()
        if types == "bytes":  # Wants watermark bytes
            encoded_message = message.encode(encoding_format)
        elif types == "b16":  # Also wants watermark bytes, but needs to convert to hex first
            encoded_message = message.encode(encoding_format).hex().upper().encode(encoding_format)
        elif types == "bits":  # Wants bit list
            encoded_message = [int(bit) for byte in message.encode(encoding_format) for bit in f"{byte:08b}"]
        else:  # Wants string
            encoded_message = message
        encoder = imwatermark.WatermarkEncoder()
        encoder.set_watermark(types, encoded_message)
        for i in range(B):
            img_tensor = images[i]  # [H,W,C]
            img_np = (img_tensor.numpy() * 255).astype(np.uint8)
            img_pil = np.array(Image.fromarray(img_np))[:, :, ::-1]
            encoded_np = np.array(encoder.encode(img_pil, algorithm))[:, :, ::-1]
            img_tensor_out = torch.from_numpy(encoded_np.copy()).float() / 255.0
            output_images.append(img_tensor_out)
        return (torch.stack(output_images, dim=0),)


class IMWatermarkDecode:
    def __init__(self):
        pass

    CATEGORY = "Steganography"
    DESCRIPTION = textwrap.dedent("""Hides a message of choice into the image. Utilizes discrete wavelet transform (DWT) and discrete cosine transform (DCT) by default, but also includes options for RivaGAN.
    - Library used: [invisible-watermark](https://github.com/ShieldMnt/invisible-watermark/)
    From my own testing, recommended algorithm choice is dwtDctSvd, which includes singular value decomposition to fortify it better at a slight cost of time.
    """)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": (
                    "IMAGE",
                    {},
                ),
                "length": (
                    "INT",
                    {
                        "default": 96,
                        "min": 1,
                        "step": 1,
                        "display": "number",
                        "toolip": "Length of the message to decode. Check the tooltip in Types for more information.",
                    },
                ),
                "algorithm": (
                    ["dwtDct", "dwtDctSvd", "rivaGan"],
                    {
                        "tooltip": textwrap.dedent("""In order of appearance:
                    - dwtDct: Discrete wavelet transform + Discrete cosine transform. Works, but unreliable.
                    - dwtDctSvd (Recommended): Same as above, but includes singular value decomposition.
                    - rivaGan: Uses a 32-bit RivaGAN implementation. Slow, experimental, and limited to 32 bits worth of information.
                    """),
                    },
                ),
                "types": (
                    ["bytes", "b16", "bits", "uuid", "ipv4"],
                    {
                        "tooltip": textwrap.dedent("""In order of appearance (and encoding length needed):
                    - bytes (8 * total byte length): Transforms message to bytes.
                    - b16 (4 * total b16 length): Text -> Byte representation -> Hexadecimal -> Byte representation.
                    - bits (equivalent to array length): 8 bits = 1 byte. Good for transmitting small binary messages.
                    - UUID (128 bits, fixed): Takes a UUID string and embeds that. Do not use to send messages.
                    - IPv4 (32 bits, fixed): Takes an IPv4 address and embeds that.""")
                    },
                ),
                "encoding_format": (
                    [
                        "utf-8",
                        "utf-16",
                        "utf-32",
                        "ascii",
                        "latin-1",
                        "cp1252",
                        "utf-8-sig",
                        "Other",
                    ],
                    {
                        "tooltip": "The encoding format available for text, may yield different results when converting.",
                    },
                ),
            },
            "optional": {
                "other_encoding_format": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": 'If, for some reason, your chosen encoding format is not available in the dropdown, select "Other" in encoding_format and type in your encoding format here. Supports all format written in Python\'s `encoding` module.',
                    },
                )
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "decode_imwatermark"

    def encoding_selector(self, encoding_format, other_encoding_format):
        if encoding_format == "Other":
            encoding_format = other_encoding_format
        return encoding_format

    def decode_imwatermark(self, images, length, algorithm, types, encoding_format, other_encoding_format):
        B, H, W, C = images.shape
        final_output = []
        encoding_format = self.encoding_selector(encoding_format, other_encoding_format)
        if types in ["bytes", "bits", "b16"]:  # Bit-related types
            if length <= 0:
                raise ValueError(
                    "Length is required for bytes-based watermark decoding. Please put in a non-zero length, preferably in a multiplication of 8."
                )
            decoder = imwatermark.WatermarkDecoder(types, length)
        else:
            decoder = imwatermark.WatermarkDecoder(types)
        if algorithm == "rivaGan":
            imwatermark.WatermarkDecoder().loadModel()
        for i in range(B):
            img_tensor = images[i]  # [H,W,C]
            img_np = (img_tensor.numpy() * 255).astype(np.uint8)
            img_pil = np.array(Image.fromarray(img_np))[:, :, ::-1]
            decoded_bit = decoder.decode(img_pil, algorithm)
            if types == "bytes":  # Returns watermark bytes
                decoded_str = decoded_bit.decode(encoding_format)
            elif types == "b16":
                decoded_str = bytes.fromhex(decoded_bit.decode(encoding_format)).decode(encoding_format)
            elif types == "bits":  # Returns bits in a list of 0/1 (i.e: [0, 1, 1, 0, 1,...])
                bits_int = [int(bit) for bit in decoded_bit]
                byte_chunks = [bits_int[i : i + 8] for i in range(0, len(bits_int), 8)]
                decoded_bytes = bytes(int("".join(str(b) for b in chunk), 2) for chunk in byte_chunks)
                decoded_str = decoded_bytes.decode(encoding_format)
            else:  # Returns string
                decoded_str = decoded_bit
            final_output.append(decoded_str)
        return ("".join(final_output),)


class SteganoAnalysis:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"image": ("IMAGE", {}), "mode": (["Parity", "Statistics"])}}

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "analyze"

    def analyze(self, image, mode):
        B, H, W, C = image.shape
        output_images = []
        for i in range(B):
            img_tensor = image[i]  # [H,W,C]
            if img_tensor.dtype == torch.float32:
                img_np = (img_tensor.numpy() * 255).astype(np.uint8)
            else:
                img_np = img_tensor.numpy()
            img_pil = Image.fromarray(img_np)
            # This part is a stub. Insert actual analysis function here
            if mode == "Parity":
                img_pil = stegano.steganalysis.parity(img_pil)
            elif mode == "Statistics":
                img_pil = stegano.steganalysis.statistics(img_pil)
            else:
                raise ValueError(f"Your chosen mode ({mode}) is invalid.")
            img_np_out = np.array(img_pil)
            img_tensor_out = torch.from_numpy(img_np_out).float() / 255.0
            output_images.append(img_tensor_out)
        return (torch.stack(output_images, dim=0),)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "SteganoLSBEncode": Stegano_LSB_Encode,
    "SteganoLSBDecode": Stegano_LSB_Decode,
    "SteganoAnalysis": SteganoAnalysis,
    "IMWatermarkEncode": IMWatermarkEncode,
    "IMWatermarkDecode": IMWatermarkDecode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SteganoLSBEncode": "Stegano LSB Encode",
    "SteganoLSBDecode": "Stegano LSB Decode",
    "SteganoAnalysis": "Stegano Analysis",
    "IMWatermarkEncode": "Invisible Watermark Encode",
    "IMWatermarkDecode": "Invisible Watermark Decode",
}
