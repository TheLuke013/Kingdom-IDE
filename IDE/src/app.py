from PySide6.QtWidgets import (QApplication, QMainWindow, QDockWidget, 
                              QWidget, QVBoxLayout, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from pathlib import Path
import os

from editor.python_editor import PythonEditor
from file_explorer import FileExplorer
from terminal import Terminal

class KingdomIDE(QMainWindow):
    def __init__(self, work_root_path=None):
        super().__init__()
        self.setWindowTitle("Kingdom IDE")
        self.resize(1200, 800)
        
        self.work_root_path = Path(work_root_path) if work_root_path else None
        self.editor = None
        self.editor_dock = None
        self.file_explorer = None
        self.current_file = None
        self.terminal = None
        
        self.setup_dark_theme()
        self.setup_docks()
        self.create_menu_bar()
        self.setup_terminal()
        
        settings = QSettings("KingdomIDE", "Layout")
        if settings.value("geometry"):
            self.restoreGeometry(settings.value("geometry"))
        if settings.value("window_state"):
            self.restoreState(settings.value("window_state"))
                
        self.setup_shortcuts()
        
    def setup_shortcuts(self):
        self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut_save.activated.connect(self.save_current_file)
        
        if hasattr(self, 'file_explorer') and self.file_explorer:
            self.shortcut_new_file = QShortcut(QKeySequence("Ctrl+N"), self)
            self.shortcut_new_file.activated.connect(self.file_explorer.create_new_file)
            
            self.shortcut_rename = QShortcut(QKeySequence("F2"), self)
            self.shortcut_rename.activated.connect(self.file_explorer.rename_selected)
            
            self.shortcut_delete = QShortcut(QKeySequence("Delete"), self)
            self.shortcut_delete.activated.connect(self.file_explorer.delete_selected)
    
    def setup_terminal(self):
        self.terminal = Terminal()
        terminal_dock = QDockWidget("Terminal", self)
        terminal_dock.setWidget(self.terminal)
        terminal_dock.setFixedHeight(200)
        self.addDockWidget(Qt.BottomDockWidgetArea, terminal_dock)
        
        settings = QSettings("KingdomIDE", "Terminal")
        if settings.value("geometry"):
            terminal_dock.restoreGeometry(settings.value("geometry"))
            
    def save_current_file(self):
        if hasattr(self, 'editor') and self.editor:
            if hasattr(self.editor, 'save_file'):
                self.editor.save_file()
            
    def setup_docks(self):
        self.create_editor_dock()
        
        self.create_file_explorer_dock()
        
        self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.TopRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)
        
        self.setDockOptions(
            QMainWindow.DockOption.AllowNestedDocks |
            QMainWindow.DockOption.AllowTabbedDocks |
            QMainWindow.DockOption.GroupedDragging
        )
    
    def create_file_explorer_dock(self):
        self.file_explorer = FileExplorer(self, self.work_root_path)
        self.file_explorer.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_explorer)
        
        self.file_explorer.file_opened.connect(self.open_file_in_editor)
        self.file_explorer.file_created.connect(self.open_file_in_editor)
        
        if self.file_explorer:
            self.file_explorer.file_execute_requested.connect(self.execute_file)
    
    def open_file_in_editor(self, file_path):
        try:
            error = self.editor.open_file(file_path)
            if error is True:
                self.statusBar().showMessage(f"Arquivo aberto: {file_path}")
            else:
                self.statusBar().showMessage(f"Erro: {error}")
        except Exception as e:
            self.statusBar().showMessage(f"Erro ao abrir arquivo: {str(e)}")
    
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("Arquivo")
        
        change_dir_action = QAction("Mudar Diretório de Trabalho", self)
        change_dir_action.triggered.connect(self.change_work_directory)
        file_menu.addAction(change_dir_action)
        
        new_action = QAction("Novo", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("Abrir...", self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        tools_menu = menu_bar.addMenu("Ferramentas")
        run_action = QAction("Executar", self)
        run_action.triggered.connect(self.run_code)
        tools_menu.addAction(run_action)
        
        if self.editor:
            edit_menu = menu_bar.addMenu("Editar")
            
            undo_action = QAction("Desfazer", self)
            undo_action.triggered.connect(self.editor.undo)
            edit_menu.addAction(undo_action)
            
            redo_action = QAction("Refazer", self)
            redo_action.triggered.connect(self.editor.redo)
            edit_menu.addAction(redo_action)
            
            edit_menu.addSeparator()
            
            cut_action = QAction("Recortar", self)
            cut_action.triggered.connect(self.editor.cut)
            edit_menu.addAction(cut_action)
            
            copy_action = QAction("Copiar", self)
            copy_action.triggered.connect(self.editor.copy)
            edit_menu.addAction(copy_action)
            
            paste_action = QAction("Colar", self)
            paste_action.triggered.connect(self.editor.paste)
            edit_menu.addAction(paste_action)
            
            save_action = QAction("Salvar", self)
            save_action.triggered.connect(self.save_current_file)
            file_menu.addAction(save_action)

    def change_work_directory(self):
        new_dir = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Novo Diretório de Trabalho",
            str(self.work_root_path) if self.work_root_path else ""
        )
        
        if new_dir:
            self.work_root_path = Path(new_dir)
            if self.file_explorer:
                self.file_explorer.set_root_path(new_dir)
            self.statusBar().showMessage(f"Diretório alterado para: {new_dir}")
            
    def execute_file(self, file_path):
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            commands = {
                '.bat': f'cmd /c "{file_path}"',
                '.vbs': f'wscript "{file_path}"',
                '.sh': f'bash "{file_path}"',
                '.py': f'python "{file_path}"',
                '.exe': f'"{file_path}"'
            }
            
            if file_ext in commands:
                cmd = commands[file_ext]
                if self.terminal:
                    self.terminal.execute_command(cmd)
                    self.statusBar().showMessage(f"Executando: {os.path.basename(file_path)}")
                else:
                    QMessageBox.warning(self, "Aviso", "Terminal não disponível")
            else:
                QMessageBox.warning(self, "Aviso", f"Extensão {file_ext} não suportada para execução")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao executar arquivo:\n{str(e)}")
            
    def run_code(self):
        if self.editor and self.editor.current_file:
            file_path = Path(self.editor.current_file)
            
            if file_path.suffix == '.py':
                self.save_current_file()
                cmd = f'python "{file_path}"'
                
                if self.terminal:
                    self.terminal.execute_command(cmd)
                    self.statusBar().showMessage(f"Executando: {file_path.name}")
                else:
                    self.statusBar().showMessage("Terminal não disponível para execução")
            else:
                self.statusBar().showMessage("Arquivo não é um script Python (.py)")
        else:
            self.statusBar().showMessage("Nenhum arquivo aberto para executar")          
    
    def new_file(self):
        self.editor.clear()
        self.statusBar().showMessage("Novo arquivo criado")
    
    def save_current_file(self):
        if self.editor and hasattr(self.editor, 'save_file'):
            result = self.editor.save_file()
            if result:
                self.statusBar().showMessage("Arquivo salvo com sucesso")
            else:
                self.statusBar().showMessage("Erro ao salvar arquivo")
        else:
            self.statusBar().showMessage("Editor não disponível para salvar")
        
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir arquivo", "", "Python Files (*.py);;All Files (*)")
        if file_name:
            try:
                with open(file_name, "r") as f:
                    self.editor.setPlainText(f.read())
                self.current_file = file_name
                self.status_bar.showMessage(f"Arquivo aberto: {file_name}")
            except Exception as e:
                self.status_bar.showMessage(f"Erro ao abrir arquivo: {str(e)}")
    
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as f:
                    f.write(self.editor.toPlainText())
                self.status_bar.showMessage(f"Arquivo salvo: {self.current_file}")
            except Exception as e:
                self.status_bar.showMessage(f"Erro ao salvar arquivo: {str(e)}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar arquivo como", "", "Python Files (*.py);;All Files (*)")
        if file_name:
            if not file_name.endswith(".py"):
                file_name += ".py"
            self.current_file = file_name
            self.save_file()
    
    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir arquivo", "", "Python Files (*.py);;All Files (*)")
        if file_name:
            error = self.editor.open_file(file_name)
            if error is True:
                self.statusBar().showMessage(f"Arquivo aberto: {file_name}")
            else:
                self.statusBar().showMessage(f"Erro: {error}")
    
    def closeEvent(self, event):
        settings = QSettings("KingdomIDE", "Layout")
        
        settings.setValue("editor_width", self.editor_dock.width())
        settings.setValue("explorer_width", self.file_explorer.width())
        
        settings.setValue("window_state", self.saveState())
        settings.setValue("geometry", self.saveGeometry())
        
        super().closeEvent(event)
        
    def create_editor_dock(self):
        self.editor = PythonEditor()
        
        self.editor_dock = QDockWidget("Editor", self)
        self.editor_dock.setWidget(self.editor)
        self.editor_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
    
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.editor_dock)
    
    def setup_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #252526;
                color: #D4D4D4;
            }
            QDockWidget {
                background: #1E1E1E;
                border: 1px solid #3F3F46;
            }
            QDockWidget::title {
                background: #252526;
                padding: 5px;
                text-align: left;
            }
        """)