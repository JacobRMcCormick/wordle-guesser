import random
import argparse
from collections import Counter

import word_data

#returns feedback based on colors of each slot via wordle rules
#g == green (right slot), y == yellow (has letter but wrong slot), b == black (does not have letter)
def feedback(guess, answer):
    result = ["b"] * 5
    unmatched = Counter()

    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "g"
        else:
            unmatched[answer[i]] += 1

    for i in range(5):
        if result[i] == "b" and unmatched[guess[i]] > 0:
            result[i] = "y"
            unmatched[guess[i]] -= 1

    return "".join(result)


class Game:
    #sets up game with 0 guesses and a random word
    #if answer is given it sets the word to that
    def __init__(self, answer=None, max_guesses=6):
        valid = word_data.load_valid_words()
        if answer is None:
            answer = random.choice(valid)
        else:
            answer = answer.strip().lower()
            if answer not in valid:
                raise ValueError(f"'{answer}' is not a valid word")
        self._answer = answer
        self.max_guesses = max_guesses
        self.guesses_made = 0

    #takes in guess and returns feedback
    #increments guesses by 1 
    def guess(self, word):
        self.guesses_made += 1
        return feedback(word, self._answer)

    #returns answer
    def reveal(self):
        return self._answer

#initializes new game
#if a word is given it uses that word
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--word", help="choose the answer instead of a random one")
    args = parser.parse_args()

    try:
        game = Game(args.word)
    except ValueError as e:
        parser.error(str(e))

    print("New game started.")
    from solver import solve
    solve(game)