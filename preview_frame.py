import tkinter as tk
from PIL import Image, ImageTk

class PreviewFrame:
    def __init__(self, root):
        """
        Initialize the preview frame within the root window.
        """
        self.root = root
        self.preview_window = None
        self.canvas = None
        self.tk_frames = []
        self.current_frame = 0
        self.duration = 200  # Default duration

    def show_preview(self, images, duration, resolution=None):
        """
        Show a preview of the GIF by displaying each image in sequence, with optional resizing.
        """
        # Close any existing preview window before opening a new one
        if self.preview_window:
            self.preview_window.destroy()
            self.preview_window = None

        # Create a new preview window
        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("GIF Preview")

        self.canvas = tk.Canvas(self.preview_window, width=400, height=300)
        self.canvas.pack()

        self.duration = duration  # Set duration between frames
        self.frames = [Image.open(image) for image in images]  # Load all images

        # Resize images based on the selected resolution
        if resolution:
            width, height = resolution
            self.frames = [frame.resize((width, height), Image.Resampling.LANCZOS) for frame in self.frames]

        self.tk_frames = [ImageTk.PhotoImage(frame) for frame in self.frames]  # Convert to Tkinter-compatible images

        # Set the canvas size based on the first image's dimensions
        self.canvas.config(width=self.frames[0].width, height=self.frames[0].height)

        # Start the animation
        self.current_frame = 0  # Reset frame index
        self.display_frame()

    def display_frame(self):
        """
        Display the current frame and recursively call itself to display the next one.
        """
        if self.tk_frames:
            # Display the current frame on the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_frames[self.current_frame])

            # Update the current frame index (loop back to start if necessary)
            self.current_frame = (self.current_frame + 1) % len(self.tk_frames)

            # Call this function again after 'duration' milliseconds for the next frame
            self.preview_window.after(self.duration, self.display_frame)
