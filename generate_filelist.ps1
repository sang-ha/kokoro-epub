# generate_filelist.ps1

# Create filelists folder if it doesn't exist
New-Item -ItemType Directory -Force -Path filelists

$metadataPath = "data\LJSpeech-1.1\metadata.csv"
$filelistPath = "filelists\ljs_train.txt"

Get-Content $metadataPath | ForEach-Object {
    $line = $_ -split '\|'
    $file = "data\LJSpeech-1.1\wavs\" + $line[0] + ".wav"
    $text = $line[1]
    "$file|$text"
} | Set-Content $filelistPath

Write-Host "✅ Filelist generated at $filelistPath"
