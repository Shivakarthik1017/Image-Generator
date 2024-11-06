import requests
import io
import streamlit as st
from PIL import Image

# Set up the Streamlit app
st.set_page_config(page_title="Image Generator App", layout="wide")

# Title and basic layout configuration
st.title("Image Generator App")
st.write("Select a category or enter a custom prompt to generate an image.")

# Define the dropdown options for categories and image sizes
category_options = [
    "Food", "Animals", "People", "Music", "Art", "Vehicles", "Random", 
    "Nature", "Travel", "Technology", "Sports", "Fashion", "Architecture", 
    "Fitness", "Education", "Animals (Wildlife)", "Food (Desserts)"
]
size_options = ["small", "medium", "regular", "full"]

# Widgets for category, size, and custom prompt
category = st.selectbox("Select Category", options=["Choose Category"] + category_options)
size = st.selectbox("Select Image Size", options=size_options, index=2)  # Default to "regular" size
prompt = st.text_input("Or enter a custom prompt")

# Function to resize images while maintaining aspect ratio
def resize_image(image, max_size=(800, 600)):
    image.thumbnail(max_size, Image.LANCZOS)
    return image

# Function to retrieve and display the image
def display_image(category, size, prompt):
    try:
        if prompt:
            url = f"https://api.unsplash.com/photos/random?query={prompt}&orientation=landscape&client_id=SouHY7Uul-OxoMl3LL3c0NkxUtjIrKwf3tsGk1JaiVo"
        else:
            url = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id=SouHY7Uul-OxoMl3LL3c0NkxUtjIrKwf3tsGk1JaiVo"
        
        # Retrieve image data
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        img_url = data["urls"][size]
        img_data = requests.get(img_url).content
        
        # Load and resize the image
        img = Image.open(io.BytesIO(img_data))
        img = resize_image(img)

        # Display the image in Streamlit
        st.image(img, caption=f"{prompt or category} Image", use_column_width=True)

        # Option to download the image
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        st.download_button(
            label="Download Image",
            data=img_bytes.getvalue(),
            file_name="generated_image.png",
            mime="image/png"
        )
        
    except requests.exceptions.HTTPError as e:
        st.error(f"Could not retrieve image: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Button to generate the image
if st.button("Generate Image") and (category != "Choose Category" or prompt):
    display_image(category, size, prompt)
else:
    st.write("Please select a category or enter a prompt.")