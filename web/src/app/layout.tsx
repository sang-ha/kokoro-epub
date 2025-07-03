import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "VibeTails – AI Audiobook Generator",
  description:
    "Turn your EPUBs into expressive AI-narrated audiobooks with VibeTails.",
  keywords: [
    "AI audiobook",
    "EPUB to audio",
    "text-to-speech",
    "VibeTails",
    "audiobook generator",
  ],
  openGraph: {
    title: "VibeTails – AI Audiobook Generator",
    description:
      "Turn your EPUBs into expressive AI-narrated audiobooks with VibeTails.",
    url: "https://vibetails.com",
    siteName: "VibeTails",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "VibeTails – AI Audiobook Generator",
    description:
      "Turn your EPUBs into expressive AI-narrated audiobooks with VibeTails.",
    site: "@adnjoo", // replace if you have one
    creator: "@adnjoo",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-white text-gray-900`}
      >
        {children}
      </body>
    </html>
  );
}
