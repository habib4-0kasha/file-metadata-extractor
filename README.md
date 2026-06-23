# File Metadata Extractor

A Python-based digital forensics tool that extracts and analyses metadata from files, generates cryptographic hashes, and produces structured forensic reports.

Built as part of a DFIR (Digital Forensics & Incident Response) learning portfolio.

---

## What it does

- Extracts **file system metadata** — name, size, timestamps (created, modified, accessed)
- Generates **MD5, SHA1, and SHA256 hashes** for file integrity verification
- Extracts **EXIF data** from images (camera model, GPS coordinates, timestamps)
- Extracts **author and revision metadata** from PDF and Word documents
- Extracts **tag metadata** from audio files
- Outputs a formatted **text report** and a **JSON report** for every analysis

---

## Tools & Libraries

| Library | Purpose |
|---|---|
| `exifread` | EXIF metadata extraction from images |
| `python-docx` | Word document metadata |
| `PyPDF2` | PDF metadata |
| `mutagen` | Audio file metadata |
| `hashlib` | Cryptographic hashing (built-in) |
| `os / datetime` | File system info (built-in) |

---

## Installation

```bash
git clone https://github.com/habib4-0kasha/file-metadata-extractor.git
cd file-metadata-extractor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py path/to/yourfile.jpg
```

Or run it interactively:

```bash
python main.py
```

---

## Example Output

============================================================

FILE METADATA EXTRACTOR — DFIR TOOL
[ FILE INFO ]
filename            : photo.jpg

size_kb             : 214.3

created             : 2025-01-14 09:23:11

modified            : 2025-01-14 09:23:11
[ HASHES ]
MD5                 : a3f1c9e2...

SHA1                : 7bd4e120...

SHA256              : 9a2f871c...
[ IMAGE METADATA ]
Image Make                    : Apple

Image Model                   : iPhone 14 Pro

GPS GPSLatitude               : 24, 27, 36

GPS GPSLongitude              : 54, 22, 12

---

## Project Structure

file-metadata-extractor/
├── src/
│   ├── extractor.py      # Core metadata extraction logic
│   └── report.py         # Report generation (TXT + JSON)
├── samples/              # Drop files here to analyse (gitignored)
├── output/               # Reports saved here (gitignored)
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── README.md

---

## DFIR Relevance

- **Hash verification** is fundamental to maintaining chain of custody in forensic investigations
- **EXIF GPS data** has been used in real criminal investigations to place suspects at crime scenes
- **Document metadata** can expose the true author of a file, relevant in fraud and insider threat cases
- **Structured JSON output** can be ingested into SIEMs like Splunk for further analysis

---

## Author

**habib4-0kasha**
BSc Computer Science (Cybersecurity) — University of Wollongong in Dubai
[LinkedIn](https://linkedin.com/in/yourprofile)