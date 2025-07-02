## Setup

Before running any scripts, create and activate a virtual environment:

```bash
python3.11 -m venv kokoro-env # 3.13 doesn't work

# Activate the virtual environment
source kokoro-env/bin/activate  # macOS/Linux
# or
source kokoro-env\Scripts\activate   # Windows/Git Bash

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
