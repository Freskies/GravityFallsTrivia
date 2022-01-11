from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QWidget, QGroupBox, QLabel, QFrame, QPushButton
from Utilities import chunks
import random

"""
Project improvements
    check if there aren't any more questions
"""


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # The number of right answer needed to win
        self.VICTORY_POINTS = 3

        """
        Players management:
        :players_list: list of players
        :players: key = name of player; value = number of right answer
        :turn: the number of the turn played (1 turn = 1 turn per player)
        """
        self.players_list = list()
        self.players = dict()
        self.turn = 0
        self.setup_players()

        """
        Question management:
        extract casual questions and then remove from dict
        :questions: key = question; value = answer
        """
        self.questions = dict()
        self.setup_questions()

        # start graphical interfaces
        self.TITLE_FONT = {
            "name": "Franklin Gothic Medium",
            "size": 22
        }
        self.MINOR_TEXT_FONT = {
            "name": "Franklin Gothic Book",
            "size": 14
        }
        self.init_ui()
        self.show()

    def popup_add_players(self) -> None:
        """
        Create a popup that will appear before the game starts
        With this popup you will be able to add players to the game
        :return: nothing
        """

        def get_others_players() -> str:
            """ :return: formatted string of all name of players """

            rows = chunks(self.players_list, 5)
            return 'Players:\n' + '\n'.join([', '.join(row) for row in rows])

        players_popup = QInputDialog(self)
        players_popup.setInputMode(QInputDialog.TextInput)
        players_popup.setWindowTitle("Add new player")
        players_popup.setLabelText(f"{get_others_players()}\n\nEnter the player name")
        players_popup.resize(300, 100)
        players_popup.exec_()
        player_name = players_popup.textValue()

        if player_name:
            if player_name not in self.players_list:
                self.players_list.append(player_name)
            self.popup_add_players()

        elif len(self.players_list) < 1:
            self.popup_add_players()

        else:
            pass

    def setup_players(self) -> None:
        """
        Add players and crate his dict
        :return: Nothing
        """

        # add players
        self.popup_add_players()

        # create the dictionary of players
        for player in self.players_list:
            self.players.update({player: 0})

    def setup_questions(self) -> None:
        # get list of questions
        with open('questions.txt', 'r') as f:
            questions_list = f.readlines()

        # get list of answers
        with open('answers.txt', 'r') as f:
            answers_list = f.readlines()

        # adapted from https://www.kite.com/python/answers/how-to-create-a-dictionary-from-two-lists-in-python
        self.questions = dict(zip(questions_list, answers_list))

    def init_ui(self) -> None:
        """
        Create the UI of the main window
        :return: nothing
        """

        def get_title_font() -> QFont:
            title_font = QFont()
            title_font.setFamily(self.TITLE_FONT["name"])
            title_font.setPointSize(self.TITLE_FONT["size"])
            return title_font

        def get_minor_font() -> QFont:
            minor_font = QFont()
            minor_font.setFamily(self.MINOR_TEXT_FONT["name"])
            minor_font.setPointSize(self.MINOR_TEXT_FONT["size"])
            return minor_font

        self.setObjectName("MainWindow")
        self.setWindowTitle("Gravity Falls Trivia Master")
        self.setFixedSize(800, 540)

        central_widget = QWidget(self)
        central_widget.setObjectName("central_widget")

        # vertical line
        vertical_line = QFrame(central_widget)
        vertical_line.setGeometry(QRect(130, -20, 41, 611))
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        vertical_line.setObjectName("vertical_line")

        # Question Box
        question_box = QGroupBox(central_widget)
        question_box.setGeometry(QRect(190, 30, 571, 161))
        question_box.setFont(get_title_font())
        question_box.setObjectName("question_box")

        question_label = QLabel(question_box)
        question_label.setGeometry(QRect(34, 45, 511, 91))
        question_label.setFont(get_minor_font())
        question_label.setObjectName("question_label")

        # Answer Box
        answer_box = QGroupBox(central_widget)
        answer_box.setGeometry(QRect(190, 220, 571, 161))
        answer_box.setFont(get_title_font())
        answer_box.setObjectName("answer_box")

        answer_label = QLabel(answer_box)
        answer_label.setGeometry(QRect(34, 45, 511, 91))
        answer_label.setFont(get_minor_font())
        answer_label.setObjectName("answer_label")

        # YES and NO Buttons
        yes_button = QPushButton(central_widget)
        yes_button.setGeometry(QRect(340, 420, 93, 81))
        yes_button.setObjectName("yes_button")

        no_button = QPushButton(central_widget)
        no_button.setGeometry(QRect(520, 420, 93, 81))
        no_button.setObjectName("no_button")

        # translate ui
        _translate = QCoreApplication.translate
        question_box.setTitle(_translate("MainWindow", "DOMANDA"))
        answer_box.setTitle(_translate("MainWindow", "RISPOSTA"))
        no_button.setText(_translate("MainWindow", "X"))
        yes_button.setText(_translate("MainWindow", "V"))

        # set everything
        self.setCentralWidget(central_widget)
        QMetaObject.connectSlotsByName(self)


# question_key = random.choice(list(self.questions))
# del self.questions[question_key]
# right answer? si: self.players[player] += 1
"""
if self.players[player] == self.VICTORY_POINTS:
    running = False
    break
"""