#!/usr/bin/env python3
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import sys
import re
import json
from datetime import datetime


class DiaryAnalysis(BaseModel):
    """Structured output for diary analysis"""
    takeaway: str = Field(description="One line big picture takeaway from the diary entry.")
    action_items: List[str] = Field(description="List of actionable items the user should consider.")
    assessment: str = Field(description="Psychological evaluation and observations based on the diary entry.")
    areas_of_improvement: str = Field(description="Text description of areas where the user could improve based on the diary.")
    standouts: List[str] = Field(description="Interesting or notable items from the diary worth highlighting.")


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
    
    return result


def generate_structured_analysis(prompt, api_key, model="gemini-2.5-flash"):
    """
    Call the Gemini API to generate a structured diary analysis.
    
    Args:
        prompt (str): The diary entry text to analyze
        api_key (str): The API key for authentication
        model (str): The model to use (default: gemini-2.5-flash)
    
    Returns:
        DiaryAnalysis: Structured analysis object
    """
    client = genai.Client(api_key=api_key)
    
    instructions = """Please analyze the following diary entry and provide structured feedback in the manner of a friendly psychologist. 
Be insightful, supportive, and provide actionable guidance."""
    
    full_prompt = instructions + "\n\n" + prompt
    
    response = client.models.generate_content(
        model=model,
        contents=full_prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": DiaryAnalysis.model_json_schema(),
        },
    )
    
    analysis = DiaryAnalysis.model_validate_json(response.text)
    return analysis


def save_analysis_to_file(analysis, filename):
    """
    Write analysis to a markdown file in a readable format.
    
    Args:
        analysis (DiaryAnalysis): The structured analysis object
        filename (str): The output filename
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, "w") as file:
            file.write(f"# Diary Analysis\n\n")
            file.write(f"## Takeaway\n{analysis.takeaway}\n\n")
            file.write(f"## Action Items\n")
            for item in analysis.action_items:
                file.write(f"- {item}\n")
            file.write(f"\n## Assessment\n{analysis.assessment}\n\n")
            file.write(f"## Areas of Improvement\n{analysis.areas_of_improvement}\n\n")
            file.write(f"## Standouts\n")
            for item in analysis.standouts:
                file.write(f"- {item}\n")
        return True
    except IOError as e:
        print(f"Error: Failed to write to '{filename}': {e}")
        return False


def save_json_analysis(analysis, filename):
    """
    Save the structured analysis as JSON.
    
    Args:
        analysis (DiaryAnalysis): The structured analysis object
        filename (str): The output JSON filename
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, "w") as file:
            file.write(analysis.model_dump_json(indent=2))
        return True
    except IOError as e:
        print(f"Error: Failed to write JSON to '{filename}': {e}")
        return False


# Get input filename
infile = "diary.md"
outfile_md = format_diary_entry()
outfile_json = outfile_md.replace(".md", ".json")

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

# Clean the input and generate analysis
cleaned_input = prompt_cleaner(finput)
analysis = generate_structured_analysis(cleaned_input, api_key)

# Save to both markdown and JSON formats
save_analysis_to_file(analysis, outfile_md)
save_json_analysis(analysis, outfile_json)

print(f"Analysis saved to {outfile_md} and {outfile_json}")