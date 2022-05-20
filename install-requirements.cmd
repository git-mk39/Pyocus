@echo off
pushd %~dp0
title installing requirements...

call .\.venv\Scripts\activate.bat
py -m pip install -r .\requirements.txt

pause
exit
