function init() {
  window.addEventListener('DOMContentLoaded', () => {
    doAThing()
    const ttsBtn = document.getElementById('ttsDemoBtn');
    if (ttsBtn) {
      ttsBtn.addEventListener('click', async () => {
        ttsBtn.disabled = true;
        ttsBtn.textContent = 'Running TTS...';
        try {
          await window.api.runKokoroTTS();
          ttsBtn.textContent = 'TTS Complete!';
        } catch (e) {
          ttsBtn.textContent = 'Error!';
          console.error(e);
        }
        setTimeout(() => {
          ttsBtn.textContent = 'Run TTS Demo';
          ttsBtn.disabled = false;
        }, 2000);
      });
    }
  })
}

function doAThing() {
  const versions = window.electron.process.versions
  replaceText('.electron-version', `Electron v${versions.electron}`)
  replaceText('.chrome-version', `Chromium v${versions.chrome}`)
  replaceText('.node-version', `Node v${versions.node}`)

  const ipcHandlerBtn = document.getElementById('ipcHandler')
  ipcHandlerBtn?.addEventListener('click', () => {
    window.electron.ipcRenderer.send('ping')
  })
}

function replaceText(selector, text) {
  const element = document.querySelector(selector)
  if (element) {
    element.innerText = text
  }
}

init()
