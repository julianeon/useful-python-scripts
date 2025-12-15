#!/usr/bin/env python3
from google import genai
import os
import sys
import re
from datetime import datetime

def format_diary_entry():
    """
    Format current datetime into filename format.
    
    Returns:
        str: Formatted filename (example: "post_diary_010525_0600.md")
    """
    dt = datetime.now()
    date_part = dt.strftime("%m%d%y")
    time_part = dt.strftime("%H%M")
    return f"post_diary_{date_part}_{time_part}.md"


def prompt_cleaner(prompt):
    """
    Clean up the prompt by removing metadata lines.
    
    Removes lines that:
    - Start with ### (headers)
    - Contain https:// (URLs)
    - Contain 6-digit numbers (like log_120125.md)
    
    Args:
        prompt (str): The raw prompt text
    
    Returns:
        str: Cleaned prompt with irrelevant lines removed
    """
    lines = prompt.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip lines starting with #
        if line.strip().startswith('#'):
            continue
        # Skip lines containing https
        if 'https' in line:
            continue
        # Skip lines containing 6-digit numbers (like dates in filenames)
        if re.search(r'\d{6}', line):
            continue
        if '.md' in line:
            continue
        cleaned_lines.append(line)
        
    result = '\n'.join(cleaned_lines).strip()
    result = re.sub(r'\n\n+', '\n\n', result)
    
    return '\n'.join(cleaned_lines).strip()


def generate_ai_response(prompt, api_key, model="gemini-2.5-flash"):
    """
    Call the Gemini API to generate a response to the given prompt.
    
    Args:
        prompt (str): The prompt to send to the model
        api_key (str): The API key for authentication
        model (str): The model to use (default: gemini-2.5-flash)
    
    Returns:
        str: The generated response text
    """
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text


def save_response_to_file(content, filename):
    """
    Write content to a file.
    
    Args:
        content (str): The content to write
        filename (str): The output filename
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, "w") as file:
            file.write(content)
        return True
    except IOError as e:
        print(f"Error: Failed to write to '{filename}': {e}")
        return False


# Get input filename
infile = "diary.md"
outfile = format_diary_entry()

# Get API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Read the diary entry from the input file
try:
    with open(infile, "r") as file:
        finput = file.read().strip()
except FileNotFoundError:
    print(f"Error: Input file '{infile}' not found.")
    exit(1)

# Build the prompt with instructions
instructions = "Please comment, in the manner of a combined psychologist and friend, on the diary entry below, w/a special emphasis on getting things done. Include any actionable insights.\n\n"
cleaned_input = prompt_cleaner(finput)
prompt = instructions + cleaned_input

# Generate AI response and save to file
#print(prompt)
response_text = generate_ai_response(prompt, api_key)
save_response_to_file(response_text, outfile)
