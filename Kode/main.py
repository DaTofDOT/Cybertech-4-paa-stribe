import player

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *

if __name__ == "__main__":
    app = QApplication([])
    gui = player.player()
    app.aboutToQuit.connect(gui.closeEvent)
    gui.show() 
    app.exec()