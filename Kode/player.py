import game, calculateBoard, os

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class player(QMainWindow):

    def __init__(self):
        """
        Initializes the player window for the Connect 4 game.

        This constructor sets up the main window, initializes the game components, and configures the layout and widgets, including:
        - Central widget for the main window.
        - Game initialization using `initGame()`.
        - Statistics logger for tracking wins, losses, and draws.
        - Fonts and window properties such as title and icon.
        - Information labels displaying the game title and player statistics.
        - Layouts for organizing widgets, including an info bar and a 7x6 grid of buttons representing the game board.

        The game board buttons are set to expand and are connected to a click handler for user interaction.
        """
        super().__init__()
        central = QWidget(self)
        self.setCentralWidget(central)
        self.initGame()
        
        self.winStats = gamesLogger()
        
        # font
        info_font = QFont("Lucida Sans Typewriter", 24  , QFont.Weight.Bold)
        stat_font = QFont("Lucida Sans Typewriter", 12  , QFont.Weight.Bold)

        self.setMinimumSize(600, 400) # min size

        # 1 title
        self.setWindowTitle("FOUR! in one Row (or Diagonal(or Column))") # window title
        self.setWindowIcon(QIcon(os.path.join(".","assets","Logo.png")))
        self.info_label = QLabel("Four in a row") # info label
        self.info_label.setFont(info_font)
        self.info_label.setMaximumHeight(100)

        # win stats
        self.stat_info_label = QLabel("Total Games:\nWins:\nLosses:\nDraws:")
        self.stat_info_label.setFont(stat_font)
        self.stat_info_label.setMaximumHeight(100)
        self.stats_label = QLabel(f"{self.winStats.total_games}\n{self.winStats.wins}\n{self.winStats.losses}\n{self.winStats.draws}")
        self.stats_label.setFont(stat_font)
        self.stats_label.setMaximumHeight(100)

        # info bar
        self.info_bar_top = QHBoxLayout()
        self.info_bar_top.addWidget(self.info_label, 4)
        self.info_bar_top.addWidget(self.stat_info_label, 2)
        self.info_bar_top.addWidget(self.stats_label, 1)


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
        
    
    def initGame(self):
        
        """
        Resets the game to its initial state.

        Attributes:
        - control_msg: resets to 0
        - turn: resets to 0
        - newestPieceIndex: resets to -1
        - playerIs: resets to 0
        - board: resets to a string of 42 zeros
        """
        self.control_msg, self.turn, self.newestPieceIndex, self.playerIs = 0,0,-1,0
        self.board = "0" * 42
        #self.calculate_board = calculateBoard.calculateBoard() for testing
        
        
        
    
    def resizeEvent(self, event):
        """
        Called when the window is resized. Forces the layout to update and recheck button sizes so
        that the buttons are always as large as possible while still fitting the window.
        """
        self.updateGeometry()
        self.update_board()
        super().resizeEvent(event)

    def handle_button_click(self, idx:int):
        """
        Called when a button on the game board is clicked. Sends the column number of the button to the server.

        Parameters:
        - idx: int, the index of the button that was clicked
        """
        self.controller.send(str(idx % 7))


    def newDataFromServer(self, signalValue = ""):
        """
        Called when new data is received from the server. Parses the data and updates the game
        board and turn information accordingly.

        Parameters:
        - signalValue: str, the new data received from the server

        If the data is valid, updates the control message, board, turn, and newest piece index
        accordingly. If the data is invalid, sets the control message to the received data.
        """
        
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
        
        self.update_board()
        self.update_turn_info()
        
        if "WINS" in self.control_msg:
            self.controller.setpCon("")
            self.reset_game_box(self.control_msg)
                
        
    def update_board(self):
        """
        Updates the game board buttons to reflect the current game state.

        If a piece has been placed on the board since the last update, the button
        corresponding to that piece is highlighted green. Otherwise, the buttons
        are updated with the correct icons and text based on the game state.

        """
        for i in range(42):
            button_size = self.btns[i].size()
            icon_size = QSize(int(button_size.height() * 0.75), int(button_size.height() * 0.75))
            try:
                if self.newestPieceIndex == -1:
                    self.btns[i].setStyleSheet("")
                else:
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
                self.btns[i].setIconSize(QSize(icon_size))  # Set icon size
            
    def update_turn_info(self):
        """
        Updates the turn information displayed on the game window.
        """
        if self.playerIs == "1":
            img_path = os.path.join(".", "assets", "RedCircle.png")
        elif self.playerIs == "2":
            img_path = os.path.join(".", "assets", "YellowCircle.png")

        if self.turn == int(self.playerIs):
            turn_text = "Your Turn"
        else:
            turn_text = "Opponent's Turn"
        
        # Update QLabel with HTML content
        self.info_label.setText(f"<p>You are <img src='{img_path}' width='24' height='24'><br>{turn_text}</p>")
    
    def reset_game_box(self, win_text):
        """
        Pops up a message box after the game is completed, displaying the result of the game and providing options to play again, start a new game, or quit the program.

        The buttons in the box are:

            - Play Again: restarts the game with the same IP and port
            - New Game: starts a new game where a new IP can be chosen
            - Quit: closes the game window

        The statistics are updated based on the outcome of the game.
        """
        msg_box = QMessageBox(self)
        play_again_button = msg_box.addButton("Play Again", QMessageBox.ButtonRole.ActionRole)
        new_game_button = msg_box.addButton("New Game", QMessageBox.ButtonRole.ActionRole)
        quit_button = msg_box.addButton("Quit", QMessageBox.ButtonRole.RejectRole)

        if f"{self.playerIs} WINS" in win_text:
            self.winStats.addToVariable("wins")
            win_text = "You win! :)"
            msg_box.setIcon(QMessageBox.Icon.Information)
            
        elif "NOBODY WINS" in win_text:
            self.winStats.addToVariable("draws")
            win_text = "It's a tie! :|"
            msg_box.setIcon(QMessageBox.Icon.Question)
        
        else:
            self.winStats.addToVariable("losses")
            win_text = "You lose! :("
            msg_box.setIcon(QMessageBox.Icon.Critical)
        
        # Update statistics label
        self.stats_label.setText(f"{self.winStats.total_games}\n{self.winStats.wins}\n{self.winStats.losses}\n{self.winStats.draws}")

        msg_box.setWindowIcon(QIcon(os.path.join(".","assets","Logo.png")))
        msg_box.setWindowTitle(win_text)
        msg_box.setText(win_text + "\nNew game?")
        msg_box.exec()

        if msg_box.clickedButton() == play_again_button:
            if self.controller.newConnection(False): #opretter en ny forbindelse til den gamle adresse
                self.initGame()
                self.update_board()
                self.info_label.setText("FOUR! in one Row\n(or Diagonal(or Column))")
                msg_box.close()
            else:
                msg_box.setText("Server no longer exists (。﹏。*)")
                
        elif msg_box.clickedButton() == new_game_button:
            self.initGame()
            self.update_board()
            self.controller.newGame()
            self.info_label.setText("FOUR! in one Row\n(or Diagonal(or Column))")
            msg_box.close()
            
        elif msg_box.clickedButton() == quit_button:
            msg_box.close()
            self.closeEvent()


    def closeEvent(self, a0=0):
        """
        Called when the window is about to be closed. Saves the win statistics and closes
        the connection to the server.
        """
        self.winStats.saveData()
        self.controller.closeMe()
        self.winStats.saveData()
        self.close()








