import os
from PIL import Image, ImageDraw, ImageFont

def add_watermark(image, watermark_text="Hippocooking.com"):
    # Get image size
    width, height = image.size

    # Create drawing context
    draw = ImageDraw.Draw(image)

    # Set font size (5% of image height, which is half the original size)
    font_size = int(height * 0.05)  # Half the size of the previous 10% height
    try:
        # Try to load a truetype font
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fall back to default PIL font if arial.ttf is not available
        font = ImageFont.load_default()
    
    # Get text bounding box (used to calculate the size of the watermark)
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Calculate position: slightly above the bottom left corner
    x = 10  # 10 pixels from the left
    y = height - text_height - 30  # 30 pixels from the bottom (upwards from the previous position)

    # Create a new image with RGBA mode (to allow transparency)
    watermark_image = Image.new("RGBA", image.size, (0, 0, 0, 0))  # Transparent background
    watermark_draw = ImageDraw.Draw(watermark_image)

    # Add the watermark text with semi-transparency (alpha = 128)
    watermark_draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))  # semi-transparent white

    # Composite the watermark with the original image
    watermarked_image = Image.alpha_composite(image.convert("RGBA"), watermark_image)

    return watermarked_image.convert("RGB")  # Convert back to RGB to save as JPEG



def scale_image(image, target_width=1080):
    # Get the current width and height of the image
    width, height = image.size
    aspect_ratio = height / width

    # Calculate the new height while keeping the aspect ratio
    new_height = int(target_width * aspect_ratio)

    # Resize image
    scaled_image = image.resize((target_width, new_height), Image.Resampling.LANCZOS)
    
    return scaled_image

def compress_and_save_image(image, output_path, quality=85):
    """
    Save the image with compression for web viewing.
    :param image: Image object to save
    :param output_path: The path where the image should be saved
    :param quality: Compression quality (1-95) for JPEG images
    """
    image.save(output_path, "JPEG", quality=quality, optimize=True)
    print(f"Saved compressed image: {output_path}")

def process_images_in_folder(folder_path):
    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpg'):
            # Build the full image path
            image_path = os.path.join(folder_path, filename)

            # Define the processed image output path
            processed_image_path = os.path.join(folder_path, "p_" + filename)

            # Check if the processed file is a processed image exists
            if filename.lower().startswith('p'):
                print(f"Skipping {filename}, already processed.")
                continue  # Skip processed  image

            # Check if the processed file already exists
            if os.path.exists(processed_image_path):
                print(f"Skipping {filename}, already processed.")
                continue  # Skip processing this image

            # Open the image
            with Image.open(image_path) as img:
                # Scale image
                scaled_img = scale_image(img)

                # Add watermark
                watermarked_img = add_watermark(scaled_img)

                # Compress and save the image for web viewing
                compress_and_save_image(watermarked_img, processed_image_path)

# Specify the folder where your images are located
folder_path = "../../static/recipes_images"  # Replace with the correct folder path
process_images_in_folder(folder_path)
