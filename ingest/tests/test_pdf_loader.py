import pytest
from ingest.loaders.pdf_loader import load_pdf
from pathlib import Path

TEST_DIR = Path(__file__).parent / "test_files"

# test with real files

# test for empty.pdf 
def test_empty_pdf():
    file = TEST_DIR / "empty.pdf"
    text = load_pdf(file)
    assert isinstance(text, str)
    assert text == ""

# test for multi_pages.pdf
def test_multy_pages_pdf():
    file = TEST_DIR / "multi_pages.pdf"
    text = load_pdf(file)
    assert isinstance(text, str)
    assert len(text) >= 0

# test for some_empty_pages.pdf
def test_some_empty_pages_pdf():
    file = TEST_DIR / "some_empty_pages.pdf"
    text = load_pdf(file)
    assert isinstance(text, str)
    assert text is not None

# test without real files

from unittest.mock import MagicMock, patch

def test_pdf_loader_with_mock():
    fake_page = MagicMock()
    fake_page.extract_text.return_value = None

    fake_reader = MagicMock()
    fake_reader.pages = [fake_page, fake_page]

    with patch("ingest.loaders.pdf_loader.PdfReader", return_value=fake_reader):
        text = load_pdf("any.pdf")
        assert isinstance(text, str)
        assert text == "\n"

    