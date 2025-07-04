import { KokoroTTS, TextSplitterStream } from "kokoro-js";

async function runKokoroTTS() {
  console.log('Kokoro TTS demo started');
  const model_id = "onnx-community/Kokoro-82M-v1.0-ONNX";
  const tts = await KokoroTTS.from_pretrained(model_id, {
    dtype: "fp32",
    device: "cpu", // Node.js: use CPU
  });
  console.log('Model loaded');

  const splitter = new TextSplitterStream();
  const stream = tts.stream(splitter);
  console.log('Stream set up');

  (async () => {
    let i = 0;
    for await (const { text, phonemes, audio } of stream) {
      console.log('Stream output:', { text, phonemes });
      await audio.save(`audio-${i++}.wav`);
      console.log(`Saved audio-${i-1}.wav`);
    }
    console.log('Stream finished');
  })();

  const text = "Kokoro is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, Kokoro can be deployed anywhere from production environments to personal projects. It can even run 100% locally in your browser, powered by Transformers.js!";
  const tokens = text.match(/\s*\S+/g);
  if (tokens) {
    for (const token of tokens) {
      splitter.push(token);
      console.log('Pushed token:', token);
      await new Promise((resolve) => setTimeout(resolve, 10));
    }
  }
  splitter.close();
  console.log('Splitter closed');
}

runKokoroTTS(); 