from PyQt5.QtWidgets import QMainWindow, QInputDialog
from Utilities import chunks


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        """
        Players management:
        :players_list: list of players
        :players: key = name of player; value = number of right answer
        """
        self.players_list = list()
        self.players = dict()

        """
        Question management:
        extract casual questions and then remove from dict
        :questions: key = question; value = answer
        """
        self.questions = dict()

        # start graphical interfaces
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        """
        Create the UI of the main window
        :return: nothing
        """

        def setup_players() -> None:
            """
            Add players and crate his dict
            :return: Nothing
            """

            # add players
            self.popup_add_players()

            # create the dictionary of players
            for player in self.players_list:
                self.players.update({player: 0})

        def setup_questions() -> None:
            # get list of questions
            with open('questions.txt', 'r') as f:
                questions_list = f.readlines()

            # get list of answers
            with open('answers.txt', 'r') as f:
                answers_list = f.readlines()

            # adapted from https://www.kite.com/python/answers/how-to-create-a-dictionary-from-two-lists-in-python
            self.questions = dict(zip(questions_list, answers_list))

        setup_players()
        setup_questions()

        print(self.questions)
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
