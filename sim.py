#!/usr/bin/env python3
from google import genai
from google.genai import types
from PIL import Image
import os
import re

# Set up API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

client = genai.Client(api_key=api_key)

# Read prompts from input.txt
try:
    with open('input.txt', 'r') as file:
        prompts = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    raise FileNotFoundError("input.txt file not found")

modelname="imagen-3.0-generate-002"
#modelname="imagen-4.0-ultra-generate-exp-05-20"
#modelname="imagen-4-0-generate-preview-05-20"
# Process each prompt
for prompt in prompts:
    # Create filename from first 5 words (or fewer if prompt is shorter)
    words = re.sub(r'[^\w\s]', '', prompt.lower()).split()
    fname_words = words[:5]
    fname = '_'.join(fname_words) + '.png'
    
    print(f"Processing prompt: {prompt}")
    print(f"Saving as: {fname}")
    
    # Generate image
    response = client.models.generate_images(
        model=modelname,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            aspect_ratio="9:16",
            number_of_images=1
        )
    )
    
    # Save image
    image = response.generated_images[0].image
    image.save(fname)
    print(f"Image saved as {fname}")
