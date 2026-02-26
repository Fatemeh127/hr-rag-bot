# def chunk_text(text: str, chunk_size: int=500, overlap: int=20):
#     chunks = []
#     for i in range(0, len(text), chunk_size - overlap):
#         chunk = text[i: i + chunk_size].strip()

#         if chunk:
#             chunks.append(chunk)
#     return chunks

## chunk with heading
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_by_heading(text: str):
    pattern = r"\n([A-Z][A-Za-z\s]+:)\n"
    sections = re.split(pattern, text)

    combined = []
    for i in range(1, len(sections), 2):
        heading = sections[i]
        content = sections[i + 1]
        combined.append((heading + "\n" + content).strip())

    return combined


splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=500,
    chunk_overlap=100
)


def chunk_text(text: str):
    final_chunks = []
    sections = split_by_heading(text)

    if not sections:
        return splitter.split_text(text)

    for sec in sections:
        if len(sec) <= 500:
            final_chunks.append(sec)
        else:
            chunks = splitter.split_text(sec)
            final_chunks.extend(chunks)

    return final_chunks