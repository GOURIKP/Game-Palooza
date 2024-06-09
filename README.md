# Game Palooza

Game Palooza is a web-based application created with Streamlit that offers a collection of fun and interactive mini-games. The app provides a visually appealing interface with background videos and easy navigation between different games.

## Features

- **Background Video**: Adds an engaging background video to the application.
- **Welcome Page**: Greets users with a welcome message and an option to enter the game arena.
- **Game Arena**: A hub where users can select from various mini-games.
- **Mini-Games**:
  - **Rock-Paper-Scissors**: Play the classic hand game using your webcam for gesture recognition.
  - **Remember Me**: A memory game where you memorize and recite a sequence of words.
  - **Mystery Image**: Guess the object in a partially obscured image.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/gamepalooza.git
   cd gamepalooza
   ```

2. **Install the required libraries**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run gamepalooza.py
   ```

## File Structure

- `gamepalooza.py`: The main application file containing the Streamlit interface and page navigation.
- `rock.py`: The Rock-Paper-Scissors game implementation.
- `rememberme.py`: The Remember Me game implementation.
- `mysteryimage.py`: The Mystery Image game implementation.
- `requirements.txt`: List of required Python libraries.


### Mini-Games and Tools Used

#### Rock-Paper-Scissors

- **Description**: This game uses your webcam to recognize hand gestures.
- **Tools Used**:
  - OpenCV: For accessing and processing the webcam feed.
  - TensorFlow/Keras: For hand gesture recognition model.
  - Mediapipe: For real-time hand tracking.

#### Remember Me

- **Description**: Memorize a sequence of words displayed on the screen and then recite them. Your speech will be recognized and matched against the original words.
- **Tools Used**:
  - SpeechRecognition: For capturing and processing audio input.
  - gTTS (Google Text-to-Speech): For converting text to speech.
  - Pyaudio: For handling audio streams.

#### Mystery Image

- **Description**: Guess the object in a partially obscured image. Type your guess and submit to see if you're correct.
- **Tools Used**:
  - PIL (Pillow): For image processing and manipulation.
  - Random: For selecting random images and obscuring them.

## Sample Images

### Game Arena Page
![Game Arena]([https://github.com/GOURIKP/Game-Palooza/blob/main/sample%20images/sampleimage1.png])

### Other Pages
Sample images of the site can be found in the `sample images` folder.

### Enjoy playing at Game Palooza! 👾
