import random

class NumberGuessingGame:
    def __init__(self, start_range=1, end_range=100, max_attempts=10):
        self.start_range = start_range
        self.end_range = end_range
        self.max_attempts = max_attempts
        self.target_number = self.generate_random_number()

    def generate_random_number(self):
        return random.randint(self.start_range, self.end_range)

    def get_user_guess(self):
        while True:
            try:
                guess = int(input("Guess the number: "))
                return guess
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def check_the_guess(self, guess):
        if guess == self.target_number:
            return "You guessed it!"
        elif guess < self.target_number:
            return "Too low. Try again."
        else:
            return "Too high. Try again."

    def play_game(self):
        print("Welcome to the number guessing game!")
        print(f"I'm thinking of a number between {self.start_range} and {self.end_range}.")

        attempts = 0

        while attempts < self.max_attempts:
            user_guess = self.get_user_guess()
            attempts += 1
            result = self.check_the_guess(user_guess)
            print(result)

            if result == "You guessed it!":
                print(f"You guessed the correct number {self.target_number} in {attempts} attempts.")
                break

        else:
            print(f"Sorry, you've run out of attempts. The correct number was {self.target_number}.")

