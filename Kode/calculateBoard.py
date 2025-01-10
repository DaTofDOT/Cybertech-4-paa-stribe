def play_move(board_str: str, col: int, player_num: int) -> tuple[str, str, str, int]:
    """
    Simulate a move in the Connect 4 game.
    
    Parameters:
    - board_str: string representing the board (length of 42)
    - col: integer (0-6) where the player wants to drop their piece
    - player_num: '1' or '2' (current player)
    
    Returns:
    - control: a string ("OK", "INVALID", "1 WINS", "2 WINS", "NOBODY WINS")
    - next_player: string ('1' or '2') indicating whose turn it is
    - new_board_str: updated board string
    - newest_piece_index: index of the newly placed piece (0-41)
    """
    # Convert board string into a list for easier manipulation
    board_list = list(board_str)
    
    # Check if the column is valid and not full
    for row in range(5, -1, -1):  # Check from the bottom row (index 5) upwards
        index = row * 7 + col  # Calculate the index in the board string for this position
        if board_list[index] == "0":
            # Found the first available spot in the column
            board_list[index] = str(player_num)  # Place the player's piece
            newest_piece_index = index
            break
    else:
        # If no available space is found in the column, it's an invalid move
        return "INVALID", str(player_num), board_str, -1  # Return current player as next player
    
    # Convert the list back to a string
    new_board_str = "".join(board_list)
    
    # Check if the current player has won
    if check_win(new_board_str, str(player_num)):
        control = f"{player_num} WINS"
        return control, str(player_num), new_board_str, newest_piece_index
    
    # Check if the board is full (draw scenario)
    if "0" not in new_board_str:
        control = "NOBODY WINS"
        return control, str(player_num), new_board_str, newest_piece_index
    
    # If no winner yet, it's the next player's turn
    control = "OK"
    next_player = 2 if player_num == 1 else 1
    return control, next_player, new_board_str, newest_piece_index

def check_win(board: str, player: str) -> bool:
    """
    Check if a player has won the game.
    
    Parameters:
    - board: string representing the board (length of 42)
    - player: '1' or '2' (current player)
    
    Returns:
    - True if the player has won, False otherwise.
    """
    # Directions: right, down, down-right, down-left
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for row in range(6):
        for col in range(7):
            if board[row * 7 + col] == player:
                # Check each direction
                for dr, dc in directions:
                    count = 0
                    for i in range(4):
                        r, c = row + i * dr, col + i * dc
                        if 0 <= r < 6 and 0 <= c < 7 and board[r * 7 + c] == player:
                            count += 1
                        else:
                            break
                    if count == 4:  # Found a winning line
                        return True
    return False