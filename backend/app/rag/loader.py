from pathlib import Path

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader


def load_file(file_path: str):
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return TextLoader(str(path), encoding="utf-8").load()
    if suffix == ".pdf":
        return PyPDFLoader(str(path)).load()
    if suffix == ".docx":
        return Docx2txtLoader(str(path)).load()
    raise ValueError(f"Unsupported file type: {suffix}")
