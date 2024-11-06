import requests
import io
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style
import threading

# create the main window
root = tk.Tk()
root.title("Image Generator App")  # Set the window title
root.attributes("-fullscreen", True)  # Set full screen
root.config(bg="#f0f0f0")  # Light gray background
style = Style(theme="flatly")  # Modern theme

# global variables
loading_label = None
image_label = None  # To store the image label
current_image = None  # To store the original PIL image

# function to resize images while maintaining aspect ratio
def resize_image(image, max_size):
    image.thumbnail(max_size, Image.LANCZOS)  # Use LANCZOS for high-quality resizing
    return image

# define a function to retrieve and display an image based on the selected category or custom prompt
def display_image(category, size, prompt):
    global loading_label, image_label, current_image
    loading_label.config(text="Loading...", fg="blue")
    loading_label.update()
    
    try:
        if prompt:  # Use prompt if provided
            url = f"https://api.unsplash.com/photos/random?query={prompt}&orientation=landscape&client_id=SouHY7Uul-OxoMl3LL3c0NkxUtjIrKwf3tsGk1JaiVo"
        else:  # Use category if no prompt
            url = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id=SouHY7Uul-OxoMl3LL3c0NkxUtjIrKwf3tsGk1JaiVo"
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        data = response.json()
        img_url = data["urls"][size]
        img_data = requests.get(img_url).content

        # Load the image and resize
        img = Image.open(io.BytesIO(img_data))
        img = resize_image(img, (800, 600))  # Adjust size for better display in full screen
        current_image = img
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo

        loading_label.config(text="")
    except requests.exceptions.HTTPError as e:
        loading_label.config(text="")
        messagebox.showerror("Error", f"Could not retrieve image: {e}")
    except Exception as e:
        loading_label.config(text="")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# function to enable/disable the "Generate Image" button
def enable_button(*args):
    generate_button.config(state="normal" if category_var.get() != "Choose Category" or prompt_entry.get() else "disabled")

# function to save the displayed image
def save_image():
    if current_image:
        current_image.save("saved_image.png")  # Save the image as PNG
        messagebox.showinfo("Saved", "Image saved as 'saved_image.png'.")
    else:
        messagebox.showwarning("Warning", "No image to save.")

# function to exit the application
def close_app():
    root.attributes("-fullscreen", False)  # Exit full screen
    root.quit()

# create the GUI elements
def create_gui():
    global category_var, generate_button, loading_label, prompt_entry, image_label

    # Create a frame for controls
    control_frame = ttk.Frame(root, padding="10")
    control_frame.grid(row=0, column=0, sticky="nsew")

    # create a dropdown menu for selecting the category
    category_var = tk.StringVar(value="Choose Category")
    category_options = [
        "Choose Category", 
        "Food", 
        "Animals", 
        "People", 
        "Music", 
        "Art", 
        "Vehicles", 
        "Random", 
        "Nature", 
        "Travel", 
        "Technology", 
        "Sports", 
        "Fashion", 
        "Architecture", 
        "Fitness", 
        "Education", 
        "Animals (Wildlife)", 
        "Food (Desserts)"
    ]
    category_dropdown = ttk.OptionMenu(control_frame, category_var, *category_options, command=enable_button)
    category_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    category_dropdown.config(width=20)

    # create a dropdown menu for selecting image size
    size_var = tk.StringVar(value="regular")
    size_options = ["small", "medium", "regular", "full"]
    size_dropdown = ttk.OptionMenu(control_frame, size_var, *size_options)
    size_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    size_dropdown.config(width=20)

    # entry for custom prompt
    prompt_entry = tk.Entry(control_frame, width=20)
    prompt_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    prompt_entry.bind("<KeyRelease>", enable_button)  # Enable button when typing in prompt

    # create a button for generating the image
    generate_button = ttk.Button(
        control_frame,
        text="Generate Image", 
        state="disabled", 
        command=lambda: threading.Thread(target=display_image, args=(category_var.get(), size_var.get(), prompt_entry.get())).start()
    )
    generate_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")  # Normal padding
    generate_button.config(width=10)  # Normal width

    # create a button for saving the image
    save_button = ttk.Button(control_frame, text="Save Image", command=save_image)
    save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")  # Normal padding
    save_button.config(width=10)  # Normal width

    # create a button for closing the app
    close_button = ttk.Button(control_frame, text="Close", command=close_app)
    close_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")  # Normal padding
    close_button.config(width=10)  # Normal width

    # loading label
    loading_label = tk.Label(root, background="#f0f0f0", font=("Arial", 10))
    loading_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # create a label for displaying the image
    image_label = tk.Label(root, background="#f0f0f0")
    image_label.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # make the columns/rows expandable
    root.columnconfigure(0, weight=1)
    root.rowconfigure([0, 1, 2], weight=1)
    root.mainloop()

if __name__ == '__main__':
    create_gui()
