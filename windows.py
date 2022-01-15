from PyQt5.QtGui import QFont, QIcon, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QLineEdit, \
    QTextEdit, QComboBox, QGridLayout
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys


class PublishWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 400, 400)

        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setUnderline(True)

        self.title = QLabel(self)
        self.title.setText("PUBLISH")
        self.title.setFont(self.font)
        self.title.setStyleSheet("font-size: 20px;")
        self.title.move(150, 10)

        self.topic_label = QLabel(self)
        self.topic_label.setText("Introduceti topicul dorit :")
        self.topic_label.move(30, 60)
        self.topic_label.resize(190, 30)
        self.topic_label.setStyleSheet("font-size: 10pt;")
        self.topic = QLineEdit(self)
        self.topic.move(210, 65)
        self.topic.resize(200, 25)

        self.message_label = QLabel(self)
        self.message_label.setText("Introduceti mesajul :")
        self.message_label.move(30, 130)
        self.message_label.resize(190, 30)
        self.message_label.setStyleSheet("font-size: 10pt;")
        self.message = QTextEdit(self)
        self.message.move(200, 135)
        self.message.resize(250, 100)

        self.QoS_title = QLabel(self)
        self.QoS_title.move(30, 250)
        self.QoS_title.resize(110, 40)
        self.QoS_title.setText("QoS :")
        self.QoS_title.setStyleSheet("font-size: 10pt;")
        self.QoS_box = QComboBox(self)
        self.QoS_box.addItems(["0", "1", "2"])
        self.QoS = self.QoS_box.currentText()
        self.QoS_box.activated.connect(self.set_QoS)
        self.QoS_box.move(75, 258)
        self.QoS_box.resize(150, 25)

    def set_QoS(self):
        self.QoS = self.QoS_box.currentText()  # QoS value


class SubscribeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 400, 400)

        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setUnderline(True)

        self.title = QLabel(self)
        self.title.setText("SUBSCRIBE")
        self.title.setFont(self.font)
        self.title.setStyleSheet("font-size: 20px;")
        self.title.move(150, 20)

        self.topic_label = QLabel(self)
        self.topic_label.setText("Introduceti topicul dorit :")
        self.topic_label.move(30, 70)
        self.topic_label.resize(190, 30)
        self.topic_label.setStyleSheet("font-size: 10pt;")
        self.topic = QLineEdit(self)
        self.topic.move(230, 75)
        self.topic.resize(200, 25)

        self.QoS_title = QLabel(self)
        self.QoS_title.move(30, 140)
        self.QoS_title.resize(110, 40)
        self.QoS_title.setText("QoS :")
        self.QoS_title.setStyleSheet("font-size: 10pt;")
        self.QoS_box = QComboBox(self)
        self.QoS_box.addItems(["0", "1", "2"])
        self.QoS = self.QoS_box.currentText()
        self.QoS_box.activated.connect(self.set_QoS)
        self.QoS_box.move(80, 150)
        self.QoS_box.resize(150, 25)

    def set_QoS(self):
        self.QoS = self.QoS_box.currentText()  # QoS value


class MessagesWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(150, 150, 400, 400)

        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setUnderline(True)

        self.title = QLabel(self)
        self.title.setText("Received messages : ")
        self.title.setFont(self.font)
        self.title.setStyleSheet("font-size: 20px;")
        self.title.move(200, 20)

        self.messages = QTextEdit(self)
        self.messages.move(190, 100)
        self.messages.resize(550, 450)
        self.messages.append('hey1')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main page")
        self.setGeometry(100, 100, 1400, 800)

        self.font = QtGui.QFont()
        self.font.setBold(True)

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(PublishWindow(), 0, 0, 1, 1)
        self.layout.addWidget(SubscribeWindow(), 1, 0, 1, 1)
        self.layout.addWidget(MessagesWindow(), 0, 1, 0, 2)


class ConnectWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connect page")
        self.setGeometry(100, 100, 900, 600)

        self.font = QtGui.QFont()
        self.font.setBold(True)

        self.text = QLabel(self)
        self.text.setText("Introduceti datele de conectare : ")
        self.text.setStyleSheet("font-size: 12pt;")
        self.text.setFont(self.font)
        self.text.move(50, 50)
        self.text.resize(350, 30)

        # ----CLIENT ID---- #
        self.client_ID_check = QCheckBox(self)
        self.client_ID_check.move(100, 150)
        self.client_ID_check.resize(100, 40)
        self.client_ID_check.setText("Client ID :")
        self.client_ID_check.setStyleSheet("font-size: 10pt;")
        self.client_ID_check.stateChanged.connect(self.clientIDCheckStateChanged)
        self.client_ID = QLineEdit(self)
        self.client_ID.move(210, 158)
        self.client_ID.resize(200, 25)
        self.client_ID.setDisabled(True)

        # ---- USERNAME & PASSWORD---- #
        self.username_password_check = QCheckBox(self)
        self.username_password_check.move(100, 230)
        self.username_password_check.resize(100, 40)
        self.username_password_check.stateChanged.connect(self.usernamePasswordCheckStateChanged)

        self.username_text = QLabel(self)
        self.username_text.setText("Username :")
        self.username_text.move(130, 215)
        self.username_text.resize(100, 30)
        self.username_text.setStyleSheet("font-size: 10pt;")
        self.username = QLineEdit(self)
        self.username.move(225, 220)
        self.username.resize(200, 25)
        self.username.setDisabled(True)

        self.password_text = QLabel(self)
        self.password_text.setText("Password :")
        self.password_text.move(130, 255)
        self.password_text.resize(100, 30)
        self.password_text.setStyleSheet("font-size: 10pt;")
        self.password = QLineEdit(self)
        self.password.move(225, 260)
        self.password.resize(200, 25)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setDisabled(True)

        # ----SHOW/HIDE BUTTON---- #
        self.eye_button = QPushButton("", self)
        self.eye_button.move(435, 260)
        self.eye_button.resize(35, 25)
        self.eye_button.setIcon(QIcon('images/show_icon.png'))
        self.eye_button.clicked.connect(self.eye_button_func)

        # ----KeepAlive--- #
        self.keepAlive_check = QCheckBox(self)
        self.keepAlive_check.move(100, 310)
        self.keepAlive_check.resize(110, 40)
        self.keepAlive_check.setText("KeepAlive :")
        self.keepAlive_check.setStyleSheet("font-size: 10pt;")
        self.keepAlive_check.stateChanged.connect(self.keepAliveCheckStateChanged)
        self.keepAlive = QLineEdit(self)
        self.keepAlive.move(220, 320)
        self.keepAlive.resize(200, 25)
        self.keepAlive.setDisabled(True)

        # ----CleanStart---- #
        self.cleanStart_check = QCheckBox(self)
        self.cleanStart_check.move(100, 370)
        self.cleanStart_check.resize(110, 40)
        self.cleanStart_check.setText("CleanStart :")
        self.cleanStart_check.setStyleSheet("font-size: 10pt;")
        self.cleanStart_check.stateChanged.connect(self.cleanStartCheckStateChanged)
        self.cleanStart_box = QComboBox(self)
        self.cleanStart_box.addItems(["0", "1"])
        self.cleanStart = self.cleanStart_box.currentText()
        self.cleanStart_box.activated.connect(self.set_cleanStart)
        self.cleanStart_box.move(220, 380)
        self.cleanStart_box.resize(200, 25)
        self.cleanStart_box.setDisabled(True)

        # ----LastWill & QoS---- #
        self.lastWill_check = QCheckBox(self)
        self.lastWill_check.move(100, 430)
        self.lastWill_check.resize(110, 40)
        self.lastWill_check.setText("LastWill :")
        self.lastWill_check.setStyleSheet("font-size: 10pt;")
        self.lastWill_check.stateChanged.connect(self.lastWillCheckStateChanged)
        self.lastWill = QLineEdit(self)
        self.lastWill.move(220, 440)
        self.lastWill.resize(200, 25)
        self.lastWill.setDisabled(True)

        self.QoS_check = QLabel(self)
        self.QoS_check.move(450, 430)
        self.QoS_check.resize(110, 40)
        self.QoS_check.setText("QoS :")
        self.QoS_check.setStyleSheet("font-size: 10pt;")
        self.QoS_box = QComboBox(self)
        self.QoS_box.addItems(["0", "1", "2"])
        self.QoS = self.QoS_box.currentText()
        self.QoS_box.activated.connect(self.set_QoS)
        self.QoS_box.move(510, 440)
        self.QoS_box.resize(200, 25)
        self.QoS_box.setDisabled(True)

        # ----CONNECT BUTTON---- #
        self.connectButton = QPushButton("CONNECT", self)
        self.connectButton.move(350, 520)
        self.connectButton.resize(100, 40)
        self.connectButton.setStyleSheet("background-color: #78BC70;")
        self.connectButton.clicked.connect(self.connect_func)

    def set_QoS(self):
        self.QoS = self.QoS_box.currentText()  # QoS value

    def set_cleanStart(self):
        self.cleanStart = self.cleanStart_box.currentText()  # clean start value

    def eye_button_func(self):
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.eye_button.setIcon(QIcon('images/hide_icon.png'))
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.eye_button.setIcon(QIcon('images/show_icon.png'))

    def clientIDCheckStateChanged(self):
        if self.client_ID_check.isChecked() == True:
            self.client_ID.setEnabled(True)
            self.client_ID_check_enabled = True
        else:
            self.client_ID.setDisabled(True)
            self.client_ID_check_enabled = False

    def usernamePasswordCheckStateChanged(self):
        if self.username_password_check.isChecked() == True:
            self.username.setEnabled(True)
            self.password.setEnabled(True)
            self.username_password_check_enabled = True
        else:
            self.username.setDisabled(True)
            self.password.setDisabled(True)
            self.username_password_check_enabled = False

    def keepAliveCheckStateChanged(self):
        if self.keepAlive_check.isChecked() == True:
            self.keepAlive.setEnabled(True)
            self.keepAlive_check_enabled = True
        else:
            self.keepAlive.setDisabled(True)
            self.keepAlive_check_enabled = False

    def cleanStartCheckStateChanged(self):
        if self.cleanStart_check.isChecked() == True:
            self.cleanStart_box.setEnabled(True)
            self.cleanStart_check_enabled = True
        else:
            self.cleanStart_box.setDisabled(True)
            self.cleanStart_check_enabled = False

    def lastWillCheckStateChanged(self):
        if self.lastWill_check.isChecked() == True:
            self.lastWill.setEnabled(True)
            self.QoS_box.setEnabled(True)
            self.lastWill_check_enabled = True
        else:
            self.lastWill.setDisabled(True)
            self.lastWill_check_enabled = False
            self.QoS_box.setDisabled(True)

    def connect_func(self):
        self.mainWindow = MainWindow()
        self.close()
        self.mainWindow.show()
