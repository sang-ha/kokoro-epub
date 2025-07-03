"use client";

import { useEffect } from "react";

declare global {
  interface Window {
    Tally?: {
      loadEmbeds: () => void;
    };
  }
}

export default function Home() {
  useEffect(() => {
    // Load the Tally script dynamically (once)
    const scriptId = "tally-script";
    if (!document.getElementById(scriptId)) {
      const script = document.createElement("script");
      script.id = scriptId;
      script.src = "https://tally.so/widgets/embed.js";
      script.onload = () => {
        if (window.Tally) window.Tally.loadEmbeds();
      };
      document.body.appendChild(script);
    } else if (window.Tally) {
      window.Tally.loadEmbeds();
    }
  }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-sans">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start max-w-xl w-full">
        <h1 className="text-5xl font-extrabold tracking-tight">VibeTails</h1>
        <p className="text-lg sm:text-xl max-w-md text-center sm:text-left">
          Turn books into voice. Feel the story. Hear the vibe.
        </p>

        {/* YouTube Audiobook Embed */}
        <div className="w-full aspect-video max-w-md">
          <iframe
            className="w-full h-full rounded-xl shadow-lg"
            src="https://www.youtube.com/embed/U53meKrKFYo"
            title="The Great Gatsby Audiobook"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>

        {/* Tally Form Embed */}
        <div className="w-full max-w-md">
          <iframe
            data-tally-src="https://tally.so/embed/mZA7vV?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1"
            loading="lazy"
            width="100%"
            height="442"
            frameBorder="0"
            marginHeight={0}
            marginWidth={0}
            title="VibeTails"
          ></iframe>
        </div>
      </main>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center text-sm opacity-60">
        <p>© 2025 VibeTails. All rights reserved.</p>
        <a
          href="https://www.stacktosale.com/"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:underline"
        >
          Made with ❤️ by S2S team
        </a>
      </footer>
    </div>
  );
}
