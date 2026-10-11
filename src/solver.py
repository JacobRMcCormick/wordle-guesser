from collections import Counter
import argparse
import word_data
from game import Game, feedback


# returns list of probabilities for each letter to appear in each slot
def slot_probs(words):
    counts = [Counter() for _ in range(5)]   # one counter per slot
    for word in words:
        for i, letter in enumerate(word):
            counts[i][letter] += 1

    n = len(words)
    return [{letter: c / n for letter, c in slot.items()} for slot in counts]


def score_word(word, probs):
    return sum(probs[i].get(letter, 0) for i, letter in enumerate(word))


def best_guess(words):
    probs = slot_probs(words)
    return max(words, key=lambda w: score_word(w, probs))


# keeps only words that match the feedback
def filter_words(words, guess, fb):
    return [w for w in words if feedback(guess, w) == fb]

#if a game is not simulated, the user types the feedback
def ask_feedback():
    while True:
        fb = input("  Feedback (g/y/b): ").strip().lower()
        if len(fb) == 5 and set(fb) <= set("gyb"):
            return fb
        print("  Enter exactly 5 characters, each g, y, or b.")

#used for interpereting the param bool value
def str_to_bool(value):
    if value.lower() in ("true", "t", "yes", "y", "1"):
        return True
    if value.lower() in ("false", "f", "no", "n", "0"):
        return False
    raise argparse.ArgumentTypeError("unrecognized boolean format")

# plays a full game
def solve(game=None):
    word_data.reset_remaining()

    for turn in range(1, 7):
        words = word_data.load_remaining()
        if not words:
            print("No words left. Check that the feedback you entered was correct.")
            return False

        guess = best_guess(words)
        print(f"Guess {turn}: {guess}  ({len(words)} words possible)")

        if game is not None:
            fb = game.guess(guess)
            print(f"  feedback: {fb}")
        else:
            fb = ask_feedback()

        if fb == "ggggg":
            print(f"Solved in {turn} guesses!")
            return True

        word_data.save_remaining(filter_words(words, guess, fb))

    if game is not None:
        print("Out of guesses. The answer was:", game.reveal())
    else:
        print("Out of guesses.")
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulated", type=str_to_bool, default=True,
                        help="true: play a hidden word; false: you type the feedback")
    parser.add_argument("--word", help="choose the hidden answer (simulated mode only)")
    args = parser.parse_args()

    if not args.simulated:
        if args.word:
            parser.error("--word can't be used with --simulated false")
        solve(None)
    else:
        try:
            game = Game(args.word)    
        except ValueError as e:
            parser.error(str(e))
        solve(game)