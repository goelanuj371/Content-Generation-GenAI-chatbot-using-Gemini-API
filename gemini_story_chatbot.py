import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# Set up Gemini API Key
API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=API_KEY)

# Function to generate story
def generate_story(prompt, story_length):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Write a creative story in {story_length} words: {prompt}")
    return response.text if response else "Error: Unable to generate the story."

# Function to load past chats
def load_chats(file_path="past_chats.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

# Function to save new chat
def save_chat(prompt, story, file_path="past_chats.json"):
    chats = load_chats(file_path)
    chats.append({"date": str(datetime.now()), "prompt": prompt, "story": story})
    with open(file_path, "w") as file:
        json.dump(chats, file, indent=4)

# Streamlit UI
st.set_page_config(page_title="Gemini Story Generator", page_icon="📖")
st.title("📖 Smart Story Generator using Gemini API")
st.write("Generate long, creative stories effortlessly!")

# User Input
prompt = st.text_area("Enter a short story idea or plot:", "")
story_length = st.slider("Select story length (number of words):", 100, 1500, 1000)

# Generate Story
if st.button("Generate Story"):
    if prompt:
        st.info("Generating story... Please wait!")
        story = generate_story(prompt, story_length)
        st.success("Here's your generated story:")
        st.write(story)
        save_chat(prompt, story)
    else:
        st.warning("Please enter a story idea to generate a story.")

# Show Past Chats
st.header("🕒 Past Stories")
chats = load_chats()
if chats:
    for i, chat in enumerate(chats[::-1]):
        with st.expander(f"Story {len(chats)-i} - {chat['date']}"):
            st.write(f"**Prompt:** {chat['prompt']}")
            st.write(f"**Story:** {chat['story']}")
else:
    st.info("No past stories found. Generate one to get started!")

st.markdown("---")
st.caption("Powered by Google Gemini API and Streamlit.")
