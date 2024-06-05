import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import random
import time
import os

# Define the path to the background image
bg_image_path = r'C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\static\bg2.jpeg'

# Read the background image and convert it to base64
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

bg_image_base64 = get_base64_image(bg_image_path)

# Set the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_image_base64}");
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Gesture to Emoji mapping
gesture_emojis = {
    'rock': '✊',
    'paper': '✋',
    'scissors': '✌',
    'None': '❓'
}

def detect_gesture(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    gesture = 'None'
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
            gesture = classify_gesture(landmarks)
    return gesture, image

def classify_gesture(landmarks):
    # Calculate distances between landmarks to determine if fingers are extended or folded
    finger_status = []
    
    # Thumb (Tip: 4, IP: 3, MCP: 2, CMC: 1)
    finger_status.append(is_thumb_folded(landmarks))

    # Index (Tip: 8, DIP: 7, PIP: 6, MCP: 5)
    finger_status.append(is_finger_folded(landmarks, 8, 6))

    # Middle (Tip: 12, DIP: 11, PIP: 10, MCP: 9)
    finger_status.append(is_finger_folded(landmarks, 12, 10))

    # Ring (Tip: 16, DIP: 15, PIP: 14, MCP: 13)
    finger_status.append(is_finger_folded(landmarks, 16, 14))

    # Pinky (Tip: 20, DIP: 19, PIP: 18, MCP: 17)
    finger_status.append(is_finger_folded(landmarks, 20, 18))
    
    if all(finger_status):
        return 'rock'
    elif not any(finger_status):
        return 'paper'
    elif finger_status[1] == False and finger_status[2] == False and all(finger_status[3:]):
        return 'scissors'
    else:
        return 'None'  # Return 'None' if gesture cannot be classified
    
def is_thumb_folded(landmarks):
    # Check if thumb is folded
    return landmarks[4][0] < landmarks[3][0]

def is_finger_folded(landmarks, tip_id, pip_id):
    # Check if finger is folded
    return landmarks[tip_id][1] > landmarks[pip_id][1]

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'Tie'
    if (user_choice == 'rock' and computer_choice == 'scissors') or \
       (user_choice == 'scissors' and computer_choice == 'paper') or \
       (user_choice == 'paper' and computer_choice == 'rock'):
        return 'Human'
    return 'Computer'

def run_game(max_score):
    cap = cv2.VideoCapture(0)
    human_score, computer_score = 0, 0
    computer_choice = 'None'

    # Create placeholders
    computer_emoji_placeholder = st.empty()
    computer_score_placeholder = st.empty()
    human_emoji_placeholder = st.empty()
    human_score_placeholder = st.empty()
    round_winner_placeholder = st.empty()

    while human_score < max_score and computer_score < max_score:
        ret, frame = cap.read()
        if not ret:
            break

        user_gesture, _ = detect_gesture(frame)  # Ignore the annotated image

        if user_gesture != 'None':
            computer_choice = get_computer_choice()
            winner = determine_winner(user_gesture, computer_choice)
            if winner == 'Human':
                human_score += 1
            elif winner == 'Computer':
                computer_score += 1

            # Update placeholders
            computer_emoji_placeholder.markdown(f"<div style='text-align: center; font-size: 100px;'>{gesture_emojis.get(computer_choice, '❓')}</div>", unsafe_allow_html=True)
            computer_score_placeholder.markdown(f"<div style='text-align: center;'>Computer: {computer_score}</div>", unsafe_allow_html=True)
            human_emoji_placeholder.markdown(f"<div style='text-align: center; font-size: 100px;'>{gesture_emojis.get(user_gesture, '❓')}</div>", unsafe_allow_html=True)
            human_score_placeholder.markdown(f"<div style='text-align: center;'>Human: {human_score}</div>", unsafe_allow_html=True)
            round_winner_placeholder.markdown(f"<div style='text-align: center;'>Round Winner: {winner}</div>", unsafe_allow_html=True)

            time.sleep(3)  # Pause for 1 second

        if human_score >= max_score or computer_score >= max_score:
            break

    cap.release()
    overall_winner = 'Human' if human_score > computer_score else 'Computer'
    round_winner_placeholder.markdown(f"<div style='text-align: center; font-size: 30px;'>Game Over! Winner: {overall_winner}</div>", unsafe_allow_html=True)
    st.write(f'To play again, click the restart button below.')
    st.button('Restart Game', key='restart_button')

def restart_game():
    # Clear the Streamlit app state and restart the game
    st.session_state.pop('human_score', None)
    st.session_state.pop('computer_score', None)
    st.session_state.pop('max_score', None)
    st.session_state.pop('game_started', None)

# Set title
st.title('ROCK-PAPER-SCISSOR')

if 'game_started' not in st.session_state:
    # Initialize game variables
    st.session_state.human_score = 0
    st.session_state.computer_score = 0
    st.session_state.game_started = True

# Input for maximum score
max_score = st.number_input('Enter the maximum score:', min_value=1, step=1)

# Start button
start_button = st.button('Start Game')

# Show game elements only if start button is pressed
if start_button:
    run_game(max_score)

# Restart game if restart button is clicked
if 'restart_button' in st.session_state:
    restart_game()
