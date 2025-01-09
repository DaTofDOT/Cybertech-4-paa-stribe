import game

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class player(QMainWindow):
    '''
    hovedklassen
    '''
    def __init__(self):
        super().__init__()
        central = QWidget(self)
        self.setCentralWidget(central)

        # font
        info_font = QFont("Lucida Sans Typewriter", 18, QFont.Weight.Bold)
        # UI
        self.setMinimumSize(600, 400) # min size
        self.setWindowTitle("4-paa-stribe") # window title
        self.info_label = QLabel("4-paa-stribe") # info label
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setFont(info_font)
        self.info_label.setMaximumHeight(100)

        



        

        # Game board
        self.btns = [QPushButton() for _ in range(42)]
        grid = QGridLayout()
        for i, btn in enumerate(self.btns):
            grid.addWidget(btn, i // 7, i % 7)
            btn.clicked.connect(lambda _, idx=i+1: self.handle_button_click(idx))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        main_layout.addLayout(grid)
        central.setLayout(main_layout)


        def handle_button_click(idx):
            pass
    
    def closeEvent(self, a0=0):
        
        self.close()