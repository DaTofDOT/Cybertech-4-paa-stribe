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

        
        # test
        self.board = "0" * 42
        self.turn = 1

        

        # Game board
        self.btns = [SquareButton() for _ in range(42)]
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)  # Remove any margins
        grid.setSpacing(0)  # Set spacing between buttons to 0
        for i, btn in enumerate(self.btns):
            grid.addWidget(btn, i // 7, i % 7)  # Arrange buttons in a 7-column grid
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Make the button expand
            btn.clicked.connect(lambda _, idx=i: self.handle_button_click(idx))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label)
        main_layout.addLayout(grid)
        central.setLayout(main_layout)
        
        
        self.show()
        self.controller=game.gameController()
    
    def resizeEvent(self, event):
        # Ensure buttons resize properly during window resize
        self.updateGeometry()  # Force the layout to update and recheck button sizes
        super().resizeEvent(event)

    def handle_button_click(self, idx:int):
        print(f"Button {idx} clicked (row: {1 + idx // 7}, cln: {1 + idx % 7})")
        self.board = self.board[:idx] + str(self.turn) + self.board[idx + 1:]
        self.turn = 2 if self.turn == 1 else 1

        self.update_board(self.board)
        self.controller.send(str(idx))
        # return (idx % 7) to the server


    def update_board(self, board):
        print("update board")
        print(board)
        for i in range(42):
            if board[i] == "0":
                self.btns[i].setText("")
            elif board[i] == "1":
                self.btns[i].setText("X")
            elif board[i] == "2":
                self.btns[i].setText("O")
            

    def closeEvent(self, a0=0):
        self.controller.closeMe()
        self.close()
    

class SquareButton(QPushButton):
    def sizeHint(self) -> QSize:
        size = super().sizeHint()
        return QSize(min(size.width(), size.height()), min(size.width(), size.height()))

