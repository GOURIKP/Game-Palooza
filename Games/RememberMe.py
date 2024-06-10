import streamlit as st
import random
import time
import base64
import os
import pyttsx3
import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# Function to add background video
def add_bg_video(video_path):
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode("utf-8")

    bg_video_style = f"""
    <style>
    .stApp {{
        background: url("data:video/mp4;base64,{video_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }}
    </style>
    <video autoplay loop muted playsinline style="position: fixed; top: 50%; left: 50%; width: 100%; height: 100%; object-fit: cover; transform: translate(-50%, -50%); z-index: -1;">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
    """
    st.markdown(bg_video_style, unsafe_allow_html=True)

# Path to your background video
video_path = r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\212831_small.mp4"
add_bg_video(video_path)
# Initialize pyttsx3 engine
engine = pyttsx3.init()

# List of words to choose from
words_list = ["apple", "banana", "cherry", "date", "elderberry", 
              "fig", "grape", "honeydew", "kiwi", "lemon",
              "mango", "nectarine", "orange", "papaya", "quince"]

# Function to generate random words
def generate_words():
    return random.sample(words_list, 10)

# Function to text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to record audio
def record_audio(duration=10, fs=44100):
    st.write("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    st.write("Recording finished.")
    return recording, fs

# Function to save and recognize audio
def recognize_audio(recording, fs):
    file_path = "output.wav"
    write(file_path, fs, recording)  # Save as WAV file
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Streamlit app
def main():
    st.title("Remember Me")

    if "state" not in st.session_state:
        st.session_state.state = "INIT"
        st.session_state.words = []
        st.session_state.recognized_words = ""
        st.session_state.restart_clicked = False

    if st.session_state.state == "INIT":
        if st.button("Start Game"):
            st.session_state.words = generate_words()
            st.session_state.state = "MEMORIZE"
            st.rerun()

    elif st.session_state.state == "MEMORIZE":
        st.write("Memorize these words:")
        st.write(", ".join(st.session_state.words))
        time.sleep(10)
        st.session_state.state = "RECALL"
        st.rerun()

    elif st.session_state.state == "RECALL":
        st.write("Prepare to recite the words in the correct sequence...")
        time.sleep(3)
        st.write("Please recite the words now.")
        recording, fs = record_audio(duration=10)
        recognized_text = recognize_audio(recording, fs)
        st.session_state.recognized_words = recognized_text
        st.session_state.state = "RESULT"
        st.rerun()

    elif st.session_state.state == "RESULT":
        st.write(f"Recognized words: {st.session_state.recognized_words}")
        recognized_text = st.session_state.recognized_words
        user_words = recognized_text.split()
        
        if user_words == st.session_state.words:
            st.write("You Won!")
            speak("You Won")
        else:
            st.write("You Lose!")
            speak("You Lose")

        st.write("Game Over!")
        st.session_state.state = "INIT"  # Reset the game
        st.session_state.words = []  # Clear the words
        st.session_state.recognized_words = ""  # Clear the recognized words
        st.session_state.restart_clicked = False
        st.rerun()

if __name__ == "__main__":
    main()
