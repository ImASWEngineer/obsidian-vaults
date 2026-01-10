# Trading Secrets Zettelkasten

A comprehensive knowledge management system for day trading concepts, strategies, and insights, built using Zettelkasten principles.

## 📂 Directory Structure

```
trading-secrets/
├── notes/          # Individual atomic notes
├── mocs/           # Maps of Content (MOCs)
├── references/     # Reference materials and sources
└── templates/      # Note templates
```

## 🔗 Linking System

### 1. Note Naming Convention
- Use lowercase with hyphens: `trading-psychology.md`
- Keep filenames concise but descriptive
- Use present tense for concepts: `using-stop-losses.md` not `how-to-use-stop-losses.md`

### 2. Internal Links
- Use double brackets for internal links: `[[trading-psychology]]`
- The system automatically converts spaces to hyphens
- Links are case-insensitive: `[[trading-psychology]]` works the same

### 3. Tags
- Use `#tag` for broad categorization
- Keep tags consistent: `#trading-psychology` not `#psychology-of-trading`
- Use snake_case for multi-word tags

## 🗺️ Maps of Content (MOCs)

MOCs are special notes that help organize and navigate related notes:

1. **Core MOCs** (in `/mocs/`):
   - `trading-psychology-moc.md`
   - `risk-management-moc.md`
   - `technical-analysis-moc.md`
   - `trading-strategies-moc.md`

2. **Using MOCs**:
   - Start with the main `index.md`
   - Navigate to relevant MOCs
   - Follow links to atomic notes

## 🔄 Workflow

1. **Creating New Notes**:
   - Use the template in `templates/zettel-template.md`
   - Add relevant links to existing notes
   - Update relevant MOCs with links to the new note

2. **Updating Notes**:
   - Keep notes atomic (one concept per note)
   Add links to related concepts
   - Update the "Last Updated" timestamp

3. **Maintaining MOCs**:
   - Regularly review and update MOCs
   - Ensure all notes are linked to at least one MOC
   - Remove or update broken links

## 📚 Resources

- [Zettelkasten Method](https://zettelkasten.de/posts/overview/)
- [Linking Your Thinking](https://linkingyourthinking.com/)
- [Obsidian Help](https://help.obsidian.md/Home)
- [Mermaid.js Documentation](https://mermaid.js.org/)
- [Python Scripting](https://docs.python.org/3/)

## 🚀 Getting Started

1. Clone this repository
2. Open in a Zettelkasten-compatible app (Obsidian, Zettlr, etc.)
3. Start with `index.md`
4. Use search and MOCs to navigate

## 🤖 For LLM Users

This Zettelkasten is designed to be LLM-friendly. When processing or generating content:

1. **Context Awareness**: Always check linked notes for full context
2. **Link Formatting**: Maintain the `[[note-title]]` format in content
3. **Atomicity**: Keep notes focused on single concepts
4. **MOC Navigation**: Use MOCs to understand relationships between concepts
5. **Metadata**: Pay attention to YAML frontmatter for note relationships

Example LLM prompt:
```
You are a helpful assistant navigating a Zettelkasten knowledge base about day trading. 
When referencing other notes, use the [[note-title]] format. 
Always check for existing notes before creating new ones.
```

## 🛠️ Zettelkasten Management Tool

We provide a command-line tool built with Python and Poetry to help manage your Zettelkasten.

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/docs/#installation)

### Installation

1. Clone this repository
2. Navigate to the project root
3. Install dependencies with Poetry:

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Usage

#### Check for broken links
```bash
poetry run zettle check
```

#### Generate a Mermaid graph of note relationships
```bash
# Print to console
poetry run zettle graph

# Save to file
poetry run zettle graph --output notes/note-graph.md
```

#### Create a new note
```bash
# Create a new note in the default notes/ directory
poetry run zettle new "Your Note Title"

# Create a note with a specific template
poetry run zettle new "Your Note Title" --template your-template

# Create and edit the note immediately
poetry run zettle new "Your Note Title" --edit
```

### Development

To set up the development environment:

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run linters
poetry run black .
poetry run isort .
poetry run flake8
poetry run mypy trading_zettelkasten
```

### For LLM Navigation

1. When you see `[[trading-psychology]]` in a note:
   - The script automatically converts it to `trading-psychology.md`
   - It first looks in the `notes/` directory, then in `mocs/`

2. When creating new links:
   - Use natural language with spaces: `[[risk-management]]`
   - The system will handle the filename conversion

### Navigation Commands
```bash
# Find a note by title (case insensitive)
find . -name "*.md" -exec grep -l -i "search term" {} \;

# Find all links in a file
grep -o '\[\[.*\]\]' path/to/note.md | sort | uniq

# Find broken links
find . -name "*.md" -type f -exec grep -l '\[\[.*\]\]' {} \; | while read file; do
    grep -o '\[\[[]]*\]\]' "$file" | while read link; do
        target=$(echo "$link" | sed 's/\[\[\([^]]*\)\]\]/\1/' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
        if ! find . -name "${target}.md" | grep -q .; then
            echo "Broken link in $file: $link"
        fi
    done
done
```

## 🔄 Workflow

1. **Creating New Notes**:
   - Use the template in `templates/zettel-template.md`
   - Add relevant links to existing notes
   - Update relevant MOCs with links to the new note

2. **Updating Notes**:
   - Keep notes atomic (one concept per note)
   Add links to related concepts
   - Update the "Last Updated" timestamp

3. **Maintaining MOCs**:
   - Regularly review and update MOCs
   - Ensure all notes are linked to at least one MOC
   - Remove or update broken links

## 📚 Resources

- [Zettelkasten Method](https://zettelkasten.de/posts/overview/)
- [Linking Your Thinking](https://linkingyourthinking.com/)
- [Obsidian Help](https://help.obsidian.md/Home)
- [Mermaid.js Documentation](https://mermaid.js.org/)
- [Python Scripting](https://docs.python.org/3/)

## 🚀 Getting Started

1. Clone this repository
2. Open in a Zettelkasten-compatible app (Obsidian, Zettlr, etc.)
3. Start with `index.md`
4. Use search and MOCs to navigate

## 🤖 For LLM Users

This Zettelkasten is designed to be LLM-friendly. When processing or generating content:

1. **Context Awareness**: Always check linked notes for full context
2. **Link Formatting**: Maintain the `[[note-title]]` format in content
3. **Atomicity**: Keep notes focused on single concepts
4. **MOC Navigation**: Use MOCs to understand relationships between concepts
5. **Metadata**: Pay attention to YAML frontmatter for note relationships

Example LLM prompt:
```
You are a helpful assistant navigating a Zettelkasten knowledge base about day trading. 
When referencing other notes, use the [[note-title]] format. 
Always check for existing notes before creating new ones.
```
