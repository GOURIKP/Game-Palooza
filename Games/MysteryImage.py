import streamlit as st
from PIL import Image
import random
import base64
import os

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

# Define the paths to your images
image_paths = {
    "cat": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\cat.jpg",
    "dog": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\dog.jpg",
    "car": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\car.jpg",
    "tree": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\tree.jpg",
    "house": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\house.jpg",
    "bicycle": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\bicycle.jpg",
    "computer": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\computer.jpg",
    "flower": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\flower.jpg",
    "bird": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\bird.jpg",
    "boat": r"C:\Users\gouri\OneDrive\Desktop\PROJECTS\ROCK PAPER SCISSOR\images\boat.jpg"
}

def partially_obscure_image(image_path):
    img = Image.open(image_path)
    width, height = img.size
    # Create a blank image with the same size as the original image
    blank_img = Image.new("RGB", (width, height), (255, 255, 255))  # White color
    # Randomly select the number of parts to reveal (adjust as needed)
    num_parts = random.randint(1, 5)
    for _ in range(num_parts):
        # Randomly select the position and size of the part to reveal
        part_width = random.randint(width // 4, width // 2)
        part_height = random.randint(height // 4, height // 2)
        x = random.randint(0, width - part_width)
        y = random.randint(0, height - part_height)
        # Paste the corresponding part of the original image onto the blank image
        part_of_original = img.crop((x, y, x + part_width, y + part_height))
        blank_img.paste(part_of_original, (x, y))
    return blank_img

def reset_game():
    st.session_state.round = 1
    st.session_state.wins = 0
    st.session_state.object_name, st.session_state.image_path = random.choice(list(image_paths.items()))

def main():
    st.title("Find the Object Game")

    if "round" not in st.session_state:
        reset_game()

    object_name = st.session_state.object_name
    image_path = st.session_state.image_path

    obscured_img = partially_obscure_image(image_path)
    st.image(obscured_img, caption=f"Round {st.session_state.round}: Find the object in the image")
    user_input = st.text_input("Enter your guess:")

    if st.button("Submit"):
        if user_input.strip().lower() == object_name:
            st.success("Congratulations! You found the object.")
            st.session_state.wins += 1
            st.session_state.round += 1
        else:
            st.error(f"Sorry, that's not correct. The correct answer was '{object_name}'.")
            st.session_state.round = 6  # End the game

        if st.session_state.round <= 5:
            st.session_state.object_name, st.session_state.image_path = random.choice(list(image_paths.items()))
            st.experimental_rerun()
        else:
            if st.session_state.wins == 5:
                st.balloons()
                st.success("Congratulations! You won all 5 rounds!")
            else:
                st.error(f"Game over. You won {st.session_state.wins} out of 5 rounds.")
            if st.button("Restart"):
                reset_game()
                st.experimental_rerun()

if __name__ == "__main__":
    main()
