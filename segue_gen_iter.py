#!/usr/bin/env python3
from google import genai
import os
import sys

# Configuration variables
var_start = 0
var_stop = 8

# Get API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Initialize the client
client = genai.Client(api_key=api_key)

# Process stepwise from var_start to var_stop
for i in range(var_start, var_stop):
    file_a = f"output_{i}.txt"
    file_b = f"output_{i+1}.txt"
    outfile = f"inter_{i}.txt"
    
    # Read the content from both input files
    try:
        with open(file_a, "r") as file:
            content_a = file.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file '{file_a}' not found.")
        exit(1)

    try:
        with open(file_b, "r") as file:
            content_b = file.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file '{file_b}' not found.")
        exit(1)

    # Construct the prompt
    prompt = f"""These are two pieces of my writing, A and B. B follows A.

Answer in media res. Do not reply with any text which is not meant to be included exactly as writen in the segue. It can be as long as is needed to smoothly connect the pieces.

A:
{content_a}

B:
{content_b}"""

    # Generate content
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )

    # Write response to the output file
    with open(outfile, "w") as file:
        file.write(response.text)

    print(f"Step {i}: Content read from '{file_a}' and '{file_b}', response saved to '{outfile}'")

print("\nAll processing complete!")
