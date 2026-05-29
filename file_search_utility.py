import string
import os
def create():
    with open("data.txt",'w') as f:
        data = str(input("enter the file data......"))
        f.write(data)
        print("Sample file 'data_file.txt' created successfully.\n")

def search_utility(file_name , target):
    line_no = 1
    found_lines = []
    with open(file_name,'r') as f:
        for line in f:
            if target.lower() in line.lower():
                found_lines.append(line_no)
            line_no += 1
    return found_lines
if not os.path.exists("data.txt"):
  create()
word = str(input("enter a word to search: "))
results = search_utility("data.txt" , word)
if results:
    print(f"The word '{word}' was found on {len(results)} line(s):")
    for line in results:
        print(f"- Line {line}")
else:
    print(f"The word '{word}' was not found in the file.")
if input("\nDo you want to delete the sample file? (y/n): ").lower() == 'y':
    os.remove("data.txt")
    print("File deleted.")
