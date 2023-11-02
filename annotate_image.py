import subprocess
import argparse

def annotate_image(input_image, output_image, annotation_text, font="Arial", font_size=50, text_color="black", background_color="white", bar_height=50):
    # Build the convert command
    command = [
        "convert",            # Command name
        input_image,          # Input image
        "-font", font,        # Font choice
        "-pointsize", str(font_size),  # Font size
        "-fill", text_color,  # Text color
        "-background", background_color,  # Background color
        "-gravity", "South",  # Text position (bottom of image)
        f"label:{annotation_text}",  # The text to annotate
        "+repage",            # Remove page information
        "-size", f"{bar_height}x",  # Size of the background bar (width x height)
        "xc:white",           # Create a white canvas of the specified size
        "-append",            # Append the canvas and the annotated image
        output_image          # Output image
    ]

    # Execute the command
    subprocess.run(command)

    print(f"Image annotated and saved as {output_image}")

if __name__ == "__main__":
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="Annotate an image with text")

    # Add arguments for input and output images
    parser.add_argument("input_image", help="Input image filename")
    parser.add_argument("output_image", help="Output image filename")
    parser.add_argument("annotation_text", help="Text to annotate")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the annotate_image function with the provided arguments
    annotate_image(args.input_image, args.output_image, args.annotation_text)
