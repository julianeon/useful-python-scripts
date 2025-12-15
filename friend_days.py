#!/usr/bin/env python3
from google import genai
import os
import sys
import re
from datetime import datetime, timedelta

def format_diary_entry(days_back=0):
    """
    Format current datetime into filename with days_back argument appended.
    
    Args:
        days_back (int): Number of days back included (0-5)
    
    Returns:
        str: Filename like "post_diary_120125_0930_4.md" if days_back=4
    """
    dt = datetime.now()
    
    # Format filename
    date_part = dt.strftime("%m%d%y")
    time_part = dt.strftime("%H%M")
    filename = f"post_diary_{date_part}_{time_part}_{days_back}.md"
    
    return filename

def get_diary_files(days_back):
    """
    Get list of diary files to include, from oldest to newest.
    
    Args:
        days_back (int): Number of days back to include (0-5). 0 means only today.
    
    Returns:
        list: List of filenames in order from oldest to newest, with diary.md last
    """
    if days_back < 0 or days_back > 5:
        raise ValueError("days_back must be between 0 and 5")
    
    files = []
    
    # Start from days_back days ago and work forward to yesterday
    for i in range(days_back, 0, -1):
        date = datetime.now() - timedelta(days=i)
        date_part = date.strftime("%m%d%y")
        files.append(f"log_{date_part}.md")
    
    # Always append today's diary.md last
    files.append("diary.md")
    
    return files

def read_and_validate_files(filenames):
    """
    Read content from files, skipping missing ones.
    
    Args:
        filenames (list): List of filenames to read
    
    Returns:
        list: List of tuples (filename, content) for successfully read files
    """
    file_contents = []
    
    for filename in filenames:
        try:
            with open(filename, "r") as file:
                content = file.read().strip()
                file_contents.append((filename, content))
        except FileNotFoundError:
            print(f"Warning: File '{filename}' not found, skipping...")
            continue
    
    if not file_contents:
        raise FileNotFoundError("No diary files found to process")
    
    return file_contents

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

# Parse command line argument
days_back = 0
if len(sys.argv) > 1:
    try:
        days_back = int(sys.argv[1])
        if days_back < 0 or days_back > 5:
            print("Error: Argument must be between 0 and 5")
            sys.exit(1)
    except ValueError:
        print("Error: Argument must be a number between 0 and 5")
        sys.exit(1)

# Get list of diary files to process
diary_files = get_diary_files(days_back)
#print(f"Processing {len(diary_files)} file(s): {', '.join(diary_files)}")

# Create output filename
outfile = format_diary_entry(days_back)

# Get API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Read all diary files
file_contents = read_and_validate_files(diary_files)

# Build prompt with all diary entries
instructions = "Please comment, in the manner of a combined psychologist and friend, on the diary entries below, w/a special emphasis on getting things done. Include any actionable insights.\n\n"

prompt = instructions

for filename, content in file_contents:
    prompt += f"--- {filename} ---\n{content}\n\n"

cleaned_input = prompt_cleaner(prompt)
prompt = cleaned_input

# Initialize the client
client = genai.Client(api_key=api_key)

print(prompt)
# Generate content
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=prompt
)

# Write response to the output file
with open(outfile, "w") as file:
    file.write(response.text)

print(f"Response has been saved to '{outfile}'")
