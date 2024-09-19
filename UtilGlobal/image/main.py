from PIL import Image, ImageSequence
import io
from django.http import FileResponse





def blur_image(input_path, blur_radius=100, resize_factor=0.5):
    with Image.open(input_path) as img:
        # Resize image to speed up the blur process
        small_img = img.resize(
            (int(img.width * resize_factor), int(img.height * resize_factor))
        )
        blurred_image = small_img.filter(ImageFilter.BoxBlur(blur_radius))
        
        # Optionally, resize back to original size if needed
        blurred_image = blurred_image.resize(img.size)
        # blurred_image.show()


def resize_gif(file, requested_size):
    # Open the image file using Pillow
    with Image.open(file) as img:
        # Ensure the file is a GIF
        if img.format != 'GIF':
            raise ValueError("This function only supports GIF images.")

        frames = []
        width_percent = (requested_size / float(img.width))
        new_height = int((float(img.height) * width_percent))

        # Loop over each frame in the GIF
        for frame in ImageSequence.Iterator(img):
            frame = frame.convert('RGBA')  # Convert to RGBA for transparency handling
            # Resize each frame
            frame = frame.resize((requested_size, new_height), Image.Resampling.NEAREST)
            frames.append(frame)

        # Save the resized frames to an in-memory file
        img_io = io.BytesIO()
        frames[0].save(img_io, format='GIF', save_all=True, append_images=frames[1:], loop=0, duration=img.info['duration'], transparency=img.info.get('transparency', 255))
        img_io.seek(0)

        # Return the resized GIF wrapped in a FileResponse
        return FileResponse(img_io, content_type='image/gif')


def resize_image(file, requested_size):
    # Open the image file using Pillow
    with Image.open(file) as img:
        img_format = img.format
        if img_format == 'GIF':
            return resize_gif(file, requested_size)
        
        # Calculate the aspect ratio to maintain it
        width_percent = (requested_size / float(img.width))
        new_height = int((float(img.height) * width_percent))
        
        # Resize the image
        img = img.resize((requested_size, new_height), Image.Resampling.NEAREST)
        
        # Save the resized image to an in-memory file
        img_io = io.BytesIO()
        img.save(img_io, format=img_format)  # Keep the original format
        img_io.seek(0)  # Seek to the beginning of the file for reading
        
        # Return the resized image wrapped in a FileResponse
        return FileResponse(img_io, content_type=f'image/{img_format.lower()}')
