#!/usr/bin/python3 -tt

import sys
import copy
import re

def get_nbhd(i,j):

  nbhd = set()
  i_start = int(i/3)*3
  j_start = int(j/3)*3

  for k in range(3):
    for l in range(3):
      nbhd.add((i_start+k,j_start+l))

  return nbhd

def make_poss_dict():

  poss_dict = {}

  for i in range(9):
    for j in range(9):
      poss_dict[(i,j)] = list(range(1,10))

  return poss_dict

def update_poss(sudoku_array, poss_dict):

  for i in range(9):
    for j in range(9):
      if sudoku_array[i][j] != 0:
        poss_dict[(i,j)] = []
        poss_dict = horiz_mod(i, sudoku_array[i][j], poss_dict)
        poss_dict = vert_mod(j, sudoku_array[i][j], poss_dict)
        poss_dict = nbhd_mod(i, j, sudoku_array[i][j], poss_dict)

  for i in range(9):
    poss_dict = horiz_uniq_poss(i, poss_dict)

  for j in range(9):
    poss_dict = vert_uniq_poss(j, poss_dict)

  return poss_dict

def horiz_uniq_poss(i, poss_dict):

  for j in range(9):
    for poss in poss_dict[(i,j)]:
      unique = True
      for l in list(range(j))+list(range(j+1,9)):
        if poss in poss_dict[(i,l)]:
          unique = False
      if unique:
        poss_dict[(i,j)] = [poss]

  return poss_dict

def vert_uniq_poss(j, poss_dict):

  for i in range(9):
    for poss in poss_dict[(i,j)]:
      unique = True
      for k in list(range(i))+list(range(i+1,9)):
        if poss in poss_dict[(k,j)]:
          unique = False
      if unique:
        poss_dict[(i,j)] = [poss]

  return poss_dict

def nbhd_uniq_poss(i, j, poss_dict):

  nbhd = get_nbhd(i,j)

  for loc in nbhd:
    for poss in poss_dict[loc]:
      unique = True
      for loc2 in nbhd:
        if loc != loc2 and poss in poss_dict[loc2]:
          unique = False
      if unique:
        poss_dict[loc] = [poss]

  return poss_dict

def horiz_mod(i, value, poss_dict):

  for k in range(9):
    try:
      poss_dict[(i,k)].remove(value)
    except:
      continue
  
  return poss_dict

def vert_mod(j, value, poss_dict):

  for l in range(9):
    try:
      poss_dict[(l,j)].remove(value)
    except:
      continue

  return poss_dict

def nbhd_mod(i, j, value, poss_dict):

  nbhd = get_nbhd(i, j)

  for loc in nbhd:
    try:
      poss_dict[loc].remove(value)
    except:
      continue

  return poss_dict

def make_guesses(sudoku_array, poss_dict):

  guess_stack = []

  for few_poss in range(2,10):
    for i in range(9):
      for j in range(9):
        if len(poss_dict[(i,j)]) == few_poss:
          for poss in poss_dict[(i,j)]:
            guess_stack.append(copy.deepcopy(sudoku_array))
            guess_stack[-1][i][j] = poss

          return guess_stack

def count_zeros(sudoku_array):

  zero_count = 0
  for i in range(9):
    for j in range(9):
      if sudoku_array[i][j] == 0: zero_count += 1

  return zero_count

def print_game(sudoku_array):

  for i in range(9):
    print(sudoku_array[i])
  print()

def solve_sudoku(sudoku_array):

  poss_dict = make_poss_dict()

  guess_stack = []

  zero_count = count_zeros(sudoku_array)

  while zero_count > 0:
    old_zero_count = zero_count
    poss_dict = update_poss(sudoku_array, poss_dict)
    for i in range(9):
      for j in range(9):
        if sudoku_array[i][j] == 0:
          if len(poss_dict[(i,j)]) == 0:
#            print("Contradiction found")
#            print("Going to next guess")
            if len(guess_stack) > 0:
              sudoku_array = guess_stack.pop()
              zero_count = count_zeros(sudoku_array)
#              print_game(sudoku_array)
              poss_dict = make_poss_dict()
              poss_dict = update_poss(sudoku_array, poss_dict)
            else:
              print("No more guesses available")
              sys.exit()
          elif len(poss_dict[(i,j)]) == 1:
              sudoku_array[i][j] = poss_dict[(i,j)].pop()
              zero_count -= 1
    
    if zero_count == old_zero_count:
#      print("Can't make any more deductions")
#      print_game(sudoku_array)
      guess_stack.extend(make_guesses(sudoku_array, poss_dict))
      sudoku_array = guess_stack.pop() 
      zero_count = count_zeros(sudoku_array)
#      print("Next guess:")
#      print_game(sudoku_array)
      poss_dict = make_poss_dict()
      poss_dict = update_poss(sudoku_array, poss_dict)

  return sudoku_array

def str_to_game(string):

  sudoku_array = []

  game_list = list(string)

  for i in range(9):
    row = []
    for j in range(9):
      row.append(int(game_list.pop(0)))
    sudoku_array.append(row.copy())

  return sudoku_array


def main():

  if len(sys.argv)!=2: 
    print("usage: python3 sudoku_solver.py [game]\n game must be 81 digits, with 0 standing for 'unknown'")
    sys.exit()

  game = sys.argv[1]
  if len(game) != 81:
    print("usage: python3 sudoku_solver.py [game]\n game must be 81 digits, with 0 standing for 'unknown'")
    sys.exit()

  match = re.fullmatch('^[0123456789]*$', game)
  if not match:
    print("usage: python3 sudoku_solver.py [game]\n game must be 81 digits, with 0 standing for 'unknown'")
    sys.exit()

  sudoku_array = str_to_game(game)
  print("Game:")
  print_game(sudoku_array)

  print("Solution:")
  solved_game = solve_sudoku(sudoku_array)
  print_game(solved_game)
  

if __name__ == '__main__':
  main()
