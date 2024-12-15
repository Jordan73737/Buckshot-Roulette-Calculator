# Buckshot Roulette Tracker

A program used for tracking live and blank shells whilst playing Buckshot Roulette (steam game).

## Features
- Dynamic shell tracking
- Probability calculations for live and blank shells
- Reset and Clear option

## Setup
Run the following commands in the CMD:
1. git clone https://github.com/Jordan73737/Buckshot-Roulette-Calculator.git
2. cd Buckshot-Roulette-Calculator
3. python -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. python app.py


## How to use the program:
1. Input the number of lives and blanks into the corresponding boxes at the top
2. Click Start Game
3. Every time you or your opponents(s) fire a round (or otherwise exposes the current shell inside the shotgun) - you configure the shell in the program to be live or blank
4. Configure shells by clicking a numbered circle and then click either the 'Mark Live' or 'Mark Blank' button
5. If you selected the wrong shell type then click the shell and then click the 'Clear Configuration' button
6. Hit the Reset Game button once the round has finished
7. Repeat Step 1

