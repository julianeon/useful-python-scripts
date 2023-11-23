import unittest
from number_guessing_game import NumberGuessingGame

class TestNumberGuessingGame(unittest.TestCase):
    def setUp(self):
        self.game = NumberGuessingGame(start_range=1, end_range=100, max_attempts=10)

    def test_check_the_guess_too_low(self):
        self.game.target_number = 20  # Set the target number to 20
        result = self.game.check_the_guess(10)
        self.assertEqual(result, "Too low. Try again.")

    def test_check_the_guess_too_high(self):
        self.game.target_number = 20  # Set the target number to 20
        result = self.game.check_the_guess(25)
        self.assertEqual(result, "Too high. Try again.")

    def test_check_the_guess_correct(self):
        self.game.target_number = 20  # Set the target number to 20
        result = self.game.check_the_guess(20)
        self.assertEqual(result, "You guessed it!")

if __name__ == "__main__":
    unittest.main()
