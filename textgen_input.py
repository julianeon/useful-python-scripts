#!/usr/bin/env python3

from google import genai
import os
import sys

# Define input and output file names
infile = sys.argv[1]
base = infile.split('.')[0]
outfile = f"post_{base}.txt"

# Get API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Read the prompt from the input file
try:
    with open(infile, "r") as file:
        prompt = file.read().strip()
except FileNotFoundError:
    print(f"Error: Input file '{infile}' not found.")
    exit(1)

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

print(f"Prompt read from '{infile}'")
print(f"Response has been saved to '{outfile}'")
