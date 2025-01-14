import sys
sys.path.append("Kode")
import player #importer player fra kode mappen

from PyQt6.QtWidgets import *

if __name__ == "__main__":
    app = QApplication([])
    gui = player.player()
    app.aboutToQuit.connect(gui.closeEvent)
    gui.show() 
    app.exec()