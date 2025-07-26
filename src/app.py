import streamlit as st
import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file at the very start
load_dotenv()

st.set_page_config(page_title="Smart Recipe Suggester", layout="centered")

# Gemini API Key Configuration (reads from environment variables)
try:
    # Now os.environ.get("GEMINI_API_KEY") will pick up the key from .env
    gemini_api_key_app = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key_app:
        st.error("Error: Gemini API Key is not available for the Streamlit application. "
                 "Please ensure it's set as an environment variable or in a .env file.")
        st.stop()

    genai.configure(api_key=gemini_api_key_app)

except Exception as e:
    st.error(f"Error configuring Gemini API Key in Streamlit: {e}. "
             "Make sure it is correctly defined and accessible.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("👨‍🍳 Hi, I'm Chiller, your AI Recipe Assistant 🥦")
st.markdown("Upload a **photo of the ingredients you have** and discover delicious recipes!")

uploaded_file = st.file_uploader("Upload an image of your ingredients", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Your ingredients image', use_container_width=True)
    st.write("")
    st.info("Analyzing your image with Gemini... Please wait a moment.")

    image = PIL.Image.open(uploaded_file)

    try:
        identification_prompt = (
            f"List in detail and clearly all food ingredients "
            f"you can identify in this image of a refrigerator. "
            f"Separate them by comma and be concise."
        )
        identification_response = model.generate_content([identification_prompt, image])
        ingredients_raw = identification_response.text.strip()
        ingredients_list = [item.strip() for item in ingredients_raw.split(',') if item.strip()]

        if ingredients_list:
            ingredients_str = ', '.join(ingredients_list)
            st.success(f"**Identified Ingredients:** {ingredients_str}")

            st.info("Generating recipe suggestions for you...")
            recipes_prompt = (
                f"With the following ingredients available: {ingredients_str}.\\n"
                f"Suggest 3 creative and simple recipes that can be made with these ingredients.\\n"
                f"For each recipe, provide:\\n"
                f"1. The name of the recipe.\\n"
                f"2. A brief description.\\n"
                f"3. A list of the main ingredients used from this list.\\n"
                f"4. Concise preparation instructions, in step-by-step format."
            )

            recipes_response = model.generate_content([recipes_prompt])
            recipe_suggestions = recipes_response.text.strip()

            st.markdown("---")
            st.subheader("✅ RECIPE SUGGESTIONS FOR YOU ✅")
            st.markdown(recipe_suggestions)

        else:
            st.warning("Could not identify significant ingredients in the image. Try a clearer image or one with more food items.")

    except Exception as e:
        st.error(f"An error occurred while processing your request: {e}")
        st.warning("Please check your API Key and if the image is clear. Ensure that the 'gemini-1.5-flash' model is correct and active.")