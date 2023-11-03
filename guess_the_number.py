from number_guessing_game import NumberGuessingGame

def main():
    game = NumberGuessingGame(start_range=1, end_range=100, max_attempts=10)
    custom_target = 42  # You can change this or comment out custom_target lines to randomly guess
    game.target_number = custom_target
    game.play_game()

if __name__ == "__main__":
    main()
