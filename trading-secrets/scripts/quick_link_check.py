#!/usr/bin/env python3
"""
Quick Link Check - A faster version of check_broken_links.py
This script checks for broken wiki links in markdown files with minimal output
and optimized performance.
"""

import re
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Set, Tuple, Optional

# Import the normalize_wikilink_text function from standardize_links.py
from standardize_links import normalize_wikilink_text

def build_markdown_index(root_dir: Path) -> Set[str]:
    """Build an index of all markdown files in the directory."""
    markdown_files = set()
    
    for file_path in root_dir.rglob('*.md'):
        # Skip certain directories
        if any(part in file_path.parts for part in ['templates', 'references', 'scripts']):
            continue
        
        # Store the normalized filename without extension
        normalized_name = normalize_wikilink_text(file_path.stem)
        markdown_files.add(normalized_name)
    
    return markdown_files

def extract_wiki_links(content: str) -> List[str]:
    """Extract all wiki links from content efficiently."""
    # Regex to find [[...]] links, capturing the link target separately
    link_pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
    return [match.group(1).strip() for match in link_pattern.finditer(content)]

def check_file_links(file_path: Path, valid_files: Set[str]) -> Tuple[int, List[str]]:
    """Check all wiki links in a file and return broken links."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return 0, []
    
    links = extract_wiki_links(content)
    total_links = len(links)
    
    broken_links = []
    for link_target in links:
        normalized_target = normalize_wikilink_text(link_target)
        if normalized_target not in valid_files:
            broken_links.append(link_target)
    
    return total_links, broken_links

def process_file(args) -> Tuple[Path, int, List[str]]:
    """Process a single file for multi-threading."""
    file_path, valid_files = args
    total_links, broken_links = check_file_links(file_path, valid_files)
    return file_path, total_links, broken_links

def main(verbose: bool = False):
    """Main function to check for broken links."""
    # Assuming the script is run from the 'trading-secrets' root directory
    zettelkasten_root = Path(__file__).parent.parent
    
    print(f"Scanning Zettelkasten at: {zettelkasten_root}")
    
    # Build index of valid markdown files
    valid_files = build_markdown_index(zettelkasten_root)
    print(f"Found {len(valid_files)} valid markdown files.")
    
    # Find all markdown files to check (focusing on notes and mocs)
    dirs_to_check = ['notes', 'mocs']
    files_to_check = []
    
    for dir_name in dirs_to_check:
        dir_path = zettelkasten_root / dir_name
        if dir_path.exists():
            files_to_check.extend(dir_path.glob('*.md'))
    
    files_to_check.sort()  # For consistent processing order
    
    print(f"Checking {len(files_to_check)} markdown files for broken links...")
    
    # Track statistics
    total_links_checked = 0
    total_broken_links = 0
    files_with_broken_links = 0
    broken_link_details = {}
    
    # Process files in parallel
    with ThreadPoolExecutor(max_workers=min(10, len(files_to_check))) as executor:
        tasks = [(file_path, valid_files) for file_path in files_to_check]
        
        for file_path, total_links, broken_links in executor.map(process_file, tasks):
            total_links_checked += total_links
            
            if broken_links:
                files_with_broken_links += 1
                total_broken_links += len(broken_links)
                broken_link_details[file_path] = broken_links
                
                if verbose:
                    rel_path = file_path.relative_to(zettelkasten_root)
                    print(f"\n{rel_path}: {len(broken_links)} broken links")
                    for link in broken_links[:5]:  # Show only the first 5 broken links
                        print(f"  - [[{link}]]")
                    if len(broken_links) > 5:
                        print(f"  ... and {len(broken_links) - 5} more")
    
    # Print summary
    print("\n" + "="*50)
    print("SUMMARY:")
    print(f"Total files checked: {len(files_to_check)}")
    print(f"Total links checked: {total_links_checked}")
    print(f"Total broken links: {total_broken_links}")
    print(f"Files with broken links: {files_with_broken_links}")
    
    # List top files with broken links
    if broken_link_details and verbose:
        print("\nTop files with broken links:")
        sorted_files = sorted(broken_link_details.items(), 
                            key=lambda x: len(x[1]), reverse=True)
        for file_path, links in sorted_files[:5]:  # Show only top 5 files
            rel_path = file_path.relative_to(zettelkasten_root)
            print(f"  {rel_path}: {len(links)} broken links")
    
    if total_broken_links > 0:
        print("\nRecommendation: Use the full checker for detailed report:")
        print("  python scripts/check_broken_links.py --report")
        return 1
    else:
        print("\nAll wiki links are valid!")
        return 0

if __name__ == "__main__":
    verbose_mode = "--verbose" in sys.argv
    sys.exit(main(verbose=verbose_mode))