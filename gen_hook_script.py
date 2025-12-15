#!/usr/bin/env python3

from google import genai
import os
import re

# Define input and output file names
title_file = "title.txt"
outfile = "output_hook.txt"

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

# Construct the prompt
prompt = f"""I would like a hook for a YouTube video for The Stoic Community with this title: {title}

Please show me 3 versions of a 200 word hook, in an engaging YT video style.

Do NOT include any asterisks or set direction in the text of the hooks. Include only words which will be spoken by the narrator.

Below is a template example of a good hook, between the asterisks.

****

Most people focus on what they need to be doing right.

But what if you should be thinking about what you're doing wrong?

It might be that those are the choices that are really hindering us and keeping us from reaching our potential.

If that's true, then the best thing we can do is not to make the right choices. It's to avoid the wrong choices.

****

Here is another example.

****

Have you ever felt that sinking feeling when dealing with someone who drains your energy?

Some people are just difficult. They're negative, critical, demanding. Or they thrive on chaos.

It could be a work colleague. It could be a family member. It's anyone you don't want to be around.

The question is, how do you deal with these people without losing your mind? How do you protect your peace of mind and stay true to your values at the same time?

Stoicism offers us a framework for navigating these tricky relationships. It starts with understanding what's within your control and what isn't.

"""

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
