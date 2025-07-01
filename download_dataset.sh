#!/usr/bin/env bash

# Exit script on error
set -e

DATA_DIR="data/LJSpeech-1.1"
URL="https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2"
TMP="data/LJSpeech-1.1.tar.bz2"

mkdir -p data
echo "Downloading LJSpeech dataset..."
wget -c "$URL" -O "$TMP"

echo "Extracting dataset..."
tar xjf "$TMP" -C data

echo "Cleaning up..."
rm "$TMP"

echo "✅ LJSpeech dataset is ready at '$DATA_DIR'"
