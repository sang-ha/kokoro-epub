import { useState, useCallback } from 'react';
import Versions from './components/Versions'
import electronLogo from './assets/electron.svg'

function App(): React.JSX.Element {
  const [droppedFile, setDroppedFile] = useState<File | null>(null);
  const [output, setOutput] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [running, setRunning] = useState<boolean>(false);

  const onDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      const file = event.dataTransfer.files[0];
      if (file.name.endsWith('.epub')) {
        setDroppedFile(file);
        setOutput('');
        setError('');
      } else {
        setDroppedFile(null);
        setOutput('');
        setError('Please drop an .epub file.');
      }
    }
  }, []);

  const onDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  const runScript = async () => {
    if (!droppedFile) return;
    setRunning(true);
    setOutput('');
    setError('');
    try {
      // Use the path property (Electron provides it on File objects)
      // Fallback to name if path is not available
      // You may need to adjust the script path and arguments as needed
      // Example: '../scripts/script.py' and [droppedFile.path]
      // For demo, just echo the file path
      const scriptPath = '../scripts/script.py';
      // @ts-ignore
      const filePath = (droppedFile as any).path || droppedFile.name;
      const result = await (window.api as {
        runPythonScript: (scriptRelativePath: string, args?: string[]) => Promise<{ code: number, stdout: string, stderr: string }>
      }).runPythonScript(scriptPath, [filePath]);
      setOutput(result.stdout || '(no output)');
      if (result.stderr) setError(result.stderr);
    } catch (err: any) {
      setError(err.message || String(err));
    } finally {
      setRunning(false);
    }
  };

  return (
    <>
      <img alt="logo" className="logo" src={electronLogo} />
      <div className="creator">Powered by electron-vite</div>
      <div className="text">
        Drag and drop an <span className="react">.epub</span> file below
      </div>
      <div
        onDrop={onDrop}
        onDragOver={onDragOver}
        style={{
          border: '2px dashed #3178c6',
          borderRadius: 12,
          padding: 40,
          margin: '24px 0',
          background: '#222',
          color: '#fff',
          textAlign: 'center',
        }}
      >
        {droppedFile ? (
          <>
            <div>File: <b>{droppedFile.name}</b></div>
            <button onClick={runScript} disabled={running} style={{marginTop: 16, padding: '8px 24px', fontSize: 16}}>
              {running ? 'Running...' : 'Run Python Script'}
            </button>
          </>
        ) : (
          <div>Drop your .epub file here</div>
        )}
        {error && <div style={{ color: 'red', marginTop: 12 }}>{error}</div>}
        {output && <pre style={{ color: 'lime', marginTop: 12, textAlign: 'left', maxWidth: 400, overflowX: 'auto' }}>{output}</pre>}
      </div>
      <Versions></Versions>
    </>
  )
}

export default App
