## Audio Merging

This project generates multiple `.wav` audio files (e.g., one per chapter or segment). To combine these into a single audiobook file, use the `pydub` Python library along with `ffmpeg`.

### Requirements

* Python packages:

  * `pydub`
* System packages:

  * `ffmpeg` (must be installed separately)

### Installing Dependencies

```bash
pip install -r requirements.txt
# On macOS, install ffmpeg with:
brew install ffmpeg
```

### Combining Audio Files

Here’s a Python example to merge all chapter audio files in the `audiobook` folder into a single `.wav` file:

```python

```

Run this script after generating your individual `.wav` files.
