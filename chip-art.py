import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

def process_image(input_path, threshold_value):
    # Read the input image
    input_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Apply image processing with the specified threshold
    _, binary_image = cv2.threshold(input_image, threshold_value, 255, cv2.THRESH_BINARY)

    return input_image, binary_image

def scan_image_to_file(binary_image, output_file):
    # Get the height and width of the image
    height, width = binary_image.shape

    # Open the file in write mode
    with open(output_file, 'w') as file:
        # Scan the binary image from top to bottom
        for y in range(height):
            for x in range(width):
                # Get the pixel value (1 or 0) and write it to the file
                pixel_value = binary_image[y, x]
                file.write(str(pixel_value) + ' ')
            file.write('\n')  # Move to the next line after scanning a row

def show_images(input_image, binary_image):
    # Create a Tkinter window
    window = tk.Tk()
    window.title("Image Viewer")

    # Convert OpenCV images to PIL format
    input_image_pil = Image.fromarray(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB))
    binary_image_pil = Image.fromarray(binary_image)

    # Convert PIL images to Tkinter PhotoImage
    input_image_tk = ImageTk.PhotoImage(input_image_pil)
    binary_image_tk = ImageTk.PhotoImage(binary_image_pil)

    # Create labels to display images
    input_label = tk.Label(window, image=input_image_tk)
    binary_label = tk.Label(window, image=binary_image_tk)

    # Pack labels into the window
    input_label.pack(side="left", padx=10)
    binary_label.pack(side="right", padx=10)

    # Run the Tkinter event loop
    window.mainloop()

def on_threshold_change(*args):
    # Function to update the threshold label when the threshold changes
    threshold_value = int(threshold_var.get())
    threshold_label.config(text=f"Threshold value: {threshold_value}")

def open_image():
    global input_path
    input_path = filedialog.askopenfilename(title="Select an Image File", filetypes=[("Image files", "*.jpg;*.png")])

    if input_path:
        # Enable the slider when an image is selected
        threshold_slider.config(state="normal")

        # Process the image and display it
        threshold_value = int(threshold_var.get())
        input_image, binary_image = process_image(input_path, threshold_value)
        show_images(input_image, binary_image)

        # Update the threshold label with the current threshold value
        threshold_label.config(text=f"Threshold value: {threshold_value}")

def process_and_show_image():
    # Function to process the image and display it
    threshold_value = int(threshold_var.get())
    input_image, binary_image = process_image(input_path, threshold_value)
    show_images(input_image, binary_image)

if __name__ == "__main__":
    # Initialize the global input_path variable
    input_path = ""

    # Create a Tkinter window for the threshold input
    threshold_window = tk.Tk()
    threshold_window.title("Threshold Input")

    # Add a slider for the threshold (initially disabled)
    threshold_var = tk.DoubleVar()
    threshold_var.set(127)  # Default threshold value
    threshold_slider = ttk.Scale(threshold_window, from_=0, to=255, variable=threshold_var, orient="horizontal", length=200, state="disabled")
    threshold_slider.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Add a label for the threshold slider
    threshold_label = ttk.Label(threshold_window, text=f"Threshold value: {int(threshold_var.get())}")
    threshold_label.grid(row=1, column=0, columnspan=2, pady=5)

    # Add a button to open the image
    open_image_button = ttk.Button(threshold_window, text="Open Image", command=open_image)
    open_image_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Add a button to process the image
    process_image_button = ttk.Button(threshold_window, text="Process Image", command=process_and_show_image)
    process_image_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Bind the function to update the threshold label when the threshold changes
    threshold_var.trace_add("write", on_threshold_change)

    # Run the Tkinter event loop for the threshold input window
    threshold_window.mainloop()

    # Get the final threshold value
    threshold_value = int(threshold_var.get())

    # Process the image and generate a binary image with the specified threshold
    if input_path:
        input_image, binary_image = process_image(input_path, threshold_value)

        # Specify the output file path
        output_file = "output.txt"

        # Scan the binary image and write the pixel values to a text file
        scan_image_to_file(binary_image, output_file)

        # Show the input and binary images in a graphical interface
        show_images(input_image, binary_image)
