#include <windows.h>
#include <cstdio>
#include <iostream>
#include <string>

#ifdef DEVELOPMENT
    #define PYTHON_PATH "..\\IDE\\venv\\Scripts\\python.exe"
    #define PYTHON_MAIN_SCRIPT "..\\IDE\\src\\main.py"
    
    int main() {
		std::string command = std::string(PYTHON_PATH) + " " + PYTHON_MAIN_SCRIPT;
		
		std::cerr << "Executando comando: " << command << "\n";
		
		int result = system(command.c_str());
		
		if (result != 0) {
			std::cerr << "Erro ao executar o comando. Código: " << result << "\n";
			std::cerr << "Verifique os caminhos:\n";
			std::cerr << "Python: " << PYTHON_PATH << "\n";
			std::cerr << "Script: " << PYTHON_MAIN_SCRIPT << "\n";
		}
		
		system("pause");
		return 0;
	}
#else
    #define PYTHON_PATH "python\\python.exe"
    #define PYTHON_MAIN_SCRIPT "IDE\\src\\main.py"
    
    int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PWSTR pCmdLine, int nCmdShow) {
        char command[512];
        snprintf(command, sizeof(command), "\"%s\" \"%s\"", PYTHON_PATH, PYTHON_MAIN_SCRIPT);
        
        DWORD attrs = GetFileAttributesA(PYTHON_PATH);
        if (attrs == INVALID_FILE_ATTRIBUTES) {
            MessageBoxA(NULL, "Python não encontrado no caminho especificado", "Erro", MB_ICONERROR);
            return 1;
        }
        
        system(command);
        return 0;
    }
#endif