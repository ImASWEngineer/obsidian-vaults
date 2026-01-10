import re
from pathlib import Path

def normalize_wikilink_text(link_text: str) -> str:
    """
    Converts a wikilink's display text to its normalized filename-like format
    (lowercase, spaces to hyphens, special chars removed).
    This aligns with the Zettelkasten's filename convention.
    """
    # Remove invalid characters (anything not alphanumeric, space, or hyphen)
    # This step ensures that characters like quotes, colons, slashes, etc.,
    # which might be in the display text but not in the filename, are removed.
    cleaned_text = re.sub(r'[^\w\s-]', '', link_text)
    # Replace spaces and underscores with hyphens, then convert to lowercase
    normalized = re.sub(r'[\s_]+', '-', cleaned_text).lower()
    # Collapse multiple hyphens into a single hyphen
    normalized = re.sub(r'-+', '-', normalized)
    # Remove any leading or trailing hyphens that might result from cleaning or collapsing
    return normalized.strip('-')

def process_markdown_file(filepath: Path):
    """
    Reads a markdown file, normalizes all internal wikilinks [[...]],
    and writes back the changes if any were made.
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    # Regex to find [[...]] links, capturing the link target and optional display text separately.
    # Group 1: Link Target (e.g., "My Note" in "[[My Note|some text]]")
    # Group 2: Optional Display Text (e.g., "|some text" in "[[My Note|some text]]")
    link_pattern = re.compile(r'\[\[([^\]|]+)(\|[^\]]+)?\]\]')

    def replacer(match):
        link_target = match.group(1)
        display_part = match.group(2) or ''  # This will be like "|some text" or empty

        normalized_target = normalize_wikilink_text(link_target)

        # Reconstruct the link with the normalized target and original display text
        return f"[[{normalized_target}{display_part}]]"

    new_content = link_pattern.sub(replacer, content)

    if new_content != content:
        try:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"Updated links in: {filepath}")
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")
    else:
        # print(f"No changes needed for: {filepath}") # Uncomment for verbose output
        pass

def main():
    # Assuming the script is run from the 'trading-secrets' root directory
    # The Zettelkasten root is one level up from the 'scripts' directory
    zettelkasten_root = Path(__file__).parent.parent

    print(f"Scanning Zettelkasten at: {zettelkasten_root}")

    # Find all markdown files recursively, excluding 'templates' and 'references' directories
    files_to_process = [
        f for f in zettelkasten_root.rglob('*.md')
        if "templates" not in f.parts and "references" not in f.parts and "scripts" not in f.parts
    ]
    files_to_process.sort() # For consistent processing order, useful for testing

    print(f"Found {len(files_to_process)} markdown files to process.")

    for filepath in files_to_process:
        process_markdown_file(filepath)

    print("\nLink standardization complete.")

if __name__ == "__main__":
    main()