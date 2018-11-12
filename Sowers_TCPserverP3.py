#
# Works with Python3
#
# Modified by: Ryan Sowers
#   03/06/2018
#
# Step 3: Enhance the server code further to support game logic and starting of new game.
#   Final product.
#
# Run: python3 Sowers_TCPserverP3.py IP GAME_TIME
#

import signal
import socket
import sys
import os
import random
import time
from threading import *

global player_threads
global guess_difference
global game_time
global winningNumber

player_threads = {}
guess_difference = {}

winningNumber = random.randint(1,101)
lock = Lock()
game_sem = Semaphore()

class ClientThread(Thread):
    def __init__(self, client_address, connection):
        Thread.__init__(self)
        self.csocket = connection

    # compare player guesses to find the least difference from winning number
    def compare_guess(self):
        if self == min(guess_difference, key=guess_difference.get):
            return True
        else:
            return False

    # play the game
    def run(self):
        
        response = "Welcome to, Guess that Number!"
        print("(sending.) %s" % response)
        self.csocket.send(bytes(response, 'utf-8'))   

        response = "Please guess a number from 1 to 100!"
        print("(sending.) %s" % response)
        self.csocket.send(bytes(response, 'utf-8'))

        game_sem.acquire()		# must lockout other clients to receive one guess at a time; 
        						# also prevent timer from ending game before all guesses entered

        num_guess = self.csocket.recv(1024)			# receive guess as string
        num_guess = num_guess.decode()
        print("(received) Guess: %s" % num_guess)

        lock.acquire()			# modifying dictionaries
        player_threads[self] = num_guess        # add guesses to dict of players
        guess_difference[self] = abs(winningNumber - int(num_guess))    # calculate guess differences from winning number
        lock.release()

        game_sem.release()

        game_window.wait()          # wait for game timer to finish
        if int(num_guess) == winningNumber:
        	response = "You guessed: %s, and my number was: %d. Bullseye! Winner! Play again soon!" % (num_guess, winningNumber)
        elif self.compare_guess():   
            response = "You guessed: %s, and my number was: %d. You were the closest. You win! Play again soon!" % (num_guess, winningNumber)
        else:
            response = "You guessed: %s, and my number was: %d. You weren't the closest. You lose! Goodbye." % (num_guess, winningNumber)
        print("(sending.) %s" % response)
        self.csocket.send(bytes(response, 'utf-8'))

        self.csocket.close()

class CountdownThread(Thread):
    def __init__(self):
        Thread.__init__(self)     

    # run the countdown thread after two players have joined
    def run(self):
        CountdownEvent.wait()		# wait for timer to be triggered by players joining
        gameTime = game_time
        print("Two players joined. Waiting %d seconds for more players" % gameTime)
        time.sleep(gameTime)
        sock.close()


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # tells kernel to reuse socket in TIME_WAIT state, 
															# without waiting for its natural timeout to expire
# Check for proper command line arguments
if len(sys.argv) < 3:
    print ("Please provide <hostname>, (e.g., localhost) and game time (seconds) on the command line!")
    exit(1)
    
# Bind the socket to the address given on the command line
server_name = sys.argv[1]                   # server name from command line
game_time = int(sys.argv[2])				# game time, to wait for players

server_address = (server_name, 10000)       # socket id
print("New game starting on %s port %s" % server_address)
sock.bind(server_address)                   # assign server address to socket                 

print("Waiting for players...")
CountdownEvent = Event()			    # create countdown event; used when players have joined
Countdown_Thread = CountdownThread()
Countdown_Thread.start()				# run countdown thread

game_window = Event()				# create game window event for signaling expiration

while True:
    sock.listen(1)              	# listen for TCP connection requests
    try:
        connection, client_address = sock.accept()
        print("Player connected:", client_address)
    except: 
        break

    new_thread = ClientThread(client_address, connection)   
    new_thread.start()         		# start a new thread for each player

    lock.acquire()				
    player_threads[new_thread] = 0	# modifying dicitonary with "player names" (no values yet), to establish count
    lock.release()

    if len(player_threads) > 1:     # two players have joined
        CountdownEvent.set()        # game window is open

game_sem.acquire()
game_window.set()       # signal game window has closed/timer expired; scores may be assessed

# prepare to restart game
time.sleep(1)

# OLD ENDING
# if __name__ == '__main__':
# 	getInput = input("New game? ")		# ask sys admin if server should keep running; allows an out from infinite restarts
# 	if getInput in ("Yes", "yes", "Y", "y"):
# 		os.execv(sys.executable, ['python3'] + sys.argv)	# restart script utilizing OS module 
# 	else:
# 		sys.exit()			# exit/quit server program

waiting = 5
def interrupt(signum, frame):
    os.execv(sys.executable, ['python3'] + sys.argv)    # restart script utilizing OS module 

signal.signal(signal.SIGALRM, interrupt)        # define the signal (timeout) result (restart server)

def get_input():
    try:
        getInput = input("Auto restart in 5 sec. Press Enter/return to quit.\n")      
        # ask sys admin if server should quit; allows an out from infinite restarts
    except:
        sys.exit()          # exit/quit server program

if __name__ == '__main__':
    signal.alarm(waiting)       # set alarm
    get_input()
    signal.alarm(0)             # disable the alarm if input received







