#!/usr/bin/env python3
from google import genai
from google.genai import types
from PIL import Image
import os
import re
import random

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
#modelname="imagen-4.0-generate-preview-06-06"
#modelname="imagen-4-0-generate-preview-05-20"

# Process each prompt
for prompt in prompts:
    # Create filename from first 7 words + 2 random words from the rest
    words = re.sub(r'[^\w\s]', '', prompt.lower()).split()
    
    if len(words) <= 7:
        # If prompt has 7 or fewer words, use all of them
        fname_words = words
    else:
        # Take first 7 words
        fname_words = words[:7]
        
        # Get remaining words (after first 7)
        remaining_words = words[7:]
        
        # Randomly select up to 2 words from remaining words
        if remaining_words:
            num_random = min(2, len(remaining_words))
            random_words = random.sample(remaining_words, num_random)
            fname_words.extend(random_words)
    
    fname = '_'.join(fname_words) + '.png'
    
    print(f"Processing prompt: {prompt}")
    print(f"Saving as: {fname}")
    
    try:
        # Generate image
        response = client.models.generate_images(
            model=modelname,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                aspect_ratio="16:9",
                number_of_images=1
            )
        )
        
        # Check if response is valid and has generated images
        if not response or not hasattr(response, 'generated_images') or not response.generated_images:
            print(f"❌ No images generated for prompt: {prompt}")
            continue
            
        # Check if the first image exists and has an image attribute
        if not response.generated_images[0] or not hasattr(response.generated_images[0], 'image'):
            print(f"❌ Invalid image data for prompt: {prompt}")
            continue
            
        # Save image
        image = response.generated_images[0].image
        if image is None:
            print(f"❌ Image is None for prompt: {prompt}")
            continue
            
        image.save(fname)
        print(f"✅ Image saved as {fname}")
        
    except Exception as e:
        print(f"❌ Error processing prompt '{prompt}': {str(e)}")
        continue

print("All prompts processed!")
