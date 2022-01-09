from PyQt5.QtWidgets import QMainWindow, QInputDialog
from Utilities import chunks


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.players_list = list()

        # add players
        self.show_popup()

        # start graphical interfaces
        self.init_ui()
        self.show()

    def init_ui(self) -> None:
        """
        Create the UI of the main window
        :return: nothing
        """
        print(self.players_list)
        self.setObjectName("MainWindow")
        self.setFixedSize(620, 558)

    def show_popup(self) -> None:
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
            self.show_popup()

        elif len(self.players_list) < 1:
            self.show_popup()

        else:
            pass
