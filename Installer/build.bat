@echo off
echo Compilando...

set TARGET=build/Installer.exe
set ICON=resources/icon.ico

rmdir /s /q build 2>nul
mkdir build 2>nul

windres resources.rc -O coff -o build/resources.res

g++ -o %TARGET% src/main.cpp build/resources.res ^
    thirdparty/imgui/src/*.cpp ^
    -Ithirdparty/imgui/include ^
    -lgdi32 -limm32 -luser32 -lkernel32 -ldwmapi -ld3d9 ^
    -lole32 -loleaut32 -lcomctl32 -luuid -lsetupapi ^
    -static -municode -Wl,-subsystem,windows

if exist %TARGET% (
    echo Build concluido com sucesso!
    
    if exist "%ICON%" (
        echo Verificando ícone no executavel...
        dir %TARGET%
    ) else (
        echo Arquivo de ícone não encontrado: %ICON%
    )
) else (
    echo Falha na compilação!
    echo Verifique:
    echo 1. Se o arquivo %ICON% existe
    echo 2. Se o windres está no PATH
)
pause