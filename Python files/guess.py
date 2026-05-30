from random import randint
secret_number = randint(1, 20)


while True:
    prompt = "Guess the number"
    guess = int(input(prompt))
    if guess == secret_number:
        print("Congratulations!You guessed the correct number!")
        break
    elif guess > secret_number:
        print("Too high! Try again.")
    elif guess < secret_number:
        print("Too low! Try again.")
    elif guess == secret_number:
        print("Congratulations!You guessed the correct number!")

