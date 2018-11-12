# 
# Works with Python3
#
# Modified by: Ryan Sowers
#   03/06/2018
#
# Step 3: Enhance the server code further to support game logic and starting of new game.
#   Final product.
#
# Run: python3 Sowers_TCPclientP3.py IP
#

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) < 2:
    print ("Please provide <hostname>, e.g., localhost on the command line!")
    exit(1)

# Connect the socket to the port on the server given by the caller
server_address = (sys.argv[1], 10000)		# socket id
print("connecting to %s port %s" % server_address)
sock.connect(server_address)				# connect to socket

try:
    
	data = sock.recv(1024)
	print(data.decode())		# receive "Welcome to..."

	data = sock.recv(1024)
	print(data.decode())		# receive "Please guess..."

	
	while True:
		try:
			number = int(input("Guess: "))			# verify input to be integer and not other string
		except ValueError:
			print("That's not a number.")
			print("Please choose a number between 1 and 100.")
		else:
			break

	while ((number < 1) or (number > 100)):			# verify input to be in desired range
		print("Please choose a number between 1 and 100.")
		try:
			number = int(input("Guess: "))
		except ValueError:
			print("That's not a number.")

	number = str(number)							# convert back to string because that's what we're encoding as
	print("Sending your guess: %s" % number)
	sock.sendall(bytes(number, 'utf-8'))			# send guess. tried: sock.sendall(bytes(number)) to send int

	data = sock.recv(1024)
	print(data.decode())		# receive "You guessed..." game ending message

finally:
    sock.close()
