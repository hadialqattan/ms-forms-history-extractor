# Build script for Windows platform!

pip install pyinstaller

pyinstaller --clean -y --onefile main.py

mv .\dist\main.exe .\run.exe

$compress = @{
  Path = ".\run.exe", ".\webview\", ".\LICENSE", ".\README.md"
  CompressionLevel = "Fastest"
  DestinationPath = ".\ms-forms-history-extractor"
}
Compress-Archive @compress

rm -r .\__pycache__, .\build, .\dist, .\main.spec, .\run.exe
