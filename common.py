LETTERS = { 
    "A": ".##.\n"
         "#..#\n"
         "#..#\n"
         "####\n"
         "#..#\n"
         "#..#\n",

    "C": ".##.\n"
         "#..#\n"
         "#...\n"
         "#...\n"
         "#..#\n"
         ".##.\n",

    "J": "..##\n"
         "...#\n"
         "...#\n"
         "...#\n"
         "#..#\n"
         ".##.\n",

    "P": "###.\n"
         "#..#\n"
         "#..#\n"
         "###.\n"
         "#...\n"
         "#...\n",

    "R": "###.\n"
         "#..#\n"
         "#..#\n"
         "###.\n"
         "#.#.\n"
         "#..#\n",

    "U": "#..#\n"
         "#..#\n"
         "#..#\n"
         "#..#\n"
         "#..#\n"
         ".##.\n",

    "Z": "####\n"
         "...#\n"
         "..#.\n"
         ".#..\n"
         "#...\n"
         "####\n",
}

ALPHABET = {v: k for k, v in LETTERS.items()}


def letters(text):
    lines = text.splitlines()
    row, column = 0, 0
    while True:
        letter = ''.join(
            ''.join(line[column: column+4]) + "\n"
            for line in lines[row: row+6]
        )
        yield ALPHABET[letter]
        column += 5
