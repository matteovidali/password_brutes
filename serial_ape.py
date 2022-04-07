#!/usr/bin/env python3
import serial
import time
from itertools import chain, product
     
# this makes a list of usable characters
# set a to true to get all alphatet characters a-z lower and capital
# set n to true to get all numerical symbols 1-9
# set s to true to get all other non alpha-numerical characters
# you can get all by setting all to true
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


# this function generates a list of combinations of the wordlist
# it will start by generating combos of length minlen up to maxlen
def bruteforce(charset, maxlength, minlen):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(minlen, maxlength + 1)))


# this is the brute forcing algorithm
def force_crack(ser, char_list, maxlen, minlen):
  # keep track of attempts
  attempt = 0

  # Create a list of passwords
  passes = list(bruteforce(char_list, maxlen, minlen))

  succ_passwords = []

  # Try each password in the list
  for s in passes:
    ser.readline()
    # this prints a status update every 1000 attempts
    if attempt%1000 == 0:
      print(attempt)

    # this checks the password and gets a response
    ser.write(bytes(s+'\r', 'utf-8'))
    re = ser.readline().decode('utf-8').strip()
    attempt += 1

    # This continues looping if its incorrect
    if re  == 'Incorrect password!': #or re == 'Please enter the password:':
      continue

    # otherwise we say the password is a sucess!
    print(f"Found password!: '{s}'")
    print(re)

    succ_passwords.append(s)
    # checking if we should continue searching
    cont = input("Do you want to keep finding passwords? y/n: ")
    while True:
      if cont == "y":
        break
      if cont == "n":
        return succ_passwords, attempt
      cont = input("Please enter 'y' or 'n': ")
  
  # if we found nothing return -1
  return [-1], attempt



# This takes a wordlist and runs through it
def word_brute(ser, wordlist):
  attempts = 0
  with open(wordlist, 'r') as f:
    for line in f:
      attempts += 1
      print(attempts)
      print(line)
      ser.write(bytes(line+'\r', 'utf-8'))
      if ser.readline().decode('utf-8') == 'Incorrect password!' or 'Please enter the password:':
        continue
      else:
        print(f'THE PASSWORD IS: {line}')
        return(line, attempts)


  return "NOTHING FOUND", attempts

# Checks passwords more manually, takes a good password list and carefully
# listents for sucess responses
def pass_check(ser, pass_list):
  good_words = []
  for p in pass_list:
    re = ser.readline().decode('utf-8').strip()
    if re != 'Please enter the password:':
      ser.write(b'\n')
      continue

    print(f"Checking '{p}' ...")
    ser.write(bytes(p+'\r', 'utf-8'))

    re = ser.readline().decode('utf-8').strip()
    print(re)
    if re == 'SUCCESS!':
      good_words.append(p)
    print('------------------')

  return good_words

def main():
  ser = serial.Serial('/dev/ttyACM2', 38400)
  print("STARTING")

  # take a time stamp and setup trackers
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
    p, at = force_crack(ser, x, q,q)
    attempts += at
    for password in p:
      if password != -1:
        password_list.append(password)

  print(f'Found Passwords: {password_list}')
  print(f'Took: {time.time()-s_time} seconds to complete')
  print(f'Took {attempts} Attempts')

  print("Checking Passwords...")
  good = pass_check(ser, password_list)
  
  print("\n\nGOOD PASSWORDS:")
  for g in good:
    print(g)
    

# ---------- RUNNING --------------------
if __name__ == "__main__":
  main()
