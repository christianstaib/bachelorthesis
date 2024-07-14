import random
import nltk
from nltk.corpus import words
from tqdm import tqdm
import click


@click.command()
@click.option(
    "-f",
    "--filename",
    required=True,
    type=click.Path(exists=False, dir_okay=False),
    help="File where word list shall be written to.",
)
@click.option(
    "-n",
    "--number_of_words",
    type=click.IntRange(min=1),
    default=1000,
    help="Desired length of word list.",
)
def generate_word_list(filename, number_of_words):
    """Program that generates a specified number of random English words and writes them to a file, separated by newlines."""

    # Download the words corpus. Has internal check to avoid mutiple downloads
    nltk.download("words")

    # Get the list of English words from nltk corpus
    word_list = words.words()

    with open(filename, "w") as file:
        for _ in tqdm(
            range(number_of_words), desc="Generating words list", leave=False
        ):
            random_word = random.choice(word_list)
            file.write(f"{random_word}\n")


if __name__ == "__main__":
    generate_word_list()
