#include "App.h"

int main() {
    if (!InitIDE(false)) {
        std::cerr << "Nao foi possivel encontrar o caminho para o Python ou para o script de entrada" << std::endl;
		system("pause");
        return 1;
    }
    
    system("pause");
    return 0;
}