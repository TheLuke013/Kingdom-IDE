#include <cstdio>
#include <iostream>
#include <string>
#include "SimpleIni.h"

bool ReadIDEConfig(std::string& entryMainScriptPython, std::string& pythonPath) {
    CSimpleIniA ini;
    ini.LoadFile("../config.ini");
    
    entryMainScriptPython = ini.GetValue(
        "EnvironmentVariables",
        "EntryMainScriptPython",
        "..\\IDE\\src\\main.py"
    );

    pythonPath = ini.GetValue(
        "EnvironmentVariables",
        "PythonPath",
        "..\\IDE\\venv\\Scripts\\python.exe"
    );
    
    return true;
}

#include <windows.h>

bool InitIDE(bool hideConsole) {
    std::string entryMainScriptPython;
    std::string pythonPath;

    ReadIDEConfig(entryMainScriptPython, pythonPath);

    std::string command = pythonPath + " " + entryMainScriptPython;

    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi;

    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = hideConsole ? SW_HIDE : SW_SHOW;

    DWORD creationFlags = hideConsole ? CREATE_NO_WINDOW : CREATE_NEW_CONSOLE;

    BOOL success = CreateProcessA(
        NULL,
        (LPSTR)command.c_str(),
        NULL,
        NULL,
        FALSE,
        creationFlags,
        NULL,
        NULL,
        &si,
        &pi
    );

    if (success) {
        WaitForSingleObject(pi.hProcess, INFINITE);

        DWORD exitCode;
        GetExitCodeProcess(pi.hProcess, &exitCode);

        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);

        return (exitCode == 0);
    }

    return false;
}

