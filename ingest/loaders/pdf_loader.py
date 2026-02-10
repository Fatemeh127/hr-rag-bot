from PyPDF2 import PdfReader

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    
    text_pages = []
    for page in reader.pages:
        text_pages.append(page.extract_text() or "")

    return "\n".join(text_pages)