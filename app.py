import tkinter as tk
from tkinter import filedialog, messagebox
from gif_creator import GifCreator
from preview_frame import PreviewFrame
from template_manager import TemplateManager
from PIL import Image, ImageTk
import os

class GifCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GIF Creator")

        # List to store selected PNG images
        self.images = []

        # Create the main layout frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10, padx=10)

        # Left frame for the image list and controls
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, padx=10)

        # Right frame for the thumbnail display with a scrollbar
        self.thumbnail_frame = tk.Frame(self.main_frame)
        self.thumbnail_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

        # Add a scrollbar for the thumbnail canvas
        self.scrollbar = tk.Scrollbar(self.thumbnail_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas for displaying thumbnails
        self.thumbnail_canvas = tk.Canvas(self.thumbnail_frame, width=200, height=400, bg="white", yscrollcommand=self.scrollbar.set)
        self.thumbnail_canvas.pack(side=tk.LEFT, fill=tk.Y)

        # Configure the scrollbar
        self.scrollbar.config(command=self.thumbnail_canvas.yview)

        # Create the UI widgets
        self.create_widgets()

        # Initialize preview frame object
        self.preview_frame = PreviewFrame(self.root)

        # Dictionary to store thumbnail references to avoid garbage collection
        self.thumbnails = {}

    def create_widgets(self):
        # Button to add PNG images
        self.add_image_button = tk.Button(self.left_frame, text="Add PNG Images", command=self.add_image)
        self.add_image_button.pack(pady=10)

        # Listbox to display selected images
        self.image_listbox = tk.Listbox(self.left_frame, width=50, height=10)
        self.image_listbox.pack(pady=10)

        # Button to remove selected image
        self.remove_image_button = tk.Button(self.left_frame, text="Remove Selected Image", command=self.remove_image)
        self.remove_image_button.pack(pady=10)

        # Buttons to move images up and down
        self.move_up_button = tk.Button(self.left_frame, text="Move Up", command=self.move_up)
        self.move_up_button.pack(pady=5)

        self.move_down_button = tk.Button(self.left_frame, text="Move Down", command=self.move_down)
        self.move_down_button.pack(pady=5)

        # Entry for duration between frames
        self.duration_label = tk.Label(self.left_frame, text="Duration between frames (ms):")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(self.left_frame)
        self.duration_entry.pack(pady=10)
        self.duration_entry.insert(0, "200")  # Default value

        # Entry for loop count
        self.loop_label = tk.Label(self.left_frame, text="Loop Count (0 for infinite):")
        self.loop_label.pack()
        self.loop_entry = tk.Entry(self.left_frame)
        self.loop_entry.pack(pady=10)
        self.loop_entry.insert(0, "0")  # Default to infinite loop

        # Add dropdown menu for resolution options
        self.resolution_label = tk.Label(self.left_frame, text="Select Resolution:")
        self.resolution_label.pack()

        self.resolutions = ["Original", "640x480", "800x600", "1024x768", "Custom"]
        self.resolution_var = tk.StringVar(self.root)
        self.resolution_var.set(self.resolutions[0])  # Default to "Original"
        self.resolution_menu = tk.OptionMenu(self.left_frame, self.resolution_var, *self.resolutions)
        self.resolution_menu.pack(pady=10)

        # Entries for custom width and height (visible only if "Custom" is selected)
        self.custom_width_label = tk.Label(self.left_frame, text="Custom Width:")
        self.custom_width_entry = tk.Entry(self.left_frame)
        self.custom_height_label = tk.Label(self.left_frame, text="Custom Height:")
        self.custom_height_entry = tk.Entry(self.left_frame)

        # Button to create GIF
        self.create_gif_button = tk.Button(self.left_frame, text="Create GIF", command=self.create_gif)
        self.create_gif_button.pack(pady=10)

        # Button to preview animation
        self.preview_button = tk.Button(self.left_frame, text="Preview Animation", command=self.preview_animation)
        self.preview_button.pack(pady=10)

        # Show or hide custom resolution fields based on dropdown selection
        self.resolution_var.trace("w", self.toggle_custom_resolution_fields)

        # Nút để lưu template
        self.save_template_button = tk.Button(self.left_frame, text="Save Template", command=self.save_template)
        self.save_template_button.pack(pady=10)

        # Nút để mở template
        self.load_template_button = tk.Button(self.left_frame, text="Load Template", command=self.load_template)
        self.load_template_button.pack(pady=10)

    def toggle_custom_resolution_fields(self, *args):
        """
        Show or hide custom width and height fields based on the selected resolution.
        """
        if self.resolution_var.get() == "Custom":
            self.custom_width_label.pack()
            self.custom_width_entry.pack(pady=10)
            self.custom_height_label.pack()
            self.custom_height_entry.pack(pady=10)
        else:
            self.custom_width_label.pack_forget()
            self.custom_width_entry.pack_forget()
            self.custom_height_label.pack_forget()
            self.custom_height_entry.pack_forget()

    def get_resolution(self):
        """
        Return the selected resolution (width, height) based on the user's input.
        """
        resolution = self.resolution_var.get()
        if resolution == "Original":
            return None  # No resizing, use original resolution
        elif resolution == "Custom":
            try:
                width = int(self.custom_width_entry.get())
                height = int(self.custom_height_entry.get())
                return (width, height)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid custom width and height.")
                return None
        else:
            width, height = map(int, resolution.split('x'))
            return (width, height)

    def add_image(self):
        # Open file dialog to select PNG images
        filepaths = filedialog.askopenfilenames(filetypes=[("PNG files", "*.png")])
        if filepaths:
            for filepath in filepaths:
                # Append a unique identifier to the image to differentiate it if added multiple times
                unique_image_id = f"{filepath}__{len(self.images)}"
                self.images.append(unique_image_id)

                # Display the filename in the Listbox
                filename = os.path.basename(filepath)
                self.image_listbox.insert(tk.END, filename)  # Display in Listbox

            # Update the thumbnails
            self.update_thumbnails()

    def remove_image(self):
        """
        Remove the selected image from the listbox and internal image list.
        """
        try:
            # Get the selected image index
            selected_index = self.image_listbox.curselection()[0]
            # Remove from the internal list of images
            self.images.pop(selected_index)
            # Remove from the Listbox
            self.image_listbox.delete(selected_index)

            # Update the thumbnails
            self.update_thumbnails()
        except IndexError:
            messagebox.showerror("Error", "No image selected to remove!")

    def update_thumbnails(self):
        """
        Update the thumbnail display when images are added or removed.
        """
        self.thumbnail_canvas.delete("all")  # Clear previous thumbnails
        self.thumbnails.clear()  # Clear references to old thumbnails

        # Generate and display thumbnails
        for idx, img_path in enumerate(self.images):
            # Extract the original filepath by removing the unique identifier
            original_img_path = img_path.split('__')[0]
            thumbnail = Image.open(original_img_path)
            thumbnail.thumbnail((100, 100))  # Create a thumbnail of max size 100x100
            thumbnail_img = ImageTk.PhotoImage(thumbnail)

            # Save the reference to avoid garbage collection
            self.thumbnails[img_path] = thumbnail_img

            # Calculate position for thumbnail in canvas (centered horizontally)
            canvas_width = self.thumbnail_canvas.winfo_width()
            x = (canvas_width - 100) // 2  # Center horizontally in the canvas
            y = idx * 110  # Spacing between thumbnails

            # Display thumbnail in the canvas
            self.thumbnail_canvas.create_image(x, y, anchor=tk.NW, image=thumbnail_img)

        # Update scroll region to fit all thumbnails
        self.thumbnail_canvas.config(scrollregion=self.thumbnail_canvas.bbox("all"))

    def move_up(self):
        """
        Move the selected image up in the list.
        """
        try:
            selected_index = self.image_listbox.curselection()[0]
            if selected_index == 0:
                return  # Can't move the first item up
            # Swap images in the internal list
            self.images[selected_index], self.images[selected_index - 1] = self.images[selected_index - 1], self.images[selected_index]
            # Update Listbox display
            self.update_listbox()
            self.image_listbox.select_set(selected_index - 1)  # Select the moved item

            # Update thumbnails
            self.update_thumbnails()
        except IndexError:
            messagebox.showerror("Error", "No image selected to move!")

    def move_down(self):
        """
        Move the selected image down in the list.
        """
        try:
            selected_index = self.image_listbox.curselection()[0]
            if selected_index == len(self.images) - 1:
                return  # Can't move the last item down
            # Swap images in the internal list
            self.images[selected_index], self.images[selected_index + 1] = self.images[selected_index + 1], self.images[selected_index]
            # Update Listbox display
            self.update_listbox()
            self.image_listbox.select_set(selected_index + 1)  # Select the moved item

            # Update thumbnails
            self.update_thumbnails()
        except IndexError:
            messagebox.showerror("Error", "No image selected to move!")

    def update_listbox(self):
        """
        Helper function to update the Listbox display after reordering.
        """
        self.image_listbox.delete(0, tk.END)  # Clear current list
        for image in self.images:
            # Display only the filename in the Listbox (without the unique identifier)
            original_filename = os.path.basename(image.split('__')[0])
            self.image_listbox.insert(tk.END, original_filename)  # Insert new ordered list

    def create_gif(self):
        # Validate if images are added
        if not self.images:
            messagebox.showerror("Error", "You need to add at least one PNG image!")
            return

        # Validate the entered duration
        try:
            duration = int(self.duration_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Duration must be a valid integer!")
            return

        # Validate the loop count
        try:
            loop_count = int(self.loop_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Loop count must be a valid integer!")
            return

        # Open save dialog for saving GIF
        save_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
        if not save_path:
            return

        # Call the GifCreator to create the GIF
        gif_creator = GifCreator([img.split('__')[0] for img in self.images], duration, save_path, loop_count)
        gif_creator.create_gif()

        messagebox.showinfo("Success", f"GIF successfully created at {save_path}")

    def preview_animation(self):
        # Preview the animation inside the preview frame
        resolution = self.get_resolution()  # Get the selected resolution
        if self.images:
            self.preview_frame.show_preview([img.split('__')[0] for img in self.images], int(self.duration_entry.get()), resolution)
    
    def save_template(self):
        # Thu thập thông tin từ giao diện người dùng
        images = self.images
        duration = self.duration_entry.get()
        loop = self.loop_entry.get()
        resolution = self.resolution_var.get()

        # Lấy thông tin custom resolution nếu được chọn
        custom_width = self.custom_width_entry.get() if resolution == "Custom" else ""
        custom_height = self.custom_height_entry.get() if resolution == "Custom" else ""

        # Gọi TemplateManager để lưu template
        TemplateManager.save_template(images, duration, loop, resolution, custom_width, custom_height)

    def load_template(self):
        # Gọi TemplateManager để mở template
        template_data = TemplateManager.load_template()

        if template_data:
            # Khôi phục lại trạng thái từ file template
            self.images = template_data.get("images", [])
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, template_data.get("duration", "200"))

            self.loop_entry.delete(0, tk.END)
            self.loop_entry.insert(0, template_data.get("loop", "0"))

            resolution = template_data.get("resolution", "Original")
            self.resolution_var.set(resolution)

            if resolution == "Custom":
                self.custom_width_entry.delete(0, tk.END)
                self.custom_width_entry.insert(0, template_data.get("custom_width", ""))

                self.custom_height_entry.delete(0, tk.END)
                self.custom_height_entry.insert(0, template_data.get("custom_height", ""))

            # Cập nhật lại Listbox và thumbnail
            self.update_listbox()
            self.update_thumbnails()

            messagebox.showinfo("Success", "Template loaded successfully!")


# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = GifCreatorApp(root)
    root.mainloop()
