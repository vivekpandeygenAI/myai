import streamlit as st
import openai
from openai import OpenAI
import speech_recognition as sr
import os

# Set OpenAI API key (replace YOUR_API_KEY with your actual OpenAI key)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Function to capture audio and convert to text
def capture_audio():
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=50, phrase_time_limit=50)
            st.success("Audio captured. Processing...")
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Speech recognition error: {e}")
        return None

# Function to get OpenAI GPT-4 response
def get_response(question,api_key):
    os.environ['OPENAI_API_KEY']=api_key
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",  # Use a specific model, e.g., text-davinci-003
            messages=[
                         {"role": "developer", "content": "You are a helpful interview assistant for Job Role Generative AI Engineer.Give Answer Short Answer with example and key component in max 10 lines."},
                         {"role": "user", "content": question}
                    ]
            )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return None

# Streamlit application
def main():
    st.title("Interview Copilot")
    st.markdown("This application listens to your voice question and provides text-based answers.")

    # Input field for OpenAI API Key
    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    
    if not api_key:
        st.warning("Please enter your OpenAI API key to proceed.")
        return

    if "response" not in st.session_state:
        st.session_state.response = ""

    if st.button("Start"):
        # Capture audio
        user_input = capture_audio()
        if user_input:
            # Get OpenAI response
            response = get_response(user_input,api_key)
            if response:
                st.session_state.response = response

    if st.session_state.response:
        st.markdown("### Copilot's Response:")
        st.write(st.session_state.response)

if __name__ == "__main__":
    main()
