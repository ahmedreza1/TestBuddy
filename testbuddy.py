import sys
import pdb
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QScrollArea
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QDesktopServices, QCursor, QFont, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QButtonGroup  # Import QButtonGroup


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
        layout.setContentsMargins(30, 30, 30, 30)

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

        # Create button groups
        self.browser_button_group = QButtonGroup(self)  # Group for browser options
        self.mobile_device_button_group = QButtonGroup(self)  # Group for mobile device options

        self.browser_options = ["Chrome", "Edge", "Firefox", "Safari"]
        self.browser_radio_buttons = []

        size_layout = QHBoxLayout()
        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Width")
        self.width_input.setFixedWidth(100)
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Height")
        self.height_input.setFixedWidth(100)
        size_button = QPushButton("Set Size")
        size_button.clicked.connect(self.set_browser_size)
        
        size_layout.addWidget(self.width_input)
        size_layout.addWidget(self.height_input)
        size_layout.addWidget(size_button)
        layout.addLayout(size_layout)

        self.mobile_device_label = QLabel("Select a mobile device:")
        layout.addWidget(self.mobile_device_label)

        self.mobile_device_options = ["iPhone X", "Samsung Galaxy S10", "iPad Pro", "iPhone 14", "Samsung Galaxy S23"]
        self.mobile_device_radio_buttons = []

        # Adding mobile device radio buttons to their group
        for device in self.mobile_device_options:
            radio_button = QRadioButton(device)
            layout.addWidget(radio_button)
            self.mobile_device_radio_buttons.append(radio_button)
            self.mobile_device_button_group.addButton(radio_button)

        self.orientation_label = QLabel("Select orientation:")
        layout.addWidget(self.orientation_label)

        self.orientation_options = ["Portrait", "Landscape"]
        self.orientation_radio_buttons = []

        for orientation in self.orientation_options:
            radio_button = QRadioButton(orientation)
            layout.addWidget(radio_button)
            self.orientation_radio_buttons.append(radio_button)

        # Adding browser radio buttons to their group
        for browser in self.browser_options:
            radio_button = QRadioButton(browser)
            radio_button.setIcon(QIcon(f"{browser.lower()}.png"))
            layout.addWidget(radio_button)
            self.browser_radio_buttons.append(radio_button)
            self.browser_button_group.addButton(radio_button) 

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
            self.browser_view.setUrl(QUrl(url))
            self.result_label.setText(f"Opened {selected_browser}")
        else:
            self.result_label.setText("Please select a browser.")

        selected_device = None
        for radio_button in self.mobile_device_radio_buttons:
            if radio_button.isChecked():
                selected_device = radio_button.text()
                break

        if selected_device:
            self.emulate_mobile_device(selected_device)

    def open_debugger(self):
        # Launch the debugger when the debugger button is clicked
        code_to_debug = self.url_input.text()  # Use the URL input field for debugging
        debugger = pdb.Pdb()
        debugger.reset()
        debugger.run(code_to_debug)

    def set_browser_size(self):
        try:
            width = int(self.width_input.text())
            height = int(self.height_input.text())
            self.browser_view.setFixedSize(width, height)
        except ValueError:
            self.result_label.setText("Please enter valid width and height values.")

    def emulate_mobile_device(self, device_name):
        device_profiles = {
            # Add real user agents and sizes for each device
            "iPhone X": {"user_agent": "[iPhone X user agent]", "size": QtCore.QSize(375, 812)},
            "iPhone 14": {"user_agent": "[iPhone 14 user agent]", "size": QtCore.QSize(390, 844)},
            "Samsung Galaxy S10": {"user_agent": "[Galaxy S10 user agent]", "size": QtCore.QSize(360, 760)},
            "Samsung Galaxy S23": {"user_agent": "[Galaxy S23 user agent]", "size": QtCore.QSize(384, 854)},
            "iPad Pro": {"user_agent": "[iPad Pro user agent]", "size": QtCore.QSize(1024, 1366)}
        }

        if device_name in device_profiles:
            profile = device_profiles[device_name]
            user_agent = profile["user_agent"]
            screen_size = profile["size"]

            profile = QWebEngineProfile.defaultProfile()
            profile.setHttpUserAgent(user_agent)
            self.browser_view.setFixedSize(screen_size)
        else:
            self.result_label.setText("Selected device not supported.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser_opener = BrowserOpener()
    browser_opener.show()
    sys.exit(app.exec_())

