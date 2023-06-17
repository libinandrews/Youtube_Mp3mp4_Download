@echo off

REM Install Python packages
pip install pandas pyperclip pytube numpy pandasgui moviepy

REM Install tkinter (included with Python)
REM Note: tkinter is usually already installed with Python, so this step may not be necessary

REM Install requests library
pip install requests

echo Dependencies installed successfully.
pause
