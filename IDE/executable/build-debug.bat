@echo off
echo Compilando..

set TARGET=build/Kingdom IDE-Debug.exe
set ICON=resources/icon.ico

rmdir /s /q build 2>nul
mkdir build 2>nul

windres resources.rc -O coff -o build/resources.res

g++ -o "%TARGET%" src/AppDebug.cpp build/resources.res

pause