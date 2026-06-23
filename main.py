import sys
import os
from src.extractor import extract
from src.report import generate_text_report, generate_json_report


def main():
    print("\n" + "=" * 60)
    print("     FILE METADATA EXTRACTOR — DFIR TOOL")
    print("     github.com/habib4-0kasha/file-metadata-extractor")
    print("=" * 60 + "\n")

    # Get filepath from user
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("Enter the path to the file you want to analyse: ").strip()

    # Validate file exists
    if not os.path.exists(filepath):
        print(f"\n[ERROR] File not found: {filepath}")
        sys.exit(1)

    print(f"\n[*] Analysing: {filepath}")
    print("[*] Extracting metadata...\n")

    # Run extraction
    try:
        data = extract(filepath)
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        sys.exit(1)

    # Display summary in terminal
    print("[ FILE INFO ]")
    print("-" * 40)
    for key, value in data["file_info"].items():
        print(f"  {key:<20}: {value}")

    print("\n[ HASHES ]")
    print("-" * 40)
    print(f"  {'MD5':<20}: {data['hashes']['md5']}")
    print(f"  {'SHA1':<20}: {data['hashes']['sha1']}")
    print(f"  {'SHA256':<20}: {data['hashes']['sha256']}")

    for section in ["image_metadata", "pdf_metadata", "docx_metadata", "audio_metadata"]:
        if section in data:
            print(f"\n[ {section.replace('_', ' ').upper()} ]")
            print("-" * 40)
            for key, value in data[section].items():
                print(f"  {str(key):<30}: {value}")

    if "note" in data:
        print(f"\n[ NOTE ]\n  {data['note']}")

    # Generate reports
    print("\n[*] Generating reports...")
    txt_path = generate_text_report(data)
    json_path = generate_json_report(data)

    print(f"\n[+] Text report saved to : {txt_path}")
    print(f"[+] JSON report saved to : {json_path}")
    print("\n" + "=" * 60)
    print("  Analysis complete.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()