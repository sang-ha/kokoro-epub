from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from kokoro import KPipeline
import soundfile as sf
import os

# --- Config ---
book_path = "relax.epub"
output_dir = "audiobook"
lang_code = 'a'
voice = 'af_heart'
os.makedirs(output_dir, exist_ok=True)

# --- TTS Init ---
pipeline = KPipeline(lang_code=lang_code)

# --- Load EPUB ---
book = epub.read_epub(book_path)
chapters = [item for item in book.items if item.get_type() == ITEM_DOCUMENT]

for i, chapter in enumerate(chapters):
    soup = BeautifulSoup(chapter.get_content(), 'html.parser')
    text = soup.get_text().strip()
    if len(text) < 100:
        continue  # skip empty chapters

    print(f"Processing chapter {i}: {chapter.get_name()}")

    for j, (_, _, audio) in enumerate(pipeline(text, voice=voice, speed=1)):
        filename = f"{output_dir}/chapter_{i:02d}_{j}.wav"
        sf.write(filename, audio, 24000)
