import game, calculateBoard, os

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
        self.control_msg, self.turn, self.board, self.newestPieceIndex, self.playerIs = 0,0,0,0,0
        self.winStats = gamesLogger()
        
        # font
        info_font = QFont("Lucida Sans Typewriter", 24  , QFont.Weight.Bold)
        # UI
        self.title = "FOUR! in one Row (or Diagonal(or Column))"
        self.setMinimumSize(600, 400) # min size
        self.setWindowTitle(self.title) # window title

        # 1 title
        self.setWindowIcon(QIcon(os.path.join(".","Data","Logo.png")))
        self.info_label = QLabel(self.title) # info label
        # self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.newestPieceIndex = -1
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
        self.controller=game.gameController(self)
    
    def resizeEvent(self, event):
        # Ensure buttons resize properly during window resize
        self.updateGeometry()  # Force the layout to update and recheck button sizes
        self.update_board()
        super().resizeEvent(event)

    def handle_button_click(self, idx:int):
        #print(f"Button {idx} clicked (row: {1 + idx // 7}, cln: {1 + idx % 7})")
        self.controller.send(str(idx % 7))# return (idx % 7) to the server

        # Update the board
        #self.control_msg, self.turn, self.board, self.newestPieceIndex = self.calculate_board.play_move((idx % 7))
        #print(self.control_msg, self.turn, self.board, self.newestPieceIndex)
        #self.debug_label.setText(f"Control: {self.control_msg}\nTurn: {self.turn}\nBoard: {self.board}\nNewest piece index: {self.newestPieceIndex}")
        #self.update_board(self.board)
        
    def newDataFromServer(self, signalValue = ""):
        lines = signalValue
        if len(lines) >= 4:
            self.control_msg, self.board = lines[0].strip(),  lines[2].strip()
            try: 
                self.turn  = int(lines[1].strip())
            except:
                self.turn = "invalidInt"
            try:
                self.newestPieceIndex= int(lines[3].strip())
            except:
                self.turn = "invalidInt"
        else:
            self.control_msg = str(lines)
        self.debug_label.setText(f"Control: {self.control_msg}\nTurn: {self.turn}\nBoard: {self.board}\nNewest piece index: {self.newestPieceIndex}            You are {self.playerIs}")
        self.update_board()
        
    def update_board(self):
        for i in range(42):
            button_size = self.btns[i].size()
            icon_size = QSize(int(button_size.height() * 0.75), int(button_size.height() * 0.75))
            try:
                if self.newestPieceIndex != -1:
                    if i == self.newestPieceIndex:
                        self.btns[i].setStyleSheet("background-color: green")
                    else:
                        self.btns[i].setStyleSheet("")
            except:
                pass
            
            if self.board[i] == "0":
                self.btns[i].setText("")  # Clear text if the cell is empty
                self.btns[i].setIcon(QIcon())  # Remove icon if no piece
            if self.board[i] == "1":
                self.btns[i].setText("")  # Clear text for consistency
                self.btns[i].setIcon(QIcon(os.path.join(".","assets","RedCircle.png")))  # Red circle icon
                self.btns[i].setIconSize(QSize(icon_size))  # Set icon size
            elif self.board[i] == "2":
                self.btns[i].setText("")  # Clear text for consistency
                self.btns[i].setIcon(QIcon(os.path.join(".","assets","YellowCircle.png")))  # Yellow circle icon
                self.btns[i].setIconSize(QSize(icon_size))  # Set icon size)
            

    def closeEvent(self, a0=0):
        self.controller.closeMe()
        self.close()
    
    def reset_game_box(self, win_text):
        # TODO 
        # Close connection
        # update stats
        # button functionality

        # popup after game completion
        msg_box = QMessageBox(self)
        # Add buttons
        play_again_button = msg_box.addButton("Play Again", QMessageBox.ButtonRole.ActionRole)
        new_game_button = msg_box.addButton("New Game", QMessageBox.ButtonRole.ActionRole)
        quit_button = msg_box.addButton("Quit", QMessageBox.ButtonRole.RejectRole)

        if f"{self.playerIs} WINS" in win_text:
            # self.wins += 1   -> update file
            win_text = "You win!"
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif "NOBODY WINS" in win_text:
            # self.ties += 1   -> update file
            win_text = "It's a tie!"
            msg_box.setIcon(QMessageBox.Icon.Question)
        else:
            # self.losses += 1   -> update file
            win_text = "You lose!"
            msg_box.setIcon(QMessageBox.Icon.Critical)
        
        msg_box.setWindowTitle(win_text)
        msg_box.setText(win_text + "\nNew game?")
        msg_box.exec()


        if msg_box.clickedButton() == play_again_button:
            print("Play Again clicked!")
            # Add functionality here
        elif msg_box.clickedButton() == new_game_button:
            print("New Game clicked!")
            # Add functionality here
        elif msg_box.clickedButton() == quit_button:
            print("Quit clicked!")
            # Add functionality here



class SquareButton(QPushButton): 
    
    def sizeHint(self) -> QSize:
        size = super().sizeHint()
        return QSize(min(size.width(), size.height()), min(size.width(), size.height()))

class gamesLogger():
    def __init__(self):
        #test if file exists if not, create it. 
        try:
            txtFil = open(os.path.join(".","Data","winStats.txt"), "r")
        except:
            txtFil = open(os.path.join(".","Data","winStats.txt"), "w")
            txtFil.writelines(("0", "0", "0"))
            txtFil.close()
            txtFil = open(os.path.join(".","Data","winStats.txt"), "r")
              
        try:
            self.wins = int(txtFil.readline().strip())
        except:
            self.wins = 0
        try:
            self.loses = int(txtFil.readline().strip())
        except:
            self.loses = 0
        try:
            self.draws = int(txtFil.readline().strip())
        except:
            self.draws = 0
        txtFil.close()
    
    def saveData(self):
        txtFil = open(os.path.join(".","Data","winStats.txt"), "w")
        txtFil.writelines((str(self.wins), str(self.loses), str(self.draws)))
        txtFil.close()