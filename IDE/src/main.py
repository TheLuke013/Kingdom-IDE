import sys
import ctypes
import argparse
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from app import KingdomIDE

def parse_arguments():
    parser = argparse.ArgumentParser(description='Kingdom IDE')
    parser.add_argument('project', nargs='?', default=None, help='Project directory path')
    return parser.parse_args()

def main():
    myappid = 'thrillerempress.kingdom_ide'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    args = parse_arguments()
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../icon.ico"))
    ide = KingdomIDE(args.project)
    ide.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()