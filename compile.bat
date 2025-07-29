@echo off
start "Compilando edocs_extractor_rpa" .\venv\Scripts\python -m nuitka --standalone --onefile --output-dir=dist --output-filename=edocs_extractor_rpa .\main.py && ^
start "Compilando edocs_credentials" .\venv\Scripts\python -m nuitka --standalone --onefile --output-dir=dist --output-filename=edocs_credentials .\credentials.py && ^