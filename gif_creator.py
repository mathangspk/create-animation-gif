from PIL import Image

class GifCreator:
    def __init__(self, images, duration, save_path, loop, resolution=None):
        """
        Initialize with a list of images, duration between frames, the save path for the GIF, loop count, and optional resolution.
        """
        self.images = images
        self.duration = duration
        self.save_path = save_path
        self.loop = loop
        self.resolution = resolution  # Tuple of (width, height) or None

    def create_gif(self):
        """
        Create a GIF from the provided list of images, resizing them if necessary.
        """
        frames = [Image.open(image) for image in self.images]

        # Resize images if a resolution is provided
        if self.resolution:
            width, height = self.resolution
            frames = [frame.resize((width, height), Image.Resampling.LANCZOS) for frame in frames]

        # Save as GIF
        frames[0].save(self.save_path, format='GIF', append_images=frames[1:], save_all=True, duration=self.duration, loop=self.loop)
