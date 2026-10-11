import csv
import shutil
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

GUESSES_CSV = DATA_DIR / "valid_guesses.csv"
REMAINING_CSV = DATA_DIR / "remaining_words.csv"

ALL_WORDS_CSV = DATA_DIR / "all_five_letter_words.csv"

def load_valid_words():
    return sorted(set(_read(GUESSES_CSV)) & set(_read(ALL_WORDS_CSV)))

def _read(path):
    with open(path, newline="") as f:
        return [row[0].strip().lower() for row in csv.reader(f)
                if row and len(row[0].strip()) == 5 and row[0].strip().isalpha()]


def _write(path, words):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for w in words:
            writer.writerow([w])

#returns all valid guesses
def load_guesses():
    return _read(GUESSES_CSV)

#resets remaining csv back to the full list of valid solutions
def reset_remaining():
    _write(REMAINING_CSV, load_valid_words())

#returns all posible words in the current game
def load_remaining():
    return _read(REMAINING_CSV)

#updates remaining words
def save_remaining(words):
    _write(REMAINING_CSV, words)

