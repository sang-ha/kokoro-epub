import argparse, sys
from pathlib import Path
import shutil
import re
from pipeline import epub_to_audio, extract_chapters, DEFAULT_VOICE

def sanitize_filename(filename):
    """Remove or replace characters that are invalid in filenames"""
    # Replace invalid characters with underscores
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra whitespace and limit length
    filename = filename.strip()[:100]
    return filename

def main():
    parser = argparse.ArgumentParser(description="EPUB → Audiobook CLI")
    parser.add_argument("epub", help="Path to EPUB file")
    parser.add_argument("--out", default="output", help="Output directory")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Voice (default af_heart)")
    parser.add_argument("--speed", type=float, default=1.0, help="Playback speed multiplier")
    parser.add_argument("--format", choices=["MP3","M4B"], default="MP3", help="Output format")
    parser.add_argument("--list-chapters", action="store_true", help="List chapters and exit")
    parser.add_argument("--chapters", help="Comma-separated chapter titles to convert", default=None)
    parser.add_argument("--separate-chapters", action="store_true", help="Create separate files for each chapter")
    args = parser.parse_args()

    epub_path = Path(args.epub)
    chapters = extract_chapters(str(epub_path))

    # Dry run
    if args.list_chapters:
        print(f"\n📖 {epub_path.name} — {len(chapters)} chapters found:\n")
        for i, (title, text) in enumerate(chapters, 1):
            print(f"{i:02d}. {title} ({len(text.split())} words)")
        sys.exit(0)

    # Create output directory
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Determine which chapters to process
    chapters_to_process = []
    if args.chapters:
        parts = [c.strip() for c in args.chapters.split(",")]
        for p in parts:
            if p.isdigit():
                idx = int(p) - 1
                if 0 <= idx < len(chapters):
                    chapters_to_process.append((idx, chapters[idx]))
            else:
                # Find chapter by title
                for idx, (title, text) in enumerate(chapters):
                    if p.lower() in title.lower():
                        chapters_to_process.append((idx, (title, text)))
                        break
    else:
        chapters_to_process = [(idx, chapter) for idx, chapter in enumerate(chapters)]

    if args.separate_chapters:
        # Process each chapter separately
        print(f"\n🎧 Processing {len(chapters_to_process)} chapters separately...")
        
        result_files = []
        for chapter_idx, (title, text) in chapters_to_process:
            print(f"\n📝 Processing Chapter {chapter_idx + 1}: {title}")
            
            # Create a temporary single-chapter list
            single_chapter = [f"{title} ({len(text.split())} words)"]
            
            result_file = None
            last_logs = ""
            
            for mp3_out, m4b_out, logs in epub_to_audio(
                epub_path.open("rb"),
                args.voice,
                args.speed,
                single_chapter,  # Process only this chapter
                args.format.upper(),
                cli=True,
            ):
                if logs and logs != last_logs:
                    diff = logs[len(last_logs):]
                    if diff.strip():
                        for line in diff.strip().splitlines():
                            print("   " + line)
                    last_logs = logs
                
                if mp3_out or m4b_out:
                    tmp_result = Path(mp3_out or m4b_out)
                    
                    # Create chapter-specific filename
                    sanitized_title = sanitize_filename(title)
                    chapter_number = f"{chapter_idx + 1:02d}"
                    extension = ".mp3" if args.format.upper() == "MP3" else ".m4b"
                    
                    final_filename = f"{chapter_number}_{sanitized_title}{extension}"
                    final_path = out_dir / final_filename
                    
                    shutil.copy(tmp_result, final_path)
                    result_file = final_path
                    result_files.append(final_path)
            
            if result_file:
                print(f"   ✅ Chapter saved: {result_file.name}")
        
        print(f"\n🎉 All chapters processed! {len(result_files)} files created in: {out_dir}")
        for file in result_files:
            print(f"   📄 {file.name}")
    
    else:
        # Original behavior - single combined file
        selected = []
        if args.chapters:
            parts = [c.strip() for c in args.chapters.split(",")]
            for p in parts:
                if p.isdigit():
                    idx = int(p) - 1
                    if 0 <= idx < len(chapters):
                        selected.append(f"{chapters[idx][0]} ({len(chapters[idx][1].split())} words)")
                else:
                    selected.append(p)

        result_file = None
        last_logs = ""
        for mp3_out, m4b_out, logs in epub_to_audio(
            epub_path.open("rb"),
            args.voice,
            args.speed,
            selected,
            args.format.upper(),
            cli=True,
        ):
            if logs and logs != last_logs:
                diff = logs[len(last_logs):]
                if diff.strip():
                    for line in diff.strip().splitlines():
                        print("   " + line)
                last_logs = logs
            
            if mp3_out or m4b_out:
                tmp_result = Path(mp3_out or m4b_out)

                # Rebuild filename in final output dir
                final_path = out_dir / tmp_result.name
                shutil.copy(tmp_result, final_path)
                result_file = final_path

        print(f"\n✅ Audiobook ready: {result_file}")

if __name__ == "__main__":
    main()
