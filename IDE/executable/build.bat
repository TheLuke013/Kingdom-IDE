@echo off
echo Compilando..

set TARGET="build/Kingdom IDE.exe"
set ICON=resources/icon.ico

rmdir /s /q build 2>nul
mkdir build 2>nul

windres resources.rc -O coff -o build/resources.res

g++ -o %TARGET% src/main.cpp build/resources.res ^
    -lgdi32 -limm32 -luser32 -lkernel32 -ldwmapi -ld3d9 ^
    -lole32 -loleaut32 -lcomctl32 -luuid -lsetupapi ^
    -static -municode -Wl,-subsystem,windows -Wl,-entry:WinMainCRTStartup

if exist %TARGET% (
    echo ✅ Build concluído com sucesso!
    
    if exist "%ICON%" (
        echo Verificando ícone no executável...
        dir %TARGET%
    ) else (
        echo ⚠️ Arquivo de ícone não encontrado: %ICON%
    )
) else (
    echo ❌ Falha na compilação!
    echo Verifique:
    echo 1. Se o arquivo %ICON% existe
    echo 2. Se o windres está no PATH
    echo 3. Se o ponto de entrada (WinMain/wWinMain) está correto
)
pause