# Morse Code

This node provides tools to encode and decode messages using Morse code for various languages.

## Historical Context

Morse code is a method used in telecommunication to encode text characters as standardized sequences of two different signal durations, called dots and dashes (or dits and dahs). It is named after Samuel Morse, an inventor of the telegraph. International Morse Code encodes the 26 basic Latin letters, some extra Latin letters, the Arabic numerals and a small set of punctuation and procedural signals (prosigns). There is no distinction between upper and lower case letters.

## How it Works

The node can both encode a given text into Morse code and decode Morse code back into text. It supports multiple languages, each with its own specific Morse code alphabet.

- **Encoding**: Each character in the input text is replaced by its corresponding Morse code sequence. A space is used to separate letters, and multiple spaces (or an empty string in the output array) can represent a word separator.
- **Decoding**: The input Morse code string is split into characters and words. Each code is looked up in the reverse dictionary to find the original character.

The node is flexible, allowing you to define what characters represent a "dot" and a "dash".

### Special Language Handling

- **Japanese**: The node expects and converts input to Katakana, following the Wabun code standard. It can handle Hiragana input by converting it to Katakana.
- **Korean**: The node decomposes Hangul syllables into their constituent Jamo (consonant and vowel) characters before encoding, as per the SKATS (Standard Korean Alphabet Transliteration System) convention for Morse code.
- **Greek**: The node converts text to uppercase and strips accents before encoding.

## Parameters

- **text**: The message to encode or decode.
- **mode**: A toggle to switch between `encode` and `decode` mode.
- **language**: The language of the Morse code alphabet to use. Supported languages are:
    - `latin`: Standard international Morse code.
    - `russian`: For text using the Cyrillic alphabet.
    - `arabic`: For text using the Arabic alphabet.
    - `hebrew`: For text using the Hebrew alphabet.
    - `greek`: For text using the Greek alphabet.
    - `korean`: For Korean text (uses SKATS).
    - `japanese-wabun`: For Japanese text (uses Wabun code).
- **dot**: The character to be used for a "dot" (e.g., `.`).
- **dash**: The character to be used for a "dash" (e.g., `-`).
