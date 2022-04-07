#!/usr/bin/env python3
import serial
import time
from itertools import chain, product
     
ser = serial.Serial('/dev/ttyACM2', 38400)

def make_alphabet(a=True, n=True, s=True):
  alphabet = """abcdefghijklmnopqrstuvwxyz"""
  cap = alphabet.upper()
  numbers = """1234567890"""
  symbols = """!@#$%^&*()`~-_=+[{]}\|'";:/?.>,<""" 
  characters = []

  if a:
    for char in alphabet:
      characters.append(char)

    for char in cap:
      characters.append(char)

  if n:
    for char in numbers:
      characters.append(char)

  if s:
    for char in symbols:
      characters.append(char)

  return characters

 
def bruteforce(charset, maxlength, minlen):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(minlen, maxlength + 1)))


# this is the brute forcing algorithm
def main(char_list, maxlen, minlen):
  # keep track of attempts
  attempt = 0

  # Create a list of passwords
  passes = list(bruteforce(char_list, maxlen, minlen))

  succ_passwords = []

  # Try each password in the list
  for s in passes:
    # this prints a status update every 1000 attempts
    if attempt%1000 == 0:
      print(attempt)

    # this checks the password and gets a response
    ser.write(bytes(s+'\n', 'utf-8'))
    re = ser.readline().decode('utf-8').strip()
    attempt += 1

    # This continues looping if its incorrect
    if re  == 'Incorrect password!' or re == 'Please enter the password:':
      continue

    # otherwise we say the password is a sucess!
    print(f"Found password!: '{s}'")
    print(re)

    succ_passwords.append(s)
    # checking if we should continue searching
    cont = input("Oo you want to keep finding passwords? y/n: ")
    while True:
      if cont == "y":
        break
      if cont == "n":
        return succ_passwords, attempt
      cont = input("Please enter 'y' or 'n': ")
  
  # if we found nothing return -1
  return -1, attempt



# This takes a wordlist and runs through it
def word_brute(wordlist):
  attempts = 0
  with open(wordlist, 'r') as f:
    for line in f:
      attempts += 1
      print(attempts)
      print(line)
      ser.write(bytes(line+'\n', 'utf-8'))
      if ser.readline().decode('utf-8') == 'Incorrect password!' or 'Please enter the password:':
        continue
      else:
        print(f'THE PASSWORD IS: {line}')
        return(line, attempts)


  return "NOTHING FOUND", attempts


# ---------- RUNNING --------------------
if __name__ == "__main__":
  
  print("STARTING")
  # take a time stamp
  s_time = time.time()
  attempts = 0

  password_list = []
  # generate list of characters
  x = make_alphabet() 

  # get min and max pas lengths
  min_char = int(input("Enter minimum number of letters per password: "))
  max_char = int(input("Enter maximum number of letters per password: "))

  print(f"Starting brute with min_len = {min_char} & max_len = {max_char}")
  # run the alogorithm
  for q in range(min_char, max_char):
    #p, attempts = word_brute() 
    print(f'MOVING TO MAX OF {q} CHARACTERS')
    p, at = main(x, q,q)
    attempts += at
    for password in p:
      if password != -1:
        password_list.append(password)


  print(f'Passwords: {password_list}')
  print(f'Took: {time.time()-s_time} seconds to complete')
  print(f'Took {attempts} Attempts')

