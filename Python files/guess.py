from random import randint
secret_number = randint(1, 20)
trials = 0


while True:
    prompt = "Guess a number between 1 and 20:"
    guess = int(input(prompt))
    if guess == secret_number:
        trials += 1
        print(f"Congratulations!You guessed the correct number in {trials} tries !")
        break
    elif guess > secret_number:
        print("Too high! Try again.")
        trials += 1
    elif guess < secret_number:
        print("Too low! Try again.")
        trials += 1


