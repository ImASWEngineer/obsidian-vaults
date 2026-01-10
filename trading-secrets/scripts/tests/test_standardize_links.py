import pytest
from pathlib import Path

# Import from the 'scripts' package directly
# This relies on the project root being in PYTHONPATH (e.g., via pytest.ini's pythonpath = .)
from scripts.standardize_links import normalize_wikilink_text, process_markdown_file


@pytest.fixture
def temp_zettelkasten_root(tmp_path):
    """
    Creates a temporary Zettelkasten root directory with a notes subdirectory
    and returns its path.
    """
    notes_dir = tmp_path / "notes"
    notes_dir.mkdir()
    return tmp_path


def test_normalize_wikilink_text_basic():
    """Test basic normalization: spaces to hyphens, lowercase."""
    assert normalize_wikilink_text("Hello World") == "hello-world"
    assert normalize_wikilink_text("Risk Management") == "risk-management"
    assert normalize_wikilink_text("Trading Strategy MOC") == "trading-strategy-moc"


def test_normalize_wikilink_text_special_characters():
    """Test normalization with various special characters."""
    assert normalize_wikilink_text("Note with 'single quotes'") == "note-with-single-quotes"
    assert normalize_wikilink_text('Note with "double quotes"') == "note-with-double-quotes"
    assert normalize_wikilink_text("Note with: a colon") == "note-with-a-colon"
    assert normalize_wikilink_text("Note with / a slash") == "note-with-a-slash"
    assert normalize_wikilink_text("Note with? a question mark") == "note-with-a-question-mark"
    assert normalize_wikilink_text("Note with! an exclamation") == "note-with-an-exclamation"
    assert normalize_wikilink_text("Note (with) parentheses") == "note-with-parentheses"
    assert normalize_wikilink_text("Note [with] brackets") == "note-with-brackets"


def test_normalize_wikilink_text_hyphens_and_underscores():
    """Test normalization with existing hyphens and underscores."""
    assert normalize_wikilink_text("hello-world") == "hello-world"
    assert normalize_wikilink_text("hello_world") == "hello-world"
    assert normalize_wikilink_text("hello--world") == "hello-world"  # Multiple hyphens
    assert normalize_wikilink_text("hello__world") == "hello-world"  # Multiple underscores
    assert normalize_wikilink_text("hello-_world") == "hello-world"  # Mixed


def test_normalize_wikilink_text_leading_trailing_spaces_hyphens():
    """Test normalization with leading/trailing spaces and hyphens."""
    assert normalize_wikilink_text("  hello world  ") == "hello-world"
    assert normalize_wikilink_text("-hello-world-") == "hello-world"
    assert normalize_wikilink_text("  -  hello world  -  ") == "hello-world"


def test_normalize_wikilink_text_empty_or_only_special_chars():
    """Test normalization of empty or only special character strings."""
    assert normalize_wikilink_text("") == ""
    assert normalize_wikilink_text("!@#$%^&*()") == ""
    assert normalize_wikilink_text("---") == ""


def test_process_markdown_file_with_links(temp_zettelkasten_root):
    """Test processing a file with links that need normalization."""
    filepath = temp_zettelkasten_root / "notes" / "test-note.md"
    original_content = """
# Test Note
This note links to [[Another Note]] and [[A Third Note]].
It also has a [[Note with Spaces]] and [[Note-with--Hyphens]].
"""
    filepath.write_text(original_content)

    process_markdown_file(filepath)

    expected_content = """
# Test Note
This note links to [[another-note]] and [[a-third-note]].
It also has a [[note-with-spaces]] and [[note-with-hyphens]].
"""
    assert filepath.read_text() == expected_content


def test_process_markdown_file_no_changes_needed(temp_zettelkasten_root):
    """Test processing a file where no links need normalization."""
    filepath = temp_zettelkasten_root / "notes" / "no-change-note.md"
    original_content = """
# No Change Note
This note links to [[already-normalized]] and [[another-one]].
"""
    filepath.write_text(original_content)

    process_markdown_file(filepath)

    # Content should remain exactly the same
    assert filepath.read_text() == original_content


def test_process_markdown_file_no_links(temp_zettelkasten_root):
    """Test processing a file with no links."""
    filepath = temp_zettelkasten_root / "notes" / "no-links.md"
    original_content = "# Just a plain note."
    filepath.write_text(original_content)

    process_markdown_file(filepath)

    assert filepath.read_text() == original_content