class SquareButton(QPushButton): 
    def sizeHint(self) -> QSize:
        size = super().sizeHint()
        return QSize(min(size.width(), size.height()), min(size.width(), size.height()))

class gamesLogger():
    def __init__(self):
        """
        Initializes the gamesLogger.
        
        Opens the file "winStats.txt" in the "Data" folder if it exists, and reads the
        win, loss, and draw counts from it. If the file does not exist, it creates it and
        sets the counts to 0.
        
        :raises FileNotFoundError: If the file cannot be opened.
        """
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
            self.losses = int(txtFil.readline().strip())
        except:
            self.losses = 0
        try:
            self.draws = int(txtFil.readline().strip())
        except:
            self.draws = 0
        self.total_games = self.wins + self.losses + self.draws
        txtFil.close()
    
    def addToVariable(self, variable:str =""):
        """
        Updates the specified game statistic variable and saves the data.

        Parameters:
        - variable: str, the name of the statistic to update ("wins", "losses", or "draws").

        Returns:
        - True if the variable was successfully updated, False if the variable name is invalid.
        """
        if variable == "wins":
            self.wins += 1
        elif variable == "losses":
            self.losses += 1
        elif variable == "draws":
            self.draws += 1
        else:
            return False
        
        self.total_games += 1
        self.saveData()
        return True
    

    
    def saveData(self):
        """
        Saves the current win, loss, and draw counts to the file "winStats.txt" in the "Data" folder.
        
        :raises FileNotFoundError: If the file cannot be opened.
        """
        txtFil = open(os.path.join(".","Data","winStats.txt"), "w")
        txtFil.write((str(self.wins)+"\n"+str(self.losses)+"\n"+str(self.draws)))
        txtFil.close()