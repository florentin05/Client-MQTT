from PyQt5.QtGui import QFont, QIcon, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QLineEdit, \
    QTextEdit, QComboBox, QGridLayout
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys

import Packets
import datetime


class PublishWindow(QWidget):
    def __init__(self, Client):
        super().__init__()

        self.Client = Client
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

        # ----PUBLISH BUTTON---- #
        self.publishButton = QPushButton("PUBLISH", self)
        self.publishButton.move(200, 310)
        self.publishButton.resize(100, 40)
        self.publishButton.setStyleSheet("background-color: #ECD137;")
        # self.publishButton.clicked.connect(self.publish_func)

        # ----PUBLISH BUTTON---- #
        self.publishButton = QPushButton("PUBLISH", self)
        self.publishButton.move(200, 310)
        self.publishButton.resize(100, 40)
        self.publishButton.setStyleSheet("background-color: #ECD137;")
        self.publishButton.clicked.connect(self.publish_func)

    def set_QoS(self):
        self.QoS = self.QoS_box.currentText()  # QoS value

    def publish_func(self):
        TopicName = self.topic.text()
        Message = self.message.toPlainText()
        qos = int(self.QoS_box.currentText())
        dupFlag = 0
        retain = 0
        Packets.PUBLISHButton(self.Client, TopicName, Message, dupFlag, qos, retain)


class SuccessWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Successful connection")
        self.setGeometry(100, 100, 500, 300)

        self.font = QtGui.QFont()
        self.font.setBold(True)

        self.text = QLabel(self)
        self.text.setText("Conectare REUSITA !")
        self.text.setStyleSheet("font-size: 14pt;")
        self.text.setFont(self.font)
        self.text.setStyleSheet("background-color: #54A227;")
        self.text.move(50, 50)
        self.text.resize(350, 30)


class SubscribeWindow(QWidget):
    def __init__(self, Client):
        super().__init__()

        self.Client = Client
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

        # ----SUBSCRIBE BUTTON---- #
        self.subscribeButton = QPushButton("SUBSCRIBE", self)
        self.subscribeButton.move(200, 220)
        self.subscribeButton.resize(100, 40)
        self.subscribeButton.setStyleSheet("background-color: #4982F6;")
        # self.publishButton.clicked.connect(self.subscribe_func)

        # ----SUBSCRIBE BUTTON---- #
        self.subscribeButton = QPushButton("SUBSCRIBE", self)
        self.subscribeButton.move(200, 220)
        self.subscribeButton.resize(100, 40)
        self.subscribeButton.setStyleSheet("background-color: #4982F6;")
        self.subscribeButton.clicked.connect(self.subscribe_func)

    def set_QoS(self):
        self.QoS = self.QoS_box.currentText()  # QoS value

    def subscribe_func(self):
        topic = self.topic.text()
        qos = int(self.QoS_box.currentText())
        self.Client.CurrentTopic = topic
        self.Client.socket.send(Packets.Subscribe(topic, qos).pack())


class MessagesWindow(QWidget):
    def __init__(self, Client):
        super().__init__()

        self.setGeometry(150, 150, 400, 400)
        self.Client = Client
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
        # self.messages.append('hey1')

        # ----DISCONNECT BUTTON---- #
        self.disconnectButton = QPushButton("DISCONNECT", self)
        self.disconnectButton.move(80, 700)
        self.disconnectButton.resize(100, 60)
        self.disconnectButton.setStyleSheet("background-color: #F73D3A;")
        self.disconnectButton.clicked.connect(self.disconnect_func)

        # ----UNSUBSCRIBE BUTTON---- #
        self.unsubscribeButton = QPushButton("UNSUBSCRIBE", self)
        self.unsubscribeButton.move(600, 700)
        self.unsubscribeButton.resize(100, 40)
        self.unsubscribeButton.setStyleSheet("background-color: #FCC5CD;")
        self.unsubscribeButton.clicked.connect(self.unsubscribe_func)

        # ----UNSUBSCRIBE COMBOBOX--- #
        self.unsubscribe_message = QLabel(self)
        self.unsubscribe_message.setText("Alegeti topicul de la care vreti sa va dezabonati : ")
        self.unsubscribe_message.move(450, 600)
        self.unsubscribe_message.resize(350, 30)
        self.unsubscribe_message.setFont(self.font)
        self.unsubscribe_combobox = QComboBox(self)
        self.unsubscribe_topic = self.unsubscribe_combobox.currentText()
        # self.unsubscribe_combobox.activated.connect(self.set_unsubscribe_topic)
        self.unsubscribe_combobox.move(550, 650)
        self.unsubscribe_combobox.resize(200, 25)

    def disconnect_func(self):
        self.Client.socket.send(Packets.Disconnect().pack())
        self.Client.window.mainWindow.MessageWindow.close()
        self.Client.window.mainWindow.PublishWindow.close()
        self.Client.window.mainWindow.SubscribeWindow.close()
        self.Client.window.mainWindow.close()

    def unsubscribe_func(self):
        topic = self.unsubscribe_combobox.currentText()
        self.Client.socket.send(Packets.Unsubscribe(topic).pack())


