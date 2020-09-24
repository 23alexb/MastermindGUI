# MastermindGUI
Desktop GUI in wxPython (Python 2) for playing Mastermind (based on the board game).

**Instructions for running:**
- Copy "Mastermind_GUI.py" to any directory
- Open terminal
- Navigate to directory containing "Mastermind_GUI.py"
- Run the script using the following:
  - Linux (Ubuntu): "python2 Mastermind_GUI.py"
  - Mac: Run script using "pythonw Mastermind_GUI.py"

**Dependencies:**
  - Python2 installed
  - wxPython installed:
    - Linux (Ubuntu): "sudo apt-get install python-wxgtk3.0"
    - Mac: "pip install wxpython"

**Gameplay:**  
Similar to the board game on which this program is based, there is an underlying "code" consisting of four coloured "pegs" in a certain order. The game is played by guessing combinations of coloured pegs. The computer then responds with two numbers, one indicating how many of the pegs are the correct colour and in the correct position, and the other indicating how many of the correct coloured pegs are in the wrong position.
  
In the user interface, you can select coloured pegs by clicking one of the eight coloured squares on the left. The active colour is displayed above the coloured
squares in the rectangle below the "Restart Game" button. When you click on any of the "pegs" above the "Submit Guess" button, it will change to the active colour. When you are happy with the combination of pegs in your guess, click the "Submit Guess" button.
  
The interface will then show your guess underneath the "Submit Guess" button. To the left of the guess is the turn number on which the guess was made, and to the right are two numbers - the top number representing how many of the pegs in that guess were the correct colour in the correct position, and the lower number representing how many of the pegs in that guess were the correct colour in the incorrect position.
  
You can continue to submit guesses by repeating the process until the game is won, or use the "Give Up" button in the lower-left corner to finish the game and reveal the underlying code. If you make more guesses than will fit in the interface, up and down buttons will appear to the right of the guess so that you can scroll through to look at your previous guesses.
  
Clicking the "New Game" button will begin a new game with a different underlying code, while clicking "Restart Game" will start a new game, but without changing the underlying code (in case you make a mistake and would like to try again with the same answer).
  
The two main game settings are "Code length" (how long the code is, with a minimum of 3 and a maximum of 6) and "Multiples allowed" (whether or not the underlying code can include multiple instances of the same colour). These settings are controlled by buttons underneath the colour panel. Changing either of these settings will change the underlying code and start a new game.
  
The "Change Palette" button allows you to change the background and button colours of the user interface between 3 different colour settings.
