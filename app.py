import gradio as gr
from processor import process_epub
from merge_audio import merge_audio_files
import tempfile, os, shutil

def epub_to_mp3(epub_file):
    # temp folder inside container
    outdir = tempfile.mkdtemp()
    try:
        # generate wavs
        process_epub(epub_file.name, output_dir=outdir)
        # merge to mp3
        mp3_path = os.path.join(outdir, "full_book.mp3")
        merge_audio_files(folder=outdir, output_path=mp3_path)
        return mp3_path
    finally:
        shutil.rmtree(outdir, ignore_errors=True)

demo = gr.Interface(
    fn=epub_to_mp3,
    inputs=gr.File(file_types=[".epub"], label="Upload EPUB"),
    outputs=gr.File(label="Download MP3"),
    title="Kokoro EPUB → Audiobook",
    description="Upload an EPUB, get back an MP3 audiobook"
)

if __name__ == "__main__":
    demo.launch()
