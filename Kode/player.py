import game, calculateBoard

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

        # 1 title
        self.info_label = QLabel("4-paa-stribe") # info label
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setFont(info_font)
        self.info_label.setMaximumHeight(100)
        # 2 (debug)
        self.debug_label = QLabel("Debug") # info label
        # self.debug_label.setFont(info_font)
        self.debug_label.setMaximumHeight(100)

        # info bar
        self.info_bar_top = QHBoxLayout()
        self.info_bar_top.addWidget(self.info_label, 7)
        self.info_bar_top.addWidget(self.debug_label, 3)

        self.board = "0" * 42
        self.calculate_board = calculateBoard.calculateBoard()


        

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
        main_layout.addLayout(self.info_bar_top)
        main_layout.addLayout(grid)
        central.setLayout(main_layout)
        
        
        self.show()
        self.controller=game.gameController()
    
    def resizeEvent(self, event):
        # Ensure buttons resize properly during window resize
        self.updateGeometry()  # Force the layout to update and recheck button sizes
        self.update_board(self.board)
        super().resizeEvent(event)

    def handle_button_click(self, idx:int):
        print(f"Button {idx} clicked (row: {1 + idx // 7}, cln: {1 + idx % 7})")

        # Update the board
        self.control_msg, self.turn, self.board, self.newestPieceIndex = self.calculate_board.play_move((idx % 7))
        print(self.control_msg, self.turn, self.board, self.newestPieceIndex)
        self.debug_label.setText(f"Control: {self.control_msg}\nTurn: {self.turn}\nBoard: {self.board}\nNewest piece index: {self.newestPieceIndex}")
        self.update_board(self.board)
        self.controller.send(str(idx))
        # return (idx % 7) to the server


    def update_board(self, board):
        for i in range(42):
            button_size = self.btns[i].size()
            icon_size = QSize(int(button_size.height() * 0.75), int(button_size.height() * 0.75))
            try:
                if i == self.newestPieceIndex:
                    self.btns[i].setStyleSheet("background-color: white")
                else:
                    self.btns[i].setStyleSheet("")
            except:
                pass
            
            if board[i] == "0":
                self.btns[i].setText("")  # Clear text if the cell is empty
                self.btns[i].setIcon(QIcon())  # Remove icon if no piece
            if board[i] == "1":
                self.btns[i].setText("")  # Clear text for consistency
                self.btns[i].setIcon(QIcon("./assets/RedCircle.png"))  # Red circle icon
                self.btns[i].setIconSize(QSize(icon_size))  # Set icon size
            elif board[i] == "2":
                self.btns[i].setText("")  # Clear text for consistency
                self.btns[i].setIcon(QIcon("./assets/YellowCircle.png"))  # Yellow circle icon
                self.btns[i].setIconSize(QSize(icon_size))  # Set icon size)
            

    def closeEvent(self, a0=0):
        self.controller.closeMe()
        self.close()
    

class SquareButton(QPushButton): 
    
    def sizeHint(self) -> QSize:
        size = super().sizeHint()
        return QSize(min(size.width(), size.height()), min(size.width(), size.height()))

    