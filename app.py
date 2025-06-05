import os
import streamlit as st
from transformers import pipeline
from music21 import stream, note, chord, midi
from midi2audio import FluidSynth

LYRIC_MODEL = "distilgpt2"
MAX_LYRIC_LENGTH = 100

@st.cache_resource
def load_lyric_generator():
    return pipeline("text-generation", model=LYRIC_MODEL)


def generate_lyrics(theme: str) -> str:
    generator = load_lyric_generator()
    prompt = f"Song about {theme}:\n"
    outputs = generator(prompt, max_length=MAX_LYRIC_LENGTH, num_return_sequences=1)
    text = outputs[0]["generated_text"]
    # remove prompt
    return text[len(prompt):].strip()


def generate_melody(file_path: str):
    s = stream.Stream()
    scale_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
    for _ in range(16):
        n = note.Note(scale_notes[_ % len(scale_notes)])
        n.quarterLength = 0.5
        s.append(n)
    c = chord.Chord(['C3', 'E3', 'G3'])
    c.quarterLength = 4
    s.insert(0, c)
    mf = midi.translate.streamToMidiFile(s)
    mf.open(file_path, 'wb')
    mf.write()
    mf.close()


def midi_to_wav(midi_path: str, wav_path: str):
    FluidSynth().midi_to_audio(midi_path, wav_path)


def main():
    st.title("AI Song Bot")
    theme = st.text_input("Enter a theme word:")
    if st.button("Generate") and theme:
        with st.spinner("Generating lyrics..."):
            lyrics = generate_lyrics(theme)
        st.subheader("Lyrics")
        st.write(lyrics)
        with st.spinner("Composing melody..."):
            midi_file = "output.mid"
            wav_file = "output.wav"
            generate_melody(midi_file)
            midi_to_wav(midi_file, wav_file)
        with open(wav_file, 'rb') as f:
            st.download_button("Download song", f, file_name="song.wav")
        # Cleanup
        os.remove(midi_file)
        os.remove(wav_file)

if __name__ == "__main__":
    main()
