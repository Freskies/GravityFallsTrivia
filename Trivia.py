from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QWidget, QGroupBox, QLabel, QFrame, QPushButton

from QLabelClickable import QLabelClickable
from Utilities import chunks
import random


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # if anyone wins running = false
        self.running = True

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
        self.WINDOW_SIZE = {
            "x": 800,
            "y": 540
        }
        self.players_labels = list()
        self.PLAYER_SPACE = 151
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
        players_popup.setWindowIcon(QIcon("incon_gft.png"))
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
        """
        create a dictionary that have questions and answers linked
        Note: the file must be encoded in ANSI
        :return:
        """

        # get list of questions
        with open('questions.txt', 'r') as f:
            questions_list = f.readlines()

        # get list of answers
        with open('answers.txt', 'r') as f:
            answers_list = f.readlines()

        for question, answer in zip(questions_list, answers_list):
            self.questions[question[:-1]] = answer[:-1]

    def init_ui(self) -> None:
        """
        Create the UI of the main window
        :return: nothing
        """

        def get_title_font() -> QFont:
            """
            :return: font of the most important parts
            """
            title_font = QFont()
            title_font.setFamily(self.TITLE_FONT["name"])
            title_font.setPointSize(self.TITLE_FONT["size"])
            return title_font

        def get_minor_font() -> QFont:
            """
            :return: font of the minor important parts
            """
            minor_font = QFont()
            minor_font.setFamily(self.MINOR_TEXT_FONT["name"])
            minor_font.setPointSize(self.MINOR_TEXT_FONT["size"])
            return minor_font

        def button_function(right_answer) -> None:
            """
            the function that will be called from the 2 buttons (right and wrong)
            :param right_answer: True if right and False if wrong
            :return: Nothing
            """
            self.change_turn(question_label, answer_label, right_answer = right_answer)

        # set main window
        self.setObjectName("MainWindow")
        self.setWindowTitle("Gravity Falls Trivia Master")
        self.setFixedSize(self.WINDOW_SIZE["x"], self.WINDOW_SIZE["y"])
        self.setWindowIcon(QIcon("incon_gft.png"))

        # create a central widget that is the father of everything
        central_widget = QWidget(self)
        central_widget.setObjectName("central_widget")

        # Question Box
        question_box = QGroupBox(central_widget)
        question_box.setGeometry(QRect(190, 30, 571, 161))
        question_box.setFont(get_title_font())
        question_box.setObjectName("question_box")

        question_label = QLabel(question_box)
        question_label.setGeometry(QRect(34, 45, 511, 91))
        question_label.setFont(get_minor_font())
        question_label.setWordWrap(True)
        question_label.setObjectName("question_label")

        # Answer Box
        answer_box = QGroupBox(central_widget)
        answer_box.setGeometry(QRect(190, 220, 571, 161))
        answer_box.setFont(get_title_font())
        answer_box.setObjectName("answer_box")

        answer_label = QLabelClickable(answer_box)
        answer_label.setGeometry(QRect(34, 45, 511, 91))
        answer_label.setFont(get_minor_font())
        answer_label.setWordWrap(True)
        answer_label.setObjectName("answer_label")

        # Right and wrong answer buttons
        yes_button = QPushButton(central_widget)
        yes_button.setGeometry(QRect(340, 420, 93, 81))
        yes_button.setObjectName("yes_button")

        no_button = QPushButton(central_widget)
        no_button.setGeometry(QRect(520, 420, 93, 81))
        no_button.setObjectName("no_button")

        # Players Frame and relatives label
        player_frame = QFrame(central_widget)
        player_frame.setGeometry(QRect(0, 0, self.PLAYER_SPACE, self.WINDOW_SIZE["y"]))
        player_frame.setFont(get_title_font())
        player_frame.setStyleSheet("border: 1px solid black;")
        player_frame.setFrameShape(QFrame.StyledPanel)
        player_frame.setFrameShadow(QFrame.Raised)
        player_frame.setObjectName("player_frame")

        players_label_height = self.WINDOW_SIZE["y"] // len(self.players_list)

        for player in self.players_list:
            player_label = QLabel(player_frame)
            player_label.setGeometry(
                QRect(0, players_label_height * self.players_list.index(player), 151, players_label_height))
            player_label.setFont(get_minor_font())
            player_label.setObjectName("answer_label")
            self.players_labels.append(player_label)

        # translate ui
        _translate = QCoreApplication.translate
        question_box.setTitle(_translate("MainWindow", "DOMANDA"))
        answer_box.setTitle(_translate("MainWindow", "RISPOSTA"))
        no_button.setText(_translate("MainWindow", "X"))
        yes_button.setText(_translate("MainWindow", "V"))

        # set everything
        self.setCentralWidget(central_widget)
        QMetaObject.connectSlotsByName(self)

        # connect functions
        answer_label.clicked.connect(lambda: self.show_answer(answer_label, question_label))
        yes_button.clicked.connect(lambda: button_function(True))
        no_button.clicked.connect(lambda: button_function(False))

        self.setup_game(question_label)

    def setup_game(self, question_label: QLabel) -> None:
        """
        extract the first question and set up the players labels
        :param question_label: the label of the questions
        :return: Nothing
        """

        question_label.setText(random.choice(list(self.questions)))
        self.refresh_labels_players()

    def show_answer(self, answer_label: QLabel, question_label: QLabel) -> None:
        """
        Show answer in the answer label when it's clicked
        :param answer_label: the label of the answer
        :param question_label: the label of the question
        :return: Nothing
        """

        answer_label.setText(self.questions[question_label.text()] if self.running else "Congratulations!")

    def change_turn(self, question_label, answer_label, right_answer = False) -> None:

        def add_point() -> None:
            """
            add a point (if the player said a right answer)
            check if with this point the player won
            :return: Nothing
            """

            self.players[player_name] += 1

            if self.players[player_name] == self.VICTORY_POINTS:
                # because +=1 after this func
                self.turn -= 1
                self.running = False

        # name of the player on this turn
        player_name = self.players_list[self.turn]

        # remove this question from the question dict
        del self.questions[question_label.text()]

        # clear labels
        question_label.setText("")
        answer_label.setText("")

        # add point (and win check) if the player said the right answer
        if right_answer:
            add_point()

        # change turn
        self.turn += 1
        if self.turn == len(self.players_list):
            self.turn = 0

        self.refresh_labels_players()

        # extract casual question and print it / if anyone won print congratulations
        question_label.setText(
            random.choice(list(self.questions)) if self.running else f"The winner is {player_name}")

    def refresh_labels_players(self) -> None:
        for player, label in zip(self.players_list, self.players_labels):
            label.setText(f"{player} {self.players[player]}")
            label.setStyleSheet("")

        self.players_labels[self.turn].setStyleSheet(
            "background-color: " + ("#bbff99" if self.running else "#ffff99"))
