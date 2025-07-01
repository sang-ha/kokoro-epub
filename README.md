## Setup

Before running any scripts, create and activate a virtual environment:

```bash
# Create virtual environment (only needed once)
python3 -m venv kokoro-env

# Activate the virtual environment
source kokoro-env/bin/activate  # macOS/Linux
# or
.\kokoro-env\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
````

---

## Requirements

* Python packages:

* Listed in `requirements.txt`
* System packages:

* `ffmpeg` (if you're using TTS that depends on it)

### Installing ffmpeg (macOS example):

```bash
brew install ffmpeg
```
