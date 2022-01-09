from PyQt5.QtWidgets import QApplication
import sys
import Trivia

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Trivia.MainWindow()
    sys.exit(app.exec_())
