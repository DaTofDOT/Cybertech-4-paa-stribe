# README

## Requirements
To run this project, you need to have the following installed on your system:
- Python (version 3.x)
- PyQt6 library

You can install PyQt6 by running:
```bash
pip install PyQt6
```

## How to Run the Game

1. **Starting the Game:**
   Run the main program file to launch the game interface.
   ```bash
   python main.py
   ```

2. **Creating or Joining a Game:**
   - Upon starting, a popup window will appear with options to either **Host** or **Join** a game.
     - **Host:**
       - Selecting "Host" creates a server on the local machine.
       - An IP address is displayed, which can be shared with another player who wants to join the game.
     - **Join:**
       - To join a game, input the IP address provided by the host and click "Join."

3. **Running Two Instances on One Machine:**
   - To test the game with two players on the same machine, open two instances of the program.
   - In the second instance, click "Join" without entering an IP address. This will automatically attempt to connect to the local host server.

## Game Flow
The game flows as expected, by players alternating turns as show in the game.

- **Game End Options:**
  After a game is finished, players are presented with three options:
  1. **Rematch:**
     - Joins the same server and IP.
     - A new game starts when both players choose this option.
  2. **New Game:**
     - Returns to the initial popup screen where you can choose to host or join a new game.
  3. **Quit:**
     - Closes the game entirely.

## Hosting a Standalone Server

- You can host a local server independently of the game UI by running the `mainServer.py` file:
  ```bash
  python mainServer.py
  ```
- This creates a server that can be controlled via the command line (CMD) and remains active until manually terminated.

## Additional Notes

- Ensure that both players are connected to the same network for seamless communication if not using localhost.
- For debugging or testing purposes, you may open multiple instances on one machine as described above.
