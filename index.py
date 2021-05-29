from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
import pandas as pd
import sys
from random import randint


class wordGuess(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.generateRandom()
        self.parseArr()
        self.xp_miktar = 0
        self.count = 2
        self.level_count = 1
        self.qRight = False
        self.end = False
        self.init_ui()


    def settings(self):
        global data
        data = pd.read_json('https://raw.githubusercontent.com/magirtopcu/kelime/master/word.json')
    
    def generateRandom(self):
        global random
        random = randint(1,399)
        return random


    def parseArr(self):
        global meaning
        global newMeaning
        meaning = data['meaning'][random]
        newMeaning = meaning.split()
        print(newMeaning)

    def init_ui(self):
        self.xp = QLabel("XP: ")
        self.xp_str = QLabel(str(self.xp_miktar))
        self.level = QLabel("Level ")
        self.level_str = QLabel(str(self.level_count))
        self.i1 = QLabel("Word: ")
        self.i1.setFont(QFont('Arial', 25))
        self.i1_str = QLabel(data['word'][random])
        self.i1_str.setFont(QFont('Arial', 25))
        self.i1_str.setStyleSheet("color: red;")
        self.inputText = QLineEdit()
        self.triggerBtn = QPushButton("Check Answer")
        self.next = QPushButton("Next Question")
        self.text = QLabel("")
        h_box = QHBoxLayout()
        h_box.addWidget(self.xp)
        h_box.addWidget(self.xp_str)
        h_box.addStretch()
        h_box.addWidget(self.level)
        h_box.addWidget(self.level_str)
        v_box = QVBoxLayout()
        v_box.addWidget(self.i1)
        v_box.addStretch()
        v2_box = QVBoxLayout()
        v2_box.addWidget(self.i1_str)
        v2_box.addStretch()
        h2_box = QHBoxLayout()
        h2_box.addStretch()
        h2_box.addLayout(v_box)
        h2_box.addLayout(v2_box)
        h2_box.addStretch()
        v3_box = QVBoxLayout()
        v3_box.addLayout(h_box)
        v3_box.addStretch()
        v3_box.addLayout(h2_box)
        v3_box.addStretch()
        v3_box.addWidget(self.inputText)
        h3_box = QHBoxLayout()
        h3_box.addWidget(self.triggerBtn)
        h3_box.addWidget(self.next)
        h4_box = QHBoxLayout()
        h4_box.addStretch()
        h4_box.addWidget(self.text)
        h4_box.addStretch()
        v4_box = QVBoxLayout()
        v4_box.addLayout(v3_box)
        v4_box.addLayout(h3_box)
        v4_box.addLayout(h4_box)


        self.setLayout(v4_box)
        self.setWindowTitle("Guess the Word")
        self.setMinimumHeight(350)
        self.setMaximumHeight(350)
        self.setMinimumWidth(450)
        self.setMaximumWidth(450)
        self.triggerBtn.clicked.connect(self.guess)
        self.next.clicked.connect(self.generateRandom)
        self.next.clicked.connect(self.parseArr)
        self.next.clicked.connect(self.guess)
        self.next.clicked.connect(self.next2)
        self.next.setEnabled(False)
        self.show()

    def guess(self):
        userInput = self.inputText.text().lower()
        if userInput == "" or self.qRight == True or self.end == True:
            return False
        if self.text.text() != "":
            self.text.setText("")
        for word in self.inputText.text().lower().split():
            if word in newMeaning:
                self.qRight = True
                self.xp_miktar += 5
                self.xp_str.setText(str(self.xp_miktar))
                self.text.setText("Correct answer! Skip to next question :)")
                self.next.setEnabled(True)
            else:
                self.text.setText("Your answer is incorrect, try again :( ")
                QMessageBox.about(self, "Notice!", "If your answer is correct and the system doesn't accept it, try adding a comma at the end of your answer.")
                return False

    def next2(self):
        if self.qRight == False or self.end == True:
            return False
        self.inputText.clear()
        self.i1_str.setText(data['word'][random])
        self.level_count += 1
        self.level_str.setText(str(self.level_count))
        self.qRight = False
        self.next.setEnabled(False)

        if self.text.text() != "":
            self.text.setText("")
app = QApplication(sys.argv)
menu = wordGuess()
sys.exit(app.exec_())
