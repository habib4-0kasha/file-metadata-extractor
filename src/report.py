import json
import os
from datetime import datetime


def generate_text_report(data, output_dir="output"):
    """Generate a readable text report, like a real forensic report."""
    os.makedirs(output_dir, exist_ok=True)

    filename = data["file_info"]["filename"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"report_{filename}_{timestamp}.txt")

    with open(report_path, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("        DIGITAL FORENSICS — METADATA EXTRACTION REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Investigator: [Your Name]\n")
        f.write("=" * 60 + "\n\n")

        # File Info
        f.write("[ FILE INFORMATION ]\n")
        f.write("-" * 40 + "\n")
        for key, value in data["file_info"].items():
            f.write(f"  {key:<20}: {value}\n")
        f.write("\n")

        # Hashes
        f.write("[ CRYPTOGRAPHIC HASHES ]\n")
        f.write("-" * 40 + "\n")
        f.write(f"  {'MD5':<20}: {data['hashes']['md5']}\n")
        f.write(f"  {'SHA1':<20}: {data['hashes']['sha1']}\n")
        f.write(f"  {'SHA256':<20}: {data['hashes']['sha256']}\n")
        f.write("\n")

        # Type-specific metadata
        for section in ["image_metadata", "pdf_metadata", "docx_metadata", "audio_metadata"]:
            if section in data:
                title = section.replace("_", " ").upper()
                f.write(f"[ {title} ]\n")
                f.write("-" * 40 + "\n")
                for key, value in data[section].items():
                    f.write(f"  {str(key):<30}: {value}\n")
                f.write("\n")

        if "note" in data:
            f.write(f"[ NOTE ]\n  {data['note']}\n\n")

        f.write("=" * 60 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 60 + "\n")

    return report_path


def generate_json_report(data, output_dir="output"):
    """Generate a JSON report, useful for feeding into other tools or SIEMs."""
    os.makedirs(output_dir, exist_ok=True)

    filename = data["file_info"]["filename"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"report_{filename}_{timestamp}.json")

    with open(report_path, "w") as f:
        json.dump(data, f, indent=4, default=str)

    return report_path