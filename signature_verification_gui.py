import logging
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image, ImageTk

# Configure logging
logging.basicConfig(filename="app_debug.log", level=logging.DEBUG)

try:
    # Function to load image from file
    def load_image():
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                img = Image.open(file_path)
                img.thumbnail((300, 300))  # Resize to keep it proportional
                img = ImageTk.PhotoImage(img)
                img_label.config(image=img)
                img_label.image = img
                global uploaded_image_path
                uploaded_image_path = file_path
        except Exception as e:
            logging.exception("Error while loading image:")

    # Function to load the template signature
    def load_template():
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                global template_image_path
                template_image_path = file_path
                messagebox.showinfo("Template Loaded", "Template signature loaded successfully.")
        except Exception as e:
            logging.exception("Error while loading template image:")

    # Function to compare images
    def compare_images():
        try:
            if uploaded_image_path and template_image_path:
                uploaded_image = cv2.imread(uploaded_image_path, cv2.IMREAD_GRAYSCALE)
                template_image = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)

                # Resize uploaded image to match template size
                uploaded_image_resized = cv2.resize(uploaded_image, (template_image.shape[1], template_image.shape[0]))

                # Compute SSIM between the images
                similarity_index, _ = ssim(uploaded_image_resized, template_image, full=True)

                # Display result
                if similarity_index > 0.8:  # Threshold of 80% similarity
                    result_label.config(text="Signature Verified!", fg="green")
                else:
                    result_label.config(text="Signature Mismatch!", fg="red")
            else:
                messagebox.showwarning("Missing Data", "Please load both signature and template images.")
        except Exception as e:
            logging.exception("Error while comparing images:")

    # Create the main window
    root = tk.Tk()
    root.title("Offline Signature Verification")

    # Set a fixed window size
    root.geometry("600x500")
    root.config(bg="#f4f4f9")  # Set background color

    # Global variables to store image paths
    uploaded_image_path = None
    template_image_path = None

    # Adding widgets to the window
    frame = tk.Frame(root, bg="#f4f4f9")
    frame.pack(padx=20, pady=20, expand=True, fill='both')

    # Title label
    title_label = tk.Label(frame, text="Offline Signature Verification", font=("Helvetica", 18, "bold"), bg="#f4f4f9")
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    # Upload Signature Button
    upload_button = tk.Button(frame, text="Upload Signature", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=load_image)
    upload_button.grid(row=1, column=0, padx=10, pady=10)

    # Load Template Button
    template_button = tk.Button(frame, text="Load Template Signature", font=("Helvetica", 12), bg="#2196F3", fg="white", command=load_template)
    template_button.grid(row=1, column=1, padx=10, pady=10)

    # Compare Button
    compare_button = tk.Button(frame, text="Compare Signatures", font=("Helvetica", 12, "bold"), bg="#FF9800", fg="white", command=compare_images)
    compare_button.grid(row=1, column=2, padx=10, pady=10)

    # Label to display uploaded image
    img_label = tk.Label(frame, bg="#f4f4f9")
    img_label.grid(row=2, column=0, columnspan=3, pady=20)

    # Result Label (Feedback message)
    result_label = tk.Label(frame, text="", font=("Helvetica", 14, "bold"), bg="#f4f4f9")
    result_label.grid(row=3, column=0, columnspan=3, pady=20)

    # Adding a footer
    footer_label = tk.Label(root, text="© 2025 Signature Verifier Tool", font=("Helvetica", 10), fg="#888", bg="#f4f4f9")
    footer_label.pack(side="bottom", pady=10)

    # Start the Tkinter event loop
    root.mainloop()

except Exception as e:
    logging.exception("An error occurred while running the application:")
