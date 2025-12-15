#!/usr/bin/env python3

from google import genai
import os
import re

# Define input and output file names
title_file = "title.txt"
hook_file = "hook.txt"
outfile = "output_quote.txt"

api_key = os.environ.get("GEMINI_API_KEY")

try:
    with open(title_file, "r") as file:
        title_content = file.read().strip()
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
    print(f"Error: Outline section file '{outline_section_file}' not found.")
    exit(1)


prompt = f"""I would like 20 Stoicism quotes for a YouTube video for The Stoic Community with this title: {title}

Please list the quotes below. Suggested authors: Marcus Aurelius, Seneca, Epictetus. Feel free to use others also.

Include each quote in this format, for example for example quote "Live well" by Seneca.

1. Live well. - Seneca.

Do NOT include any asterisks or quotation marks in your response. There should be 1 quote per line.

Below is my hook for context.

****

{hook}"""

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=prompt
)

with open(outfile, "w") as file:
    file.write(response.text)

print(f"Response has been saved to '{outfile}'")
