# Zettelkasten Link Checker Scripts

This directory contains scripts for checking and maintaining the integrity of wiki links in your Zettelkasten system.

## Available Scripts

### `check_broken_links.py`

A comprehensive link checker that scans all markdown files in the notes and mocs directories for wiki links (`[[like-this]]`) and verifies that they point to existing notes.

**Features:**
- Colorized output for easy reading
- Detailed reports of broken links with line numbers
- Suggests potential matches for broken links
- Option to generate a full report file

**Usage:**
```bash
# Run the basic check
python scripts/check_broken_links.py

# Generate a detailed report file
python scripts/check_broken_links.py --report
```

### `quick_link_check.py`

A faster, optimized version of the link checker with minimal output. Useful for quick scans of large Zettelkasten systems.

**Features:**
- Multi-threaded for faster processing
- Concise summary output
- Optional verbose mode for more details
- Significantly faster than the full checker

**Usage:**
```bash
# Run a quick check
python scripts/quick_link_check.py

# Run with verbose output
python scripts/quick_link_check.py --verbose
```

## How Wiki Links Work

In this Zettelkasten system:

1. Wiki links use the format `[[link-name]]` or `[[link-name|display text]]`
2. Links are normalized to lowercase with spaces converted to hyphens
3. Special characters are removed
4. A link like `[[My-Note]]` should point to a file named `my-note.md`

## Fixing Broken Links

When broken links are found, you have two options:

1. **Create the missing note** - Create a new markdown file with the normalized name
2. **Update the link** - Change the link to point to an existing note

## Integration with Zettelkasten Workflow

Consider running these scripts:
- After adding multiple new notes
- Before committing changes to version control
- Periodically as maintenance
- When experiencing issues with navigation

The scripts can be integrated into automated workflows to maintain Zettelkasten integrity.