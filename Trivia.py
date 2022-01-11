from PyQt5.QtWidgets import QMainWindow, QInputDialog
from Utilities import chunks
import random


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
        self.init_ui()
        self.show()

        self.game_loop()

    def init_ui(self) -> None:
        """
        Create the UI of the main window
        :return: nothing
        """

        self.setObjectName("MainWindow")
        self.setFixedSize(620, 558)

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

    # TODO documentation
    def game_loop(self) -> None:
        print(self.questions)
        running = True

        while running:
            # next turn
            self.turn += 1

            # do a turn for every player
            for player in self.players:
                # extract casual question
                question_key = random.choice(list(self.questions))

                # TODO fai vedere la risposta

                # capisci se ha indovinato o no
                if input("indovianto: ") == "si":
                    self.players[player] += 1

                # TODO elimina la domanda
                print(self.players)

                # TODO controlla se ha vinto
                if self.players[player] == self.VICTORY_POINTS:
                    running = False
                    break
