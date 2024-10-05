import streamlit as st
from google.generativeai import GenerativeModel
import google.generativeai as genai

api_key=st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)  # Loading the API key into the generativeai module

# Initialize the Gemini model
model = GenerativeModel('models/gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize conversation history in Streamlit's session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to get a response from the Gemini model
def get_response(conversation):
    response = model.generate_content(contents=conversation)
    return response.text

# Display the conversation history using Streamlit's chat interface
for message in st.session_state.conversation:
    with st.chat_message(translate_role_for_streamlit(message["role"])):
        st.write(" ".join(message["parts"]))

# Create a chat input widget to get user input
if user_input := st.chat_input("You: "):
    # Add user message to the conversation history
    st.session_state.conversation.append({'role': 'user', 'parts': [user_input]})

    # Display user's message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # Generate and display the AI's response
    with st.chat_message("model"):
        with st.spinner("Gemini is thinking..."):
            ai_response = get_response(st.session_state.conversation)
            st.write(ai_response)

    # Add AI response to conversation history
    st.session_state.conversation.append({'role': 'model', 'parts': [ai_response]})
