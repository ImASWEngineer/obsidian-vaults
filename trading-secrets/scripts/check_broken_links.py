import re
import sys
import difflib
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Import the normalize_wikilink_text function from standardize_links.py
from standardize_links import normalize_wikilink_text

# ANSI color codes for colored output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def build_markdown_index(root_dir: Path) -> Set[str]:
    """
    Build an index of all markdown files in the directory.
    Returns a set of normalized filenames (without .md extension).
    """
    markdown_files = set()
    
    for file_path in root_dir.rglob('*.md'):
        # Skip certain directories
        if any(part in file_path.parts for part in ['templates', 'references', 'scripts']):
            continue
        
        # Store the normalized filename without extension
        normalized_name = normalize_wikilink_text(file_path.stem)
        markdown_files.add(normalized_name)
    
    return markdown_files

def extract_wiki_links(content: str) -> List[Tuple[str, int]]:
    """
    Extract all wiki links from content.
    Returns a list of tuples containing (link_target, line_number).
    """
    links = []
    # Regex to find [[...]] links, capturing the link target separately
    link_pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
    
    for line_num, line in enumerate(content.splitlines(), 1):
        for match in link_pattern.finditer(line):
            link_target = match.group(1).strip()
            links.append((link_target, line_num))
    
    return links

def check_file_links(file_path: Path, valid_files: Set[str]) -> List[Tuple[str, int, str]]:
    """
    Check all wiki links in a file against the valid files index.
    Returns a list of broken links with their line numbers.
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    broken_links = []
    links = extract_wiki_links(content)
    
    for link_target, line_num in links:
        normalized_target = normalize_wikilink_text(link_target)
        if normalized_target not in valid_files:
            broken_links.append((link_target, line_num, normalized_target))
    
    return broken_links

def main():
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
    
    # Check each file for broken links
    for file_path in files_to_check:
        broken_links = check_file_links(file_path, valid_files)
        
        # Count links in this file
        try:
            file_content = file_path.read_text(encoding='utf-8')
            file_links = extract_wiki_links(file_content)
            total_links_checked += len(file_links)
        except Exception:
            pass
        
        if broken_links:
            files_with_broken_links += 1
            total_broken_links += len(broken_links)
            
            print(f"\n{Colors.YELLOW}Broken links in {Colors.BOLD}{file_path.relative_to(zettelkasten_root)}{Colors.ENDC}{Colors.YELLOW}:{Colors.ENDC}")
            for link_target, line_num, normalized_target in broken_links:
                print(f"  Line {line_num}: {Colors.RED}[[{link_target}]]{Colors.ENDC} (normalized: {normalized_target})")
                
                # Find similar valid filenames as suggestions
                similar_names = difflib.get_close_matches(normalized_target, valid_files, n=3, cutoff=0.6)
                if similar_names:
                    suggestions = ", ".join([f"[[{name}]]" for name in similar_names])
                    print(f"    {Colors.GREEN}Suggested alternatives: {suggestions}{Colors.ENDC}")
    
    # Print summary
    print("\n" + "="*50)
    print(f"{Colors.HEADER}SUMMARY:{Colors.ENDC}")
    print(f"Total files checked: {len(files_to_check)}")
    print(f"Total links checked: {total_links_checked}")
    print(f"{Colors.BOLD}Total broken links: {Colors.RED if total_broken_links > 0 else Colors.GREEN}{total_broken_links}{Colors.ENDC}")
    print(f"{Colors.BOLD}Files with broken links: {Colors.RED if files_with_broken_links > 0 else Colors.GREEN}{files_with_broken_links}{Colors.ENDC}")
    
    if total_broken_links > 0:
        print(f"\n{Colors.YELLOW}Recommendation: Fix the broken links by either:{Colors.ENDC}")
        print(f"1. Creating the missing notes")
        print(f"2. Updating the links to point to existing notes")
        
        # Add option to save report to file
        print(f"\n{Colors.BLUE}To generate a detailed report file, run:{Colors.ENDC}")
        print(f"  python {Path(__file__).name} --report")
        
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}All wiki links are valid! 🎉{Colors.ENDC}")
        sys.exit(0)

if __name__ == "__main__":
    # Check for --report flag
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        # Redirect output to file
        report_path = Path(__file__).parent / "broken_links_report.txt"
        print(f"Generating report at: {report_path}")
        
        # Save current stdout
        original_stdout = sys.stdout
        
        # Redirect stdout to file
        with open(report_path, 'w', encoding='utf-8') as f:
            sys.stdout = f
            main()
            
        # Restore stdout
        sys.stdout = original_stdout
        
        print(f"{Colors.GREEN}Report generated at: {report_path}{Colors.ENDC}")
    else:
        main()