@echo off
pushd %~dp0
title pyocus is running...

call .\.venv.\Scripts\activate.bat
py .\main.py

exit
