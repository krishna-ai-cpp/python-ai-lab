import numpy as np
import random
n = int(input("enter the length of array: "))
arr = []
for i in range(n):
  d = random.randint(1,65)
  arr.append(d)
print(arr)
try:
  row = int(input("enter the size of row: "))
  col = int(input("enter the size of coloumn: "))
except ValueError:
  print("invalid input....")
mat = np.resize(np.array(arr) , (row,col))
try:
  if mat.shape == (8,8):
    middle = mat[2:6 , 2:6]
    print(f"\nextratedinner matrix for (8 x 8) only: {middle}")
except ValueError as e:
  print(f"ERROR: {e}\n")
value,counts = np.unique(mat , return_counts = True)
for value,counts in zip(value,counts):
  print(f"In the 2D array the value {value} repeated {counts} times \n")
