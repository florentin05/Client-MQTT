import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


class ConnectForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Title")
        self.resize(500, 120)

        # Create a form layout
        formlayout = QGridLayout()

        formlayout.setVerticalSpacing(30)

        label_username = QLabel('<font size="4"> Username: </font>')
        self.username_line = QLineEdit()
        self.username_line.setPlaceholderText('Enter your username')
        formlayout.addWidget(label_username, 0, 0)
        formlayout.addWidget(self.username_line, 0, 1)
        self.username_value = self.username_line.text()

        label_password = QLabel('<font size="4"> Password: </font>')
        self.password_line = QLineEdit()
        self.password_line.setEchoMode(QLineEdit.Password)
        self.password_line.setPlaceholderText('Enter your password')
        formlayout.addWidget(label_password, 1, 0)
        formlayout.addWidget(self.password_line, 1, 1)
        self.password_value = self.password_line.text()

        # Add connect button
        self.connect_button = QPushButton('Connect')
        formlayout.addWidget(self.connect_button,2,0)

        self.setLayout(formlayout)