class MainWindow(QWidget):
    def __init__(self, Client):
        super().__init__()

        self.Client = Client
        self.setWindowTitle("Main page")
        self.setGeometry(100, 100, 1400, 800)

        self.font = QtGui.QFont()
        self.font.setBold(True)

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.MessageWindow = MessagesWindow(Client)
        self.PublishWindow = PublishWindow(Client)
        self.SubscribeWindow = SubscribeWindow(Client)
        self.layout.addWidget(self.PublishWindow, 0, 0, 1, 1)
        self.layout.addWidget(self.SubscribeWindow, 1, 0, 1, 1)
        self.layout.addWidget(self.MessageWindow, 0, 1, 0, 2)


class ConnectWindow(QWidget):

    def __init__(self, Client):
        super().__init__()

        self.Client = Client

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
        self.client_ID_check.move(100, 120)
        self.client_ID_check.resize(100, 40)
        self.client_ID_check.setText("Client ID :")
        self.client_ID_check.setStyleSheet("font-size: 10pt;")
        self.client_ID_check.stateChanged.connect(self.clientIDCheckStateChanged)
        self.client_ID = QLineEdit(self)
        self.client_ID.move(210, 128)
        self.client_ID.resize(200, 25)
        self.client_ID.setDisabled(True)

        # ---- USERNAME & PASSWORD---- #
        self.username_password_check = QCheckBox(self)
        self.username_password_check.move(100, 200)
        self.username_password_check.resize(100, 40)
        self.username_password_check.stateChanged.connect(self.usernamePasswordCheckStateChanged)

        self.username_text = QLabel(self)
        self.username_text.setText("Username :")
        self.username_text.move(130, 185)
        self.username_text.resize(100, 30)
        self.username_text.setStyleSheet("font-size: 10pt;")
        self.username = QLineEdit(self)
        self.username.move(225, 190)
        self.username.resize(200, 25)
        self.username.setDisabled(True)

        self.password_text = QLabel(self)
        self.password_text.setText("Password :")
        self.password_text.move(130, 225)
        self.password_text.resize(100, 30)
        self.password_text.setStyleSheet("font-size: 10pt;")
        self.password = QLineEdit(self)
        self.password.move(225, 230)
        self.password.resize(200, 25)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setDisabled(True)

        # ----SHOW/HIDE BUTTON---- #
        self.eye_button = QPushButton("", self)
        self.eye_button.move(435, 230)
        self.eye_button.resize(35, 25)
        self.eye_button.setIcon(QIcon('images/show_icon.png'))
        self.eye_button.clicked.connect(self.eye_button_func)

        # ----KeepAlive--- #
        self.keepAlive_check = QCheckBox(self)
        self.keepAlive_check.move(100, 280)
        self.keepAlive_check.resize(110, 40)
        self.keepAlive_check.setText("KeepAlive :")
        self.keepAlive_check.setStyleSheet("font-size: 10pt;")
        self.keepAlive_check.stateChanged.connect(self.keepAliveCheckStateChanged)
        self.keepAlive = QLineEdit(self)
        self.keepAlive.move(220, 290)
        self.keepAlive.resize(200, 25)
        self.keepAlive.setDisabled(True)

        # ----CleanStart---- #
        self.cleanStart_check = QCheckBox(self)
        self.cleanStart_check.move(100, 340)
        self.cleanStart_check.resize(110, 40)
        self.cleanStart_check.setText("CleanStart :")
        self.cleanStart_check.setStyleSheet("font-size: 10pt;")
        self.cleanStart_check.stateChanged.connect(self.cleanStartCheckStateChanged)
        self.cleanStart_box = QComboBox(self)
        self.cleanStart_box.addItems(["0", "1"])
        self.cleanStart = self.cleanStart_box.currentText()
        self.cleanStart_box.activated.connect(self.set_cleanStart)
        self.cleanStart_box.move(220, 350)
        self.cleanStart_box.resize(200, 25)
        self.cleanStart_box.setDisabled(True)

        # ----LastWill & QoS---- #
        self.last_will_topic_check = QCheckBox(self)
        self.last_will_topic_check.move(100, 400)
        self.last_will_topic_check.resize(130, 40)
        self.last_will_topic_check.setText("LastWill topic:")
        self.last_will_topic_check.setStyleSheet("font-size: 10pt;")
        self.last_will_topic_check.stateChanged.connect(self.lastWillCheckStateChanged)
        self.last_will_topic = QLineEdit(self)
        self.last_will_topic.move(260, 410)
        self.last_will_topic.resize(200, 25)
        self.last_will_topic.setDisabled(True)

        self.last_will_message_check = QLabel(self)
        self.last_will_message_check.move(120, 430)
        self.last_will_message_check.resize(140, 40)
        self.last_will_message_check.setText("LastWill message:")
        self.last_will_message_check.setStyleSheet("font-size: 10pt;")
        self.last_will_message = QLineEdit(self)
        self.last_will_message.move(260, 440)
        self.last_will_message.resize(200, 25)
        self.last_will_message.setDisabled(True)

        self.QoS_check = QLabel(self)
        self.QoS_check.move(470, 400)
        self.QoS_check.resize(110, 40)
        self.QoS_check.setText("QoS :")
        self.QoS_check.setStyleSheet("font-size: 10pt;")
        self.QoS_box = QComboBox(self)
        self.QoS_box.addItems(["0", "1", "2"])
        self.QoS = self.QoS_box.currentText()
        self.QoS_box.activated.connect(self.set_QoS)
        self.QoS_box.move(530, 410)
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
        if self.last_will_topic_check.isChecked() == True:
            self.last_will_topic.setEnabled(True)
            self.last_will_message.setEnabled(True)
            self.QoS_box.setEnabled(True)
            self.lastWill_check_enabled = True
        else:
            self.last_will_topic.setDisabled(True)
            self.last_will_message.setDisabled(True)
            self.lastWill_check_enabled = False
            self.QoS_box.setDisabled(True)

    def connect_func(self):
        # id, usernameFlag, username, passwordFlag, password, keepAlive, lastWillFlag, lastWillMessage, lastWillQOS, lastWillTopic, CleanStart
        if self.username_password_check.isChecked() == True:
            usernameFlag = 1
            self.Client.username = self.username.text()
            self.Client.password = self.password.text()
            passwordFlag = 1
        else:
            usernameFlag = 0
            passwordFlag = 0
        if self.keepAlive_check.isChecked() == True:
            self.Client.KeepAlive = int(self.keepAlive.text())
        else:
            self.Client.KeepAlive = 0
        if self.last_will_topic_check.isChecked() == True:
            self.Client.lastWillFlag = 1
            self.Client.lastWillMessage = self.last_will_message.text()
            self.Client.lastWillQOS = int(self.QoS_box.currentText())
            self.Client.lastWillTopic = self.last_will_topic.text()
        else:
            self.Client.lastWillFlag = 0
            self.Client.LastWillMessage = ""
            self.Client.lastWillQOS = 0
            self.Client.lastWillTopic = ""
        if (self.cleanStart_check.isChecked() == True):
            self.Client.cleanStart = 1
        else:
            self.Client.CleanStart = 0
        if (self.client_ID_check.isChecked() == True):
            self.Client.id = self.client_ID.text()
        else:
            self.Client.id = ""
        self.Client.socket.send(
            Packets.Connect(self.Client.id, usernameFlag, self.Client.username, passwordFlag, self.Client.password,
                            self.Client.KeepAlive, self.Client.lastWillFlag, self.Client.lastWillMessage,
                            self.Client.lastWillQOS, self.Client.lastWillTopic, self.Client.CleanStart).pack())
        self.Client.LastMessageSent = datetime.datetime.now()
        self.mainWindow = MainWindow(self.Client)
        self.close()
        # time.sleep(2)
        self.mainWindow.show()


class SuccessWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Successful connection")
        self.setGeometry(100, 100, 500, 300)

        self.font = QtGui.QFont()
        self.font.setBold(True)

        self.text = QLabel(self)
        self.text.setText("Conectare REUSITA !")
        self.text.setStyleSheet("font-size: 14pt;")
        self.text.setFont(self.font)
        self.text.setStyleSheet("background-color: #54A227;")
        self.text.move(50, 50)
        self.text.resize(350, 30)
