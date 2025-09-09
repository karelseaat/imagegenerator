#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
import random
import os
import argparse

def _get_image_paths(folder_path):
    """Returns a list of image file paths from the given folder."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder not found: {folder_path}")
        return []
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(folder_path, f))
    ]

def _colorize_image(image, new_color):
    """Recolors the non-transparent parts of an image to a new color."""
    if not new_color:
        return image
        
    colorized_image = image.copy()
    pixels = colorized_image.load()
    
    for y in range(colorized_image.height):
        for x in range(colorized_image.width):
            r, g, b, a = pixels[x, y]
            if a > 0:
                pixels[x, y] = (new_color[0], new_color[1], new_color[2], a)
                
    return colorized_image

def _align_fg_bottom(image_to_align, reference_image):
    """Aligns the subject of an image horizontally centered and vertically to the bottom."""
    try:
        bbox = image_to_align.getbbox()
        if not bbox:
            return image_to_align # No subject found

        # Horizontal centering
        paste_x = int((reference_image.width - image_to_align.width) / 2)

        # Vertical alignment to bottom
        subject_bottom = bbox[3]
        canvas_bottom = reference_image.height
        paste_y = int(canvas_bottom - subject_bottom)

        aligned_image = Image.new('RGBA', reference_image.size, (0, 0, 0, 0))
        aligned_image.paste(image_to_align, (paste_x, paste_y))
        
        return aligned_image
    except Exception as e:
        print(f"Warning: Could not align image. Error: {e}")
        return image_to_align

def _load_and_resize_images(bg_path, mg_path, fg_path, bg_color, mg_color, fg_color):
    """Loads, colorizes, and resizes images."""
    try:
        bg_img = Image.open(bg_path).convert("RGBA")
        mg_img = Image.open(mg_path).convert("RGBA")
        fg_img = Image.open(fg_path).convert("RGBA")

        # Randomly mirror images
        if random.choice([True, False]):
            bg_img = bg_img.transpose(Image.FLIP_LEFT_RIGHT)
        if random.choice([True, False]):
            mg_img = mg_img.transpose(Image.FLIP_LEFT_RIGHT)
        if random.choice([True, False]):
            fg_img = fg_img.transpose(Image.FLIP_LEFT_RIGHT)

        bg_img = _colorize_image(bg_img, bg_color)
        mg_img = _colorize_image(mg_img, mg_color)
        fg_img = _colorize_image(fg_img, fg_color)

        # Resize foreground so its height is 2/3 of the background's height
        original_fg_width, original_fg_height = fg_img.size
        aspect_ratio = original_fg_width / original_fg_height
        
        target_height = int(bg_img.height * (2/3))
        target_width = int(target_height * aspect_ratio)
        
        fg_img = fg_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # Resize midground to background size
        mg_img = mg_img.resize(bg_img.size, Image.Resampling.LANCZOS)
        return bg_img, mg_img, fg_img
    except FileNotFoundError as e:
        print(f"Error opening image: {e}. Check paths.")
        return None, None, None
    except Exception as e:
        print(f"An unexpected error occurred loading images: {e}")
        return None, None, None

def _composite_images(bg_img, mg_img, fg_img):
    """Composites the three images onto a single canvas."""
    combined_img = Image.new("RGBA", bg_img.size)
    combined_img = Image.alpha_composite(combined_img, bg_img)
    combined_img = Image.alpha_composite(combined_img, mg_img)
    combined_img = Image.alpha_composite(combined_img, fg_img)
    return combined_img

def _find_system_font():
    """Tries to find a common system font."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
        "/usr/share/fonts/truetype/verdana/Verdana.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return path
    return None

def _add_text_to_image(image, text, color, font_path, font_size, text_position="bottom-center"):
    """Adds text to the given image."""
    draw = ImageDraw.Draw(image)
    
    font_to_use = None
    
    # 1. Try user-provided font path first
    if font_path and os.path.exists(font_path):
        try:
            font_to_use = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Warning: Could not load font from {font_path}. Trying system fonts.")

    # 2. If no user font, try to find a common system font
    if not font_to_use:
        system_font_path = _find_system_font()
        if system_font_path:
            try:
                font_to_use = ImageFont.truetype(system_font_path, font_size)
            except IOError:
                print(f"Warning: Could not load system font {system_font_path}. Using default.")

    # 3. As a last resort, use the default font
    if not font_to_use:
        print("Warning: No suitable font found. Using default, fixed-size font.")
        font_to_use = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), text, font=font_to_use)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    positions = {
        "top-left": (20, 20),
        "top-center": ((image.width - text_width) / 2, 20),
        "top-right": (image.width - text_width - 20, 20),
        "center-left": (20, (image.height - text_height) / 2),
        "center": ((image.width - text_width) / 2, (image.height - text_height) / 2),
        "center-right": (image.width - text_width - 20, (image.height - text_height) / 2),
        "bottom-left": (20, image.height - text_height - 20),
        "bottom-center": ((image.width - text_width) / 2, image.height - text_height - 20),
        "bottom-right": (image.width - text_width - 20, image.height - text_height - 20),
    }

    text_x, text_y = positions.get(text_position, positions["bottom-center"])

    if ',' in text_position:
        try:
            x, y = map(int, text_position.split(','))
            text_x, text_y = x, y
        except ValueError:
            print("Warning: Invalid coordinate format for text_position. Using default.")
            text_x, text_y = positions["bottom-center"]

    draw.text((text_x, text_y), text, font=font_to_use, fill=color)
    return image

