import sys
import pdb
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QScrollArea
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QDesktopServices, QCursor, QFont, QIcon
from PyQt5.QtCore import Qt, QUrl


class BrowserOpener(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TestBuddy by Md Ahmed Reza")
        self.setGeometry(100, 100, 900, 700)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)  # setting margins

        # Font and styling
        font = QFont()
        font.setPointSize(12)
        self.central_widget.setFont(font)

        name_label = QLabel('Welcome to TestBuddy. If you find this cool and want to reach out, send me hi <a href="mailto:ahmedreza80@gmail.com">Md Ahmed Reza</a>')
        name_label.setOpenExternalLinks(True)
        name_label.setStyleSheet("color: #555;")
        layout.addWidget(name_label, alignment=Qt.AlignTop | Qt.AlignRight)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL")
        self.url_input.setFixedHeight(40)
        layout.addWidget(self.url_input, alignment=Qt.AlignTop)

        self.label = QLabel("Select a browser:")
        layout.addWidget(self.label)

        self.browser_options = ["Chrome", "Edge", "Firefox", "Safari"]
        self.browser_radio_buttons = []

        for browser in self.browser_options:
            radio_button = QRadioButton(browser)
            radio_button.setIcon(QIcon(f"{browser.lower()}.png"))  # Assumes you have icons named like chrome.png, edge.png etc.
            layout.addWidget(radio_button)
            self.browser_radio_buttons.append(radio_button)

        self.open_button = QPushButton("Open Browser")
        self.open_button.setStyleSheet("background-color: #0099CC; color: white; padding: 10px; border: none; border-radius: 5px;")
        self.open_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.open_button.clicked.connect(self.open_virtual_browser)
        layout.addWidget(self.open_button)

        self.debug_button = QPushButton("Open Debugger")
        self.debug_button.setStyleSheet("background-color: #0099CC; color: white; padding: 10px; border: none; border-radius: 5px;")
        self.debug_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.debug_button.clicked.connect(self.open_debugger)
        layout.addWidget(self.debug_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.browser_scroll_area = QScrollArea()
        self.browser_scroll_area.setWidgetResizable(True)
        layout.addWidget(self.browser_scroll_area)

        self.browser_view = QWebEngineView()
        self.browser_scroll_area.setWidget(self.browser_view)
        self.browser_view.setFixedSize(800, 600)

        self.central_widget.setLayout(layout)


    def open_virtual_browser(self):
        selected_browser = None

        for radio_button in self.browser_radio_buttons:
            if radio_button.isChecked():
                selected_browser = radio_button.text()
                break

        if selected_browser:
            url = self.url_input.text()
            if not url:
                self.result_label.setText("Please enter a URL.")
                return

            self.result_label.setText(f"Opening {selected_browser}...")

            # Create a QWebEngineView to display the web content
            self.browser_view.setUrl(QUrl(url))

            self.result_label.setText(f"Opened {selected_browser}")
        else:
            self.result_label.setText("Please select a browser.")
    
    def open_debugger(self):
        # Launch the debugger when the debugger button is clicked
        code_to_debug = self.url_input.text()  # Use the URL input field for debugging
        debugger = pdb.Pdb()
        debugger.reset()
        debugger.run(code_to_debug)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser_opener = BrowserOpener()
    browser_opener.show()
    sys.exit(app.exec_())