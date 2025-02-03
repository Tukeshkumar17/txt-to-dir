import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QIcon

class ChatbotDirectoryCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text To Directory Creator")
        self.setMinimumSize(500, 600)
        self.resize(500, 600)
        
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: white;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: bold;
                color: black;
            }
            QLabel#section {
                font-size: 14px;
                color: black;
                margin-top: 16px;
            }
            QLineEdit, QTextEdit {
                padding: 12px;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                background: white;
                font-size: 13px;
            }
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton#browse, QPushButton#load {
                background: #f5f5f5;
                border: 1px solid #e0e0e0;
            }
            QPushButton#browse:hover, QPushButton#load:hover {
                background: #e8e8e8;
            }
            QPushButton#create {
                background: #4285f4;
                color: white;
                border: none;
            }
            QPushButton#create:hover {
                background: #3b78e7;
            }
            QLabel#version {
                color: #666;
                font-size: 11px;
            }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Text To Directory Creator")
        title.setObjectName("title")
        layout.addWidget(title)

        location_label = QLabel("Location")
        location_label.setObjectName("section")
        layout.addWidget(location_label)

        location_row = QHBoxLayout()
        location_row.setSpacing(8)
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Select directory location...")
        self.location_input.setFixedHeight(40)
        
        browse_btn = QPushButton("📁")
        browse_btn.setObjectName("browse")
        browse_btn.setFixedSize(40, 40)
        browse_btn.clicked.connect(self.browse_directory)
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.add_hover_animation(browse_btn)
        
        location_row.addWidget(self.location_input)
        location_row.addWidget(browse_btn)
        layout.addLayout(location_row)

        config_label = QLabel("Chatbot Configuration")
        config_label.setObjectName("section")
        layout.addWidget(config_label)

        self.config_text = QTextEdit()
        self.config_text.setPlaceholderText("Enter your chatbot configuration here...")
        self.config_text.setMinimumHeight(200)
        layout.addWidget(self.config_text)

        load_btn = QPushButton("Load from Text File")
        load_btn.setObjectName("load")
        load_btn.setFixedHeight(40)
        load_btn.clicked.connect(self.load_from_file)
        load_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_hover_animation(load_btn)
        layout.addWidget(load_btn)

        create_btn = QPushButton("➕ Create Directory")
        create_btn.setObjectName("create")
        create_btn.setFixedHeight(40)
        create_btn.clicked.connect(self.create_directory)
        create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_hover_animation(create_btn)
        layout.addWidget(create_btn)

        version = QLabel("v0.1.0A")
        version.setObjectName("version")
        layout.addWidget(version)

        layout.addStretch()

    def add_hover_animation(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(100)
        button.enterEvent = lambda e: self.button_hover(button, True)
        button.leaveEvent = lambda e: self.button_hover(button, False)

    def button_hover(self, button, is_enter):
        geometry = button.geometry()
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(100)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        if is_enter:
            new_geometry = QRect(
                geometry.x() - 2,
                geometry.y() - 2,
                geometry.width() + 4,
                geometry.height() + 4
            )
        else:
            new_geometry = QRect(
                geometry.x() + 2,
                geometry.y() + 2,
                geometry.width() - 4,
                geometry.height() - 4
            )
            
        animation.setStartValue(geometry)
        animation.setEndValue(new_geometry)
        animation.start()

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.location_input.setText(directory)

    def load_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.config_text.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

    def create_directory(self):
        base_path = self.location_input.text().strip()
        structure_text = self.config_text.toPlainText().strip()

        if not base_path or not structure_text:
            QMessageBox.critical(self, "Error", "Please select a location and enter configuration.")
            return

        try:
            self.create_structure(base_path, structure_text)
            QMessageBox.information(self, "Success", "Directory structure created successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def create_structure(self, base_path, structure_text):
        lines = structure_text.split("\n")
        path_stack = [base_path]

        for line in lines:
            stripped_line = line.lstrip(" │├─└")
            indent_level = (len(line) - len(stripped_line)) // 2

            name = stripped_line.strip()
            if not name:
                continue

            while len(path_stack) > indent_level + 1:
                path_stack.pop()

            new_path = os.path.join(path_stack[-1], name)

            if "." in name:
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                open(new_path, 'w').close()
            else:
                os.makedirs(new_path, exist_ok=True)
                path_stack.append(new_path)

def main():
    app = QApplication(sys.argv)
    window = ChatbotDirectoryCreator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
