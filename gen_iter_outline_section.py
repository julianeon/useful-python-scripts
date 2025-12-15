#!/usr/bin/env python3

from google import genai
import os
import re

# Define input file names
title_file = "title.txt"
outline_file = "outline.txt"

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

# Read the outline file
try:
    with open(outline_file, "r") as file:
        outline_content = file.read()
except FileNotFoundError:
    print(f"Error: Outline file '{outline_file}' not found.")
    exit(1)

# Parse the outline into sections
# Looking for sections that start with "## " followed by a number
sections = re.findall(r'## \d+\.(.*?)(?=## \d+\.|$)', outline_content, re.DOTALL)

# Initialize the client
client = genai.Client(api_key=api_key)

# Process each section
for i, section in enumerate(sections):
    # Construct the prompt for this section
    prompt = f"""I'm writing a script for an explanatory and action-oriented talk with this title: {title}

Please write 500 words "in media res" for the section shown below. Do not include rhetorical questions.
Assume earlier section(s) have been written, ie no context setting for the beginning needed.
Do NOT include any visual direction or asterisks. Just the text of the video, with quotation marks where needed. Only include text which is literally meant to be spoken by the narrator.
Also, just end the section assuming more sections will follow (ie, no "comment below" type closers needed).

*****
{section.strip()}
****

As a template, here is an example of the type of style it should be written in.

If you’re struggling to find love, you’re not alone. But the truth is, a relationship isn't dumb luck. It takes effort, good choices, and the right mindset. 

We believe love is beautiful. You can have it, if you want it. You just need a method to bring that love to you. 

But first, a warning. I'm going to be blunt here. A lot of advice online, to be polite, is trash. I don't think the people saying it believe it. They just say anything to get engagement or attention. 

That's not what we're about here. As Stoics, we should always choose truth and integrity over lies. Everything that you're about to hear is real and based on success.

So let's get to it. What's the first thing you need to do to find love?

You need to be putting yourself out there. In one way or another, you need to be introducing yourself to the world. You need to be meeting potential partners and selling yourself to them. You need to be in the arena - fighting, struggling, and sweating - in order to win.

In a sentence: to find love, you must first get in front of the people who can give you love. 

"""


    # Generate content
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt
    )

    # Write response to the output file
    outfile = f"output_{i}.txt"
    with open(outfile, "w") as file:
        file.write(response.text)
    
    print(f"Generated content for section {i}, saved to '{outfile}'")

print(f"Title read from '{title_file}'")
print(f"All sections from '{outline_file}' have been processed and saved.")
