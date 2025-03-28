import streamlit as st
import openai
import requests
import os
from dotenv import load_dotenv
import base64

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

openai.api_key = OPENAI_API_KEY

custom_responses = {
    "Introduction": 
        "I am a software engineer with strong expertise in Python, MySQL and machine learning. I have worked on AI-related projects and enjoy applying my skills to real-world problems.",

    "What should we know about your life story in a few sentences?": 
        "I have always been passionate about coding and building innovative solutions. I pursued my education in Computer Science & Engineering from SRM Institute of Science & Technology and gained hands-on experience through internships in AI and machine learning. I enjoy creating new things with code and continuously expanding my knowledge.",

    "What’s your #1 superpower?": 
        "My ability to quickly learn and adapt to new technologies. Whether it’s optimizing databases, developing AI models or solving complex coding challenges, I am always eager to improve and refine my skills.",

    "What are the top 3 areas you’d like to grow in?": 
        "I want to further develop my expertise in machine learning, strengthen my database management skills with MySQL and improve my ability to integrate AI into practical applications.",

    "What misconception do your coworkers have about you?": 
        "People sometimes assume I only focus on technical implementation, but I also enjoy problem-solving, discussing ideas and collaborating with others to refine and improve projects.",

    "How do you push your boundaries and limits?": 
        "I continuously challenge myself by working on complex projects, keeping up with the latest AI advancements and experimenting with new tools to enhance my skill set.",

    "Skills": 
        "My key skills include Python, MySQL and machine learning. I also have experience with AI-driven solutions and database management.",

    "Projects": 
        "I have worked on AI and machine learning projects, including developing models for data-driven insights and optimizing MySQL databases for efficiency."
}


def get_response(user_input):
    return custom_responses.get(user_input, "I'm not sure how to answer that. Please select a question from the dropdown.")

# Function to generate voice from text
def text_to_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.content  # Returns the audio file data
    else:
        st.error(f"Failed to generate voice. Error: {response.text}")  # Print API error response
        return None

# Streamlit UI
st.title("AI Voice Bot 🎙️")
st.write("Select a question, and I'll respond with text and voice!")

# Dropdown for predefined questions
selected_question = st.selectbox("Choose a question:", list(custom_responses.keys()))

if st.button("Get Response"):
    response_text = get_response(selected_question)
    st.write("**AI Response:**", response_text)

    # Generate speech
    audio_data = text_to_speech(response_text)

    if audio_data:
        audio_file = "response.mp3"
        with open(audio_file, "wb") as f:
            f.write(audio_data)

        # Play audio in Streamlit
        st.audio(audio_file, format="audio/mp3")

        # Provide download link
        b64_audio = base64.b64encode(audio_data).decode()
        href = f'<a href="data:audio/mp3;base64,{b64_audio}" download="response.mp3">Download Audio Response</a>'
        st.markdown(href, unsafe_allow_html=True)