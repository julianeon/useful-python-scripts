from datetime import datetime

def format_diary_entry():
    """
    Format current datetime into readable string and filename format.
    
    Returns:
        str: Formatted string with readable time and filename
        Example: "6am on 1/5/25\npost_diary_010525_0600.md"
    """
    dt = datetime.now()
    
    # Format human-readable string
    am_pm = dt.strftime("%I%p").lstrip('0').lower()
    readable = dt.strftime("%-m/%-d/%y")
    readable_str = f"{am_pm} on {readable}"
    
    # Format filename
    date_part = dt.strftime("%m%d%y")
    time_part = dt.strftime("%H%M")
    filename = f"post_diary_{date_part}_{time_part}.md"
    

    #return f"{readable_str}\n{filename}"
    return filename

if __name__ == "__main__":
    str = format_diary_entry()
    print(str)
