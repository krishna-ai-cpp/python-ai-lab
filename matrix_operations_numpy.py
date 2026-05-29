import numpy as np

try:
  user_input_str = input("Enter a sequence of 16 numbers separated by spaces (e.g., 1 2 3 ... 16): ")
  str_numbers = user_input_str.split()
  numbers = [int(s) for s in str_numbers]
  if len(numbers) == 16:
    arr = np.array(numbers).reshape(4, 4)
    print("Successfully created a 4x4 NumPy array:")
    print(arr)
    hor = np.hstack(arr)
    ver = np.vstack(arr)
    print(f"Horizontal stack: {hor}")
    print(f"verticle stack: {ver}")
    mer = np.concatenate(hor,ver)
    print(f"Merged stack: {mer}")
  else:
    print(f"Error: Expected 16 numbers for a 4x4 array, but got {len(numbers)} numbers.")

except ValueError as ve:
  print(f"Input Error: Please ensure you enter valid numbers separated by spaces. Details: {ve}")
except Exception as e:
  print(f"An unexpected error occurred: {e}")
