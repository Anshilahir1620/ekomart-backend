import re
import time
import os

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a filename by removing special characters, converting to lowercase,
    replacing spaces with hyphens, and appending a timestamp for uniqueness.
    Format: original-name-timestamp.ext
    """
    # Get name and extension
    name, ext = os.path.splitext(filename)
    
    # Remove special characters from name, keep only alphanumeric and hyphens/underscores
    # Convert to lowercase
    name = name.lower()
    # Replace spaces and non-alphanumeric characters with hyphens
    name = re.sub(r'[^a-z0-9]', '-', name)
    # Remove multiple hyphens
    name = re.sub(r'-+', '-', name)
    # Strip leading/trailing hyphens
    name = name.strip('-')
    
    # If name is empty after sanitization, use 'upload'
    if not name:
        name = 'upload'
        
    # Append timestamp for uniqueness
    timestamp = int(time.time())
    return f"{name}-{timestamp}{ext.lower()}"
