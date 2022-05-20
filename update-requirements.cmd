@echo off
pushd %~dp0
title updating requirements...

call .\.venv\Scripts\activate.bat
py -m pip freeze > .\requirements.txt

echo DONE!
timeout /t 1
exit
