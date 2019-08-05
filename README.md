#   Author: Yiwen(Victor) Song

Welcome to the Land Battle Chess Game!\
\
If you do not know how to play, read this wikipedia page:
  https://en.wikipedia.org/wiki/Luzhanqi \
Or, you can check out the help manual within the game (press "H").

To run the game, you need to first cd into the directory and run `python3 server.py`. The program will automatically get your IP address and select an available port. Then, open a new terminal window and run `python3 __init__.py`. Copy and paste (or type in) the numbers shown in the server window. You can create another instance of the game by running `python3 __init__.py` on another computer (or another terminal window). Note that the server hosts at most two clients.

This game has three modes: singleplayer, multiplayer, and multiplayer in dark mode. In singleplayer mode, the player plays against an AI player (implemented using Minimax with alpha-beta pruning). In multiplayer mode, two players can connect to one server using socket and play against each other; in the dark mode, opponent layout is hidden. After selecting the mode, you will be able to rearrange your layout. When you confirm your layout, the game starts. Capture the flag to win!
