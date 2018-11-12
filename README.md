# NetworkGame
develop a networked computer game called “Guess that Number!”

develop both the server and client programs. 
The game host starts the game by starting the game server on a specific port (fixed). the server’s IP address must be a command line option or input via a GUI for the client program. 
Once started the server picks an integer randomly from 1 to 100 and waits for a fixed amount of time in seconds (variable name: game_time) for the players to join the game. 
The server should not start counting down the time until at least two players have joined the game.
A player joins the game by starting the client program. Once joined, the client prompts the player to input an integer from 1 to 100.
At the end of the game_time period, the server compares all the guesses from the players who have joined and discloses the outcome to all players using messages such as “The number is <> and your guess is <>. You win with the closest guess / Better luck next time”. 
The server should start another game immediately after that.
