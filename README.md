# AI Song Bot

This repository contains a minimal web application that generates song lyrics
and simple background music from a theme. The entire pipeline runs locally on a
MacBook with 32 GB of RAM.

## Features
- Web interface using **Streamlit**.
- Lyrics generated with the small `distilgpt2` model from HuggingFace.
- Simple melody generation using the `music21` library.
- Export the resulting song as a WAV file with a download link.

## Requirements
- Python 3.9+
- `pip install -r requirements.txt`
- On macOS, install Fluidsynth for MIDI to audio conversion:
  ```bash
  brew install fluid-synth
  ```

## Running
```bash
streamlit run app.py
```

Enter a topic word in the web interface and press **Generate**.
The app creates a short lyric and a matching melody, then provides
an audio download link.
