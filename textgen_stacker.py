#!/usr/bin/env python3

from google import genai
import os

# Define input and output file names
infile = "file.txt"
outfile_base = "output"
outfile_ext = ".txt"
separator = "*****"

# Get API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Initialize the client
client = genai.Client(api_key=api_key)

# Read the entire input file
try:
    with open(infile, "r") as file:
        content = file.read()
except FileNotFoundError:
    print(f"Error: Input file '{infile}' not found.")
    exit(1)

# Start with count at 1
count = 1

# Split content by separators and remove the last part (assumed empty)
parts = content.split(separator)[:-1]

# Process each part (text before each separator)
for part in parts:
    part = part.strip()
    
    # Skip empty parts
    if not part:
        continue
    
    # Generate content from Gemini API
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=part
    )
    
    # Save response to output_{count}.txt
    with open(f"{outfile_base}_{count}{outfile_ext}", "w") as file:
        file.write(response.text)
    
    print(f"Processed part {count}")
    print(f"Response has been saved to '{outfile_base}_{count}{outfile_ext}'")
    
    # Increment count
    count += 1

print("All parts processed successfully.")
