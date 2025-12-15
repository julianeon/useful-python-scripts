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


cleaned_input = prompt_cleaner(finput)
prompt = instructions + cleaned_input
