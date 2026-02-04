def chunk_text(text: str, chunk_size: int=500, overlap: int=20):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i: i + chunk_size].strip()

        if chunk:
            chunks.append(chunk)
    return chunks