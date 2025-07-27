@echo off
echo Setting up Challenge 1b environment...

:: Create necessary directories
if not exist "input" mkdir input
echo Created 'input' directory - place your PDF files here

if not exist "output" mkdir output
echo Created 'output' directory - output JSON files will be saved here

:: Install required Python packages
echo Installing required Python packages...
pip install -r requirements.txt

echo.
echo Setup complete!
echo 1. Place your PDF files in the 'input' directory
echo 2. Run 'python extract_outline.py'
echo 3. Check the 'output' directory for the results
