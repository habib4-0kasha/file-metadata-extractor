import os
import hashlib
import exifread
import mutagen
from docx import Document
from PyPDF2 import PdfReader
from datetime import datetime


def get_file_info(filepath):
    """Basic file information available for any file type."""
    stat = os.stat(filepath)
    return {
        "filename": os.path.basename(filepath),
        "filepath": os.path.abspath(filepath),
        "size_bytes": stat.st_size,
        "size_kb": round(stat.st_size / 1024, 2),
        "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "accessed": datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
        "extension": os.path.splitext(filepath)[1].lower()
    }


def get_hashes(filepath):
    """Generate MD5, SHA1 and SHA256 hashes, used to verify file integrity."""
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)

    return {
        "md5": md5.hexdigest(),
        "sha1": sha1.hexdigest(),
        "sha256": sha256.hexdigest()
    }


def get_image_metadata(filepath):
    """Extract EXIF metadata from images, can reveal camera model, GPS location, timestamps."""
    metadata = {}
    try:
        with open(filepath, "rb") as f:
            tags = exifread.process_file(f, stop_tag="UNDEF", details=False)
            for tag, value in tags.items():
                metadata[tag] = str(value)
    except Exception as e:
        metadata["error"] = str(e)
    return metadata


def get_pdf_metadata(filepath):
    """Extract metadata from PDF files, author, creator tool, creation date."""
    metadata = {}
    try:
        reader = PdfReader(filepath)
        info = reader.metadata
        if info:
            for key, value in info.items():
                metadata[key.strip("/")] = str(value)
        metadata["pages"] = len(reader.pages)
    except Exception as e:
        metadata["error"] = str(e)
    return metadata


def get_docx_metadata(filepath):
    """Extract metadata from Word documents, author, last modified by, revision count."""
    metadata = {}
    try:
        doc = Document(filepath)
        props = doc.core_properties
        metadata["author"] = props.author
        metadata["last_modified_by"] = props.last_modified_by
        metadata["created"] = str(props.created)
        metadata["modified"] = str(props.modified)
        metadata["revision"] = props.revision
        metadata["title"] = props.title
        metadata["subject"] = props.subject
    except Exception as e:
        metadata["error"] = str(e)
    return metadata


def get_audio_metadata(filepath):
    """Extract metadata from audio files, artist, album, duration, encoder."""
    metadata = {}
    try:
        audio = mutagen.File(filepath)
        if audio:
            for key, value in audio.items():
                metadata[key] = str(value)
            if hasattr(audio.info, "length"):
                metadata["duration_seconds"] = round(audio.info.length, 2)
    except Exception as e:
        metadata["error"] = str(e)
    return metadata


def extract(filepath):
    """Main function, runs all relevant extractors based on file type."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    result = {}
    result["file_info"] = get_file_info(filepath)
    result["hashes"] = get_hashes(filepath)

    ext = result["file_info"]["extension"]

    if ext in [".jpg", ".jpeg", ".png", ".tiff", ".heic"]:
        result["image_metadata"] = get_image_metadata(filepath)

    elif ext == ".pdf":
        result["pdf_metadata"] = get_pdf_metadata(filepath)

    elif ext == ".docx":
        result["docx_metadata"] = get_docx_metadata(filepath)

    elif ext in [".mp3", ".flac", ".wav", ".m4a", ".ogg"]:
        result["audio_metadata"] = get_audio_metadata(filepath)

    else:
        result["note"] = "No specific metadata extractor for this file type — basic info and hashes extracted."

    return result