@echo off
echo Compilado todo projeto...

mkdir bin 2>nul

if not exist "Installer/build/Installer.exe" (
	echo Compilando Instalador:
	cd Installer
	call build
	cd ..
) else (
	echo Installer ja foi compilado
)

if not exist "IDE/executable/build/Kingdom IDE-Debug.exe" (
	echo Compilando Executavel:
	cd IDE/executable
	call build-debug
	
	echo Instalando dependencias
	cd ..
	call install-dependencies
	
	cd ..
) else (
	echo Kingdom IDE ja foi compilado
)




echo Copiando Executaveis...

if exist "Installer\build\Installer.exe" (
    copy "Installer\build\Installer.exe" "bin\Installer.exe" >nul
    echo ✅ Installer.exe copiado
) else (
    echo ❌ Arquivo Installer.exe não encontrado!
    exit /b 1
)

if exist "IDE\executable\build\Kingdom IDE-Debug.exe" (
    copy "IDE\executable\build\Kingdom IDE-Debug.exe" "bin\Kingdom IDE-Debug.exe" >nul
    echo ✅ Kingdom IDE-Debug.exe copiado
) else (
    echo ❌ Arquivo Kingdom IDE-Debug.exe não encontrado!
    exit /b 1
)


pause