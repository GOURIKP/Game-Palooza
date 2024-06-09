import streamlit as st
from streamlit_option_menu import option_menu
import base64
import os
import importlib.util

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

# Function to display the welcome page
def welcome_page():
    st.markdown("<h1 style='text-align: center; font-size: 4em;'>Game Palooza👾</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Enter Game Arena"):
        st.session_state.page = 'game_arena'
    st.markdown("</div>", unsafe_allow_html=True)



# Function to display the game selection page
def game_arena_page():
    st.markdown("<h1 style='text-align: center;'>Game Arena</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Select A Game From Below</h5>", unsafe_allow_html=True)
    
    # Define the columns for layout
    col1, col2, col3= st.columns(3)  # 3 columns
    
    # Display the first image and button in col1
    game1_image_path = r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\game1pic.jpeg"
    col1.image(game1_image_path, width=150)
    if col1.button("Rock-Paper-Scissors"):
        # Redirect to the game page for the first image
        st.session_state.page = 'rock_paper_scissors'
    
    # Display the second image and button in col2
    game2_image_path = r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\game2pic.jpeg"
    col2.image(game2_image_path, width=150)
    if col2.button("Remember Me"):
        # Add functionality for the "Play Remember Me" button
        st.session_state.page = 'remember_me'

    # Display the third image and button in col3
    game3_image_path = r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\game3pic.jpeg"
    col3.image(game3_image_path, width=150)
    if col3.button("Mystery Image"):
        # Add functionality for the "Fire It Up" button
        st.session_state.page = 'mystery_image'

    # Add button to go back to home page
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Back to Home Page"):
        st.session_state.page = 'welcome'
    st.markdown("</div>", unsafe_allow_html=True)



# Function to run the rock-paper-scissors game
def rock_paper_scissors():
    # Dynamically load and run the rock game script
    rock_path = r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\rock.py"
    spec = importlib.util.spec_from_file_location("rock", rock_path)
    rock = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rock)
    with st.sidebar:
        selected = option_menu("Choose", ["Rock-Paper-Scissors", "Game Arena", "Home Page"])
    if selected == "Game Arena":
        st.session_state.page = 'game_arena'
    elif selected == "Home Page":
        st.session_state.page = 'welcome'

    rock.main()

# Function to run the "Remember Me" game
def remember_me_game():
    # Dynamically load and run the Remember Me game script
    remember_me_path = r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\RememberMe.py"
    spec = importlib.util.spec_from_file_location("remember_me", remember_me_path)
    remember_me = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(remember_me)
    with st.sidebar:
        selected = option_menu("Choose", ["Remember Me", "Game Arena", "Home Page"])
    if selected == "Game Arena":
        st.session_state.page = 'game_arena'
    elif selected == "Home Page":
        st.session_state.page = 'welcome'

    remember_me.main()

# Function to run the "Mystery Image" game
def mystery_image_game():
    # Dynamically load and run the Mystery Image game script
    mystery_image_path = r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\MysteryImage.py"
    spec = importlib.util.spec_from_file_location("mystery_image", mystery_image_path)
    mystery_image = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mystery_image)
    with st.sidebar:
        selected = option_menu("Choose", ["Mystery Image", "Game Arena", "Home Page"])
    if selected == "Game Arena":
        st.session_state.page = 'game_arena'
    elif selected == "Home Page":
        st.session_state.page = 'welcome'

    mystery_image.main()

# Set up page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'



# Display the appropriate page based on the session state
if st.session_state.page == 'welcome':
    welcome_page()
    # Add background video
    add_bg_video(video_path)
elif st.session_state.page == 'game_arena':
    game_arena_page()
    # Add background video
    add_bg_video(video_path)
elif st.session_state.page == 'rock_paper_scissors':
    rock_paper_scissors()
elif st.session_state.page == 'remember_me':
    remember_me_game()
elif st.session_state.page == 'mystery_image':
    mystery_image_game()