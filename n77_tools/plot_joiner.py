from PIL import Image


def trim_image(image, left_offset, right_offset):
    # Get image dimensions
    width, height = image.size    

    # Define bounding box
    bbox = (left_offset, 0, width - right_offset, height)

    # Crop image to bounding box
    cropped_image = image.crop(bbox)

    return cropped_image

def join_images_horizontally(image_paths):
    # Load images
    images = [Image.open(path) for path in image_paths]

    # Trim images
    # trimmed_images = [trim_image(image,0,0) for image in images]
    trimmed_images = [trim_image(image,191,163) for image in images]

    # Get maximum height
    max_height = max(image.height for image in trimmed_images)

    # Resize images to have the same height
    resized_images = [image.resize((image.width, max_height)) for image in trimmed_images]

    # Calculate total width
    total_width = sum(image.width for image in resized_images)

    # Create a new image with the total width and maximum height
    new_image = Image.new('RGB', (total_width, max_height))

    # Paste each image into the new image
    x_offset = 0
    for image in resized_images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.width

    return new_image

# Example usage
start_index = 33  # Start index of the images
end_index = 36   # End index of the images
image_paths = [f'fft_plot_span_{n}.png' for n in range(start_index, end_index + 1)]

joined_image = join_images_horizontally(image_paths)

# Save the joined image
joined_image.save('extract.png')
