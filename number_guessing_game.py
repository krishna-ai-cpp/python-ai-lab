import random

# Generate a random number once for the player to guess
secret_number = random.randint(1, 100)

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

# Initialize a flag to control the guessing loop
guessed_correctly = False
while not guessed_correctly:
  try:
    # Get user input, convert to lowercase for 'quit' check
    user_guess_str = input("Guess a number (or type 'quit' to exit): ").lower()
    
    if user_guess_str == "quit":
      print("Exiting game. Thanks for playing!")
      break # Exit the game loop
    
    # Convert input to integer
    ch = int(user_guess_str) 

    if ch < secret_number:
        print("CHOOSE A HIGHER NUMBER.....")
    elif ch > secret_number:
        print("CHOOSE A LOWER NUMBER....")
    else:
        print("YOU GUESSED IT RIGHT.....")
        guessed_correctly = True # Set flag to true to exit the loop
  except ValueError:
    print("Invalid input. Please enter a whole number or 'quit'.")
