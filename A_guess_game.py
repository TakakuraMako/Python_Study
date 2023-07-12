"""A Python little game"""

temp = input("Please guess a number,")
guess = int(temp)
if guess == 8:
    print("Wow, you are right!")
else:
    print("haha, you are wrong")

print("game over")