import numpy as np
import os
import string

name = "" # Initialize to ensure 'name' is always defined
con = ""  # Initialize to ensure 'con' is always defined

try:
  name = input("enter the file name: ")
  # Fix 1: Read content as a string directly, as it's comma-separated numbers.
  con = input("enter the content: ")
except Exception as e:
  # Catch any other potential input errors here, but the specific ValueError for int() is gone.
  print(f"An error occurred during input: {e}")

# The rest of the logic should ideally run if inputs were successful, not only on error.
# So, we move the file handling out of the previous try-except block.
if name and con: # Only proceed if both name and con have values
  if not os.path.exists(name): # Fix 3: Use the variable 'name' for file existence check
    try:
      with open(name , 'w') as f: # Fix 3: Use the variable 'name' for writing
        f.write(con) # Fix 2: 'con' is now a string, so f.write() is correct.
      print(f"File '{name}' created and content written.")
    except IOError as e:
      print(f"Error writing to file '{name}': {e}")
  else:
    print(f"File '{name}' already exists....... ")

  # Now, read from the file and process it
  try:
    with open(name , 'r') as f: # Fix 3: Use the variable 'name' for reading
      data = f.readline()
      # Clean up the string, split by comma, filter out empty strings, and convert to int
      numbers_as_strings = [s.strip() for s in data.split(',') if s.strip()]

      if numbers_as_strings:
        # Fix 4: Convert list of strings to a NumPy array, then cast to int.
        line = np.array(numbers_as_strings, dtype=int)
        dup = np.unique(line , return_counts = True)
        sor = np.sort(dup)
        print(f"All the Duplicates ({dup}) have been removed ")
        print(f"sorted data: {sor}")
      else:
        print(f"No valid numbers found in the file '{name}' content to process.")

  except FileNotFoundError:
    print(f"Error: File '{name}' not found for reading.")
  except ValueError:
    print(f"Error: Content of file '{name}' could not be converted to integers. Please ensure it contains comma-separated numbers.")
  except Exception as e:
    print(f"An unexpected error occurred during file reading or processing: {e}")
  except ValueError:
    print(f"The content of the file could not be sorted")
else:
  print("File name or content was not successfully provided. Skipping file operations.")

