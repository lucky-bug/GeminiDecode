import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables (likely your Google API key)
load_dotenv()

# Ensure API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key not found in environment variables.")
    st.stop()

genai.configure(api_key=api_key)

def get_gemini_response(input_text, image_data, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([input_text, image_data[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        st.error("No file uploaded")
        st.stop()

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

input_prompt = """
    You are an expert in understanding invoices.
    You will receive input images as invoices &
    you will have to answer questions based on the input image
"""

if submit:
    if uploaded_file:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)
        if response:
            st.subheader("The Response is")
            st.write(response)
    else:
        st.error("Please upload an image before submitting.")
