import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
from io import BytesIO
import base64
import time

# Set page configuration
st.set_page_config(
    page_title="Voice Assistant",
    page_icon="🗣️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .assistant-response {
        background-color: #f0f2;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .user-input {
        background-color: #e6ff;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        width: 100%;
        background-color: #17b4;
        color: white;
    }
    .feature-card {
        background-color: #f9f9;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'listening' not in st.session_state:
    st.session_state.listening = False
if 'speaking' not in st.session_state:
    st.session_state.speaking = False

# Function to speak text
def speak(text):
    st.session_state.speaking = True
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
    finally:
        st.session_state.speaking = False

# Function to wish the user based on time of day
def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        return "Good Morning!"
    elif hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

# Function to process commands
def process_command(query):
    response = ""
    
    if 'wikipedia' in query:
        response += "Searching Wikipedia... "
        query = query.replace("wikipedia", "")
        try:
            result = wikipedia.summary(query, sentences=2)
            response += "According to Wikipedia: " + result
        except:
            response += "Sorry, I couldn't find anything on Wikipedia."
            
    elif 'open youtube' in query:
        response = "Opening YouTube..."
        webbrowser.open("https://www.youtube.com/")
        
    elif 'open google' in query:
        response = "Opening Google..."
        webbrowser.open("https://www.google.com/")
        
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {strTime}"
        
    elif 'joke' in query:
        joke = pyjokes.get_joke()
        response = joke
        
    elif 'exit' in query or 'bye' in query:
        response = "Goodbye! Have a nice day!"
        
    else:
        response = "I'm not sure how to help with that. Try asking me to search Wikipedia, tell a joke, or open YouTube or Google."
    
    return response

# Function to record audio
def record_audio():
    st.session_state.listening = True
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        st.info("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        query = recognizer.recognize_google(audio)
        st.session_state.conversation.append(("You", query))
        return query.lower()
    except sr.UnknownValueError:
        st.error("Could not understand audio")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
        return ""
    finally:
        st.session_state.listening = False

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🗣️ Voice Assistant</h1>', unsafe_allow_html=True)
    
    # Introduction
    greeting = wish_user()
    st.markdown(f'<div class="assistant-response">🤖: {greeting} I am your voice assistant. How can I help you today?</div>', unsafe_allow_html=True)
    
    # Display conversation history
    for speaker, text in st.session_state.conversation:
        if speaker == "You":
            st.markdown(f'<div class="user-input">👤 {speaker}: {text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-response">🤖 {speaker}: {text}</div>', unsafe_allow_html=True)
    
    # Input methods
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Made by Subhadip")
        
    with col2:
        text_input = st.text_input("Or type your command here:", key="text_input")
        if st.button("Submit Text Command") and text_input:
            st.session_state.conversation.append(("You", text_input))
            response = process_command(text_input.lower())
            st.session_state.conversation.append(("Assistant", response))
            st.rerun()
    
    # Speak the last assistant response if available
    if st.session_state.conversation and st.session_state.conversation[-1][0] == "Assistant":
        if st.button("🔊 Speak Response") and not st.session_state.speaking:
            speak(st.session_state.conversation[-1][1])
    
    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.conversation = []
        st.rerun()
    
    # Features section
    st.markdown("---")
    st.subheader("What I can do:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="feature-card">🔍 Wikipedia Search<br><small>Try: "Search Wikipedia for artificial intelligence"</small></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">⏰ Time Check<br><small>Try: "What time is it?"</small></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-card">😂 Tell a Joke<br><small>Try: "Tell me a joke"</small></div>', unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown('<div class="feature-card">📺 Open YouTube<br><small>Try: "Open YouTube"</small></div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="feature-card">🌐 Open Google<br><small>Try: "Open Google"</small></div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="feature-card">👋 Exit<br><small>Try: "Goodbye" or "Exit"</small></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()