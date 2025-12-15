#!/usr/bin/env python3

from google import genai
import os
import re

# Define input and output file names
title_file = "title.txt"
hook_file = "hook.txt"
desc_file = "shortdesc.txt"
outfile = "output_outline.txt"

# Get API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Read the title from the title file
try:
    with open(title_file, "r") as file:
        title_content = file.read().strip()
        # Extract the title part after "(title)"
        title_match = re.search(r'\(title\)(.*?)($|\()', title_content)
        if title_match:
            title = title_match.group(1).strip()
        else:
            # If no "(title)" format is found, use the whole content
            title = title_content
except FileNotFoundError:
    print(f"Error: Title file '{title_file}' not found.")
    exit(1)

try:
    with open(hook_file, "r") as file:
        hook = file.read().strip()
except FileNotFoundError:
    print(f"Error: not found.")
    exit(1)

try:
    with open(desc_file, "r") as file:
        desc = file.read().strip()
except FileNotFoundError:
    print(f"Error: not found.")
    exit(1)

# Construct the prompt
prompt = f"""I'm writing a script for a YouTube channel called The Stoic Community with this title: {title}

Please write an 20-section outline for the script that is to be written. Assume the outline is completely self-contained and includes all quotations etc. necessary for the script within its text.

For reference see the template shown below (from a different unrelated video).

## 0. The Ruling Mindset: Foundation of Personal Sovereignty

- The psychology behind seeing yourself as the ruler of your own life
- Why most people surrender their sovereignty to external forces
- The Stoic concept of "ruling faculty" (hegemonikon) and its modern application
- Simple daily affirmations to rewire your thinking toward self-leadership

Some of the areas I'd like to cover are listed below.

{desc}

Do NOT include any visual direction or asterisks. Just the text of the outline.

Hook of the script is shown below.

*****
{hook}"""

# Initialize the client
client = genai.Client(api_key=api_key)

# Generate content
response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=prompt
)

# Write response to the output file
with open(outfile, "w") as file:
    file.write(response.text)

print(f"Title read from '{title_file}'")
print(f"Response has been saved to '{outfile}'")
