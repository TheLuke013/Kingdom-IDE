#include <windows.h>

#include "App.h"

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PWSTR pCmdLine, int nCmdShow) {   
    if (!InitIDE(true)) {
        MessageBoxA(NULL, "Python não encontrado no caminho especificado", "Erro", MB_ICONERROR);
        return 1;
    }
    
    return 0;
}