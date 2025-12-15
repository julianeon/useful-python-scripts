#!/usr/bin/env python3
import requests
import json
import base64
import subprocess
import sys
import random
import re

PROJECT_ID = "gen-lang-client-0583662963"
LOCATION_ID = "us-central1"
API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
MODEL_ID = "imagen-4.0-generate-001"

def get_access_token():
    result = subprocess.run(['gcloud', 'auth', 'print-access-token'], 
                          capture_output=True, text=True)
    return result.stdout.strip()

def generate_filename(filetitle):
    """Generate filename from file title by stringing together words + .png"""
    # Split filetitle into words and clean them
    words = re.findall(r'\b\w+\b', filetitle.lower())

    # Join all words with underscores
    fbase = "_".join(words) 
    filename = fbase[:200] + ".png"
    return filename

def generate_image(prompt):
    """Generate image from prompt and return the image data"""
    try:
        request_data = {
            "endpoint": f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/publishers/google/models/{MODEL_ID}",
            "instances": [
                {
                    "prompt": prompt,
                }
            ],
            "parameters": {
                "aspectRatio": "16:9",
                "sampleCount": 1,
                "negativePrompt": "",
                "enhancePrompt": False,
                "personGeneration": "allow_all",
                "safetySetting": "block_few",
                "addWatermark": True,
                "includeRaiReason": True,
                "language": "auto"
            }
        }
        
        url = f"https://{API_ENDPOINT}/v1/projects/{PROJECT_ID}/locations/{LOCATION_ID}/publishers/google/models/{MODEL_ID}:predict"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_access_token()}"
        }
        
        response = requests.post(url, headers=headers, json=request_data)
        
        if response.status_code == 200:
            result = response.json()
            if "predictions" in result and result["predictions"]:
                return base64.b64decode(result["predictions"][0]["bytesBase64Encoded"])
            else:
                print(f"No predictions in response for prompt: {prompt[:50]}...")
                return None
        else:
            print(f"Error {response.status_code} for prompt: {prompt[:50]}...")
            return None
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <prompts_file>")
        sys.exit(1)
    
    prompts_file = sys.argv[1]
    
    try:
        with open(prompts_file, 'r', encoding='utf-8') as f:
            prompts = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{prompts_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    print(f"Processing {len(prompts)} prompts from {prompts_file}")
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\nProcessing prompt {i}/{len(prompts)}: {prompt[:50]}...")
        
        try:
            # Generate image
            image_data = generate_image(prompt)
            
            if image_data:
                # Generate filename
                filename = generate_filename(prompt)
                
                # Save image
                try:
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    print(f"✓ Saved: {filename}")
                except Exception as e:
                    print(f"✗ Failed to save {filename}: {e}")
            else:
                print(f"✗ Failed to generate image for prompt {i}")
                
        except Exception as e:
            print(f"✗ Error with prompt {i}: {e}")
            continue

if __name__ == "__main__":
    main()
