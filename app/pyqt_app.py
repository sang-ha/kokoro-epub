import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import soundfile as sf
import sounddevice as sd

# Import your kokoro pipeline
from kokoro import KPipeline

class TTSWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    audio_ready = pyqtSignal(str)

    def run(self):
        self.progress.emit("Loading Kokoro model...")
        pipeline = KPipeline(lang_code='a')
        text = (
            "Kokoro is an open-weight TTS model with 82 million parameters. "
            "Despite its lightweight architecture, it delivers comparable quality to larger models "
            "while being significantly faster and more cost-efficient."
        )
        self.progress.emit("Synthesizing speech...")
        for i, (_, _, audio) in enumerate(pipeline(text, voice='af_heart')):
            filename = f"output_{i}.wav"
            sf.write(filename, audio, 24000)
            self.progress.emit(f"Saved {filename}")
            self.audio_ready.emit(filename)
        self.finished.emit("Done! All audio files saved.")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kokoro TTS PyQt Demo")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        self.label = QLabel("Click the button to generate speech with Kokoro TTS.")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.button = QPushButton("Generate Sample Speech")
        self.button.clicked.connect(self.run_tts)
        layout.addWidget(self.button)

        self.play_button = QPushButton("Play Last Audio")
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self.play_audio)
        layout.addWidget(self.play_button)

        self.setLayout(layout)
        self.last_audio_file = None

    def run_tts(self):
        self.button.setEnabled(False)
        self.label.setText("Running TTS...")
        self.worker = TTSWorker()
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.tts_done)
        self.worker.audio_ready.connect(self.set_last_audio)
        self.worker.start()

    def update_status(self, msg):
        self.label.setText(msg)

    def tts_done(self, msg):
        self.label.setText(msg)
        self.button.setEnabled(True)
        self.play_button.setEnabled(self.last_audio_file is not None)

    def set_last_audio(self, filename):
        self.last_audio_file = filename
        self.play_button.setEnabled(True)

    def play_audio(self):
        if self.last_audio_file:
            data, samplerate = sf.read(self.last_audio_file)
            sd.play(data, samplerate)
            self.label.setText(f"Playing {self.last_audio_file}...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())