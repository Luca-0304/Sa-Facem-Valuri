from PIL import Image, ImageDraw, ImageFont  #code by @luca 
import os                                    # I know its in english but i want to be abel to sent this so other peopel not just romanians


# Path to the input image
input_image_path = r"File" #path to the file that you want to tunr into ASCII
output_ascii_image_path = r"Output" #location for the file , ir has to end in .png/.jpg

# Expanded set of ASCII characters including space for pure white
ASCII_CHARS = ' 0-+,='

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii(image, ascii_chars):
    pixels = image.getdata()
    ascii_str = "".join([ascii_chars[pixel * len(ascii_chars) // 256] for pixel in pixels])
    return ascii_str

def create_ascii_image(image, original_image, ascii_chars):
    ascii_str = map_pixels_to_ascii(image, ascii_chars)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    
    ascii_img = "\n".join([ascii_str[i:(i + img_width)] for i in range(0, ascii_str_len, img_width)])
    
    # Load a monospaced font
    try:
        font = ImageFont.truetype("cour.ttf", 10)  # Ensure the font file is available
    except Exception as e:
        print(f"Error loading font: {e}")
        font = ImageFont.load_default()
    
    # Calculate character width and height using getbbox
    char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]
    img_height = char_height * (ascii_str_len // img_width)
    
    ascii_image = Image.new("RGB", (img_width * char_width, img_height), "white")
    draw = ImageDraw.Draw(ascii_image)
    
    # Draw ASCII characters with corresponding colors from the original image
    y = 0
    for line in ascii_img.split("\n"):
        x = 0
        for char in line:
            if x // char_width < original_image.width and y // char_height < original_image.height:
                color = original_image.getpixel((x // char_width, y // char_height))
                draw.text((x, y), char, fill=color, font=font)
            x += char_width
        y += char_height
    
    # Draw grid lines for better visibility
    for x in range(0, img_width * char_width, char_width):
        draw.line((x, 0, x, img_height), fill="lightgrey")
    for y in range(0, img_height, char_height):
        draw.line((0, y, img_width * char_width, y), fill="lightgrey")
    
    return ascii_image

def generate_images(image_path, output_ascii_image_path, new_width=100):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}.")
        print(e)
        return
    
    resized_image = resize_image(image, new_width)
    grayscale_image = convert_to_grayscale(resized_image)
    ascii_image = create_ascii_image(grayscale_image, resized_image, ASCII_CHARS)
    
    if ascii_image is not None:
        try:
            ascii_image.save(output_ascii_image_path)
            print(f"ASCII art saved as image to {output_ascii_image_path}")
        except Exception as e:
            print(f"Unable to save image file {output_ascii_image_path}.")
            print(e)

output_dir = os.path.dirname(output_ascii_image_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

generate_images(input_image_path, output_ascii_image_path, new_width=100)
