import random
import string

character = string.ascii_letters + string.digits + string.punctuation
length = 12
passw = ''.join(random.choice(character)for i in range(length))
print("FINAL PASSWORD: ", passw)