def generate_combined_image(
    background_folder="background",
    midground_folder="midground",
    foreground_folder="foreground",
    output_folder="combined_images",
    text_to_add="Combined Image",
    text_color=(255, 255, 255),
    font_path=None,
    font_size=50,
    text_position="bottom-center",
    bg_color=None,
    mg_color=None,
    fg_color=None,
    align_fg_bottom=False
):
    """
    Randomly combines images from specified folders and adds text.
    The output is saved in 'output_folder' relative to the script's location.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_output_path = os.path.join(script_dir, output_folder)
    os.makedirs(full_output_path, exist_ok=True) # Create output folder if it doesn't exist

    bg_paths = _get_image_paths(os.path.join(script_dir, background_folder))
    mg_paths = _get_image_paths(os.path.join(script_dir, midground_folder))
    fg_paths = _get_image_paths(os.path.join(script_dir, foreground_folder))

    if not (bg_paths and mg_paths and fg_paths):
        print("Error: Ensure all background, midground, and foreground folders contain images.")
        return

    # Randomly select and load images
    bg_img, mg_img, fg_img = _load_and_resize_images(
        random.choice(bg_paths),
        random.choice(mg_paths),
        random.choice(fg_paths),
        bg_color, mg_color, fg_color
    )

    if not all([bg_img, mg_img, fg_img]):
        print("Failed to load one or more images. Aborting.")
        return

    if align_fg_bottom:
        fg_img = _align_fg_bottom(fg_img, bg_img)
    else:
        # Default behavior: place fg at top-center on a canvas of bg_img's size
        fg_canvas = Image.new('RGBA', bg_img.size, (0, 0, 0, 0))
        paste_x = int((bg_img.width - fg_img.width) / 2)
        fg_canvas.paste(fg_img, (paste_x, 0))
        fg_img = fg_canvas

    # Composite and add text
    combined_img = _composite_images(bg_img, mg_img, fg_img)
    final_img = _add_text_to_image(combined_img, text_to_add, text_color, font_path, font_size, text_position)

    # Save the result
    timestamp = random.randint(1000, 9999)
    output_filename = f"combined_{timestamp}.png"
    output_path = os.path.join(full_output_path, output_filename)
    final_img.save(output_path)
    print(f"Combined image saved to: {output_path}")



### How to Use:


#### Example Call (within `if __name__ == "__main__":` block):

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine images and add text.")
    parser.add_argument("--text", default="Hello World!", help="Text to add to the image.")
    parser.add_argument("--color", default="255,255,0", help="Text color as an RGB string, e.g., '255,255,0'.")
    parser.add_argument("--font_size", type=int, default=70, help="Font size.")
    parser.add_argument("--font_path", help="Path to a .ttf font file.")
    parser.add_argument("--text-position", default="bottom-center", help="Position of the text. E.g., 'top-left', 'center', or coordinates like '100,150'.")
    parser.add_argument("--fg-color", help="Color for the foreground image subject.")
    parser.add_argument("--mg-color", help="Color for the midground image subject.")
    parser.add_argument("--bg-color", help="Color for the background image subject.")
    parser.add_argument("--count", type=int, default=1, help="Number of images to generate.")
    parser.add_argument("--align-fg-bottom", action="store_true", help="Align the foreground subject to the bottom of the image.")
    args = parser.parse_args()

    def parse_color(color_str):
        if not color_str:
            return None
        try:
            color_tuple = tuple(map(int, color_str.split(',')))
            if len(color_tuple) != 3:
                raise ValueError
            return color_tuple
        except (ValueError, AttributeError):
            print(f"Warning: Invalid color format for '{color_str}'. Ignoring.")
            return None

    text_color = parse_color(args.color)
    if not text_color:
        text_color = (255, 255, 0) # Default if parsing fails

    fg_color = parse_color(args.fg_color)
    mg_color = parse_color(args.mg_color)
    bg_color = parse_color(args.bg_color)

    # --- Optional: Setup dummy images for first run if you don't have real ones yet ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for folder_name in ["background", "midground", "foreground"]:
        path = os.path.join(script_dir, folder_name)
        os.makedirs(path, exist_ok=True)
        # Create a simple dummy image for each folder
        if not os.listdir(path): # Only create if folder is empty
            color = tuple(random.randint(0, 255) for _ in range(3)) + (255,) if folder_name == "background" else tuple(random.randint(0, 255) for _ in range(3)) + (128,)
            Image.new('RGBA', (800, 600), color=color).save(os.path.join(path, f'{folder_name}_dummy.png'))
    # --- End of Optional Setup ---

    for _ in range(args.count):
        generate_combined_image(
            text_to_add=args.text,
            text_color=text_color,
            font_size=args.font_size,
            font_path=args.font_path,
            text_position=args.text_position,
            fg_color=fg_color,
            mg_color=mg_color,
            bg_color=bg_color,
            align_fg_bottom=args.align_fg_bottom
        )
