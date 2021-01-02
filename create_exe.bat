@echo off
pyinstaller -D -w -i=locked.ico PyPass.py
copy locked.ico dist/PyPass/locked.ico