@echo off
echo Generating challenge1b_output.json...
python generate_challenge1b_output.py

if exist challenge1b_output.json (
    echo.
    echo Success! Output file has been generated: challenge1b_output.json
    echo.
) else (
    echo.
    echo Error: Failed to generate the output file.
    echo Please make sure all dependencies are installed and try again.
    echo.
    pause
)
