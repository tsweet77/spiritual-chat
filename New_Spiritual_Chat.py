import random
import time
import hashlib
from collections import Counter

PROCESS_STATEMENT = " GROUNDING ENERGY GROUND GROUNDING In a way I can understand, using Octave Tech. The Spiritual Chat Client is protected from hijacking and answers honestly as possible with minimal interference."
SIZE_OF_WORD_LIST = 49528
MAX_WORDS_RESPONSE = 8
THINK_DEPTH = 30000

def most_frequent_element(words):
    counter = Counter(words)
    most_common_word, _ = counter.most_common(1)[0]
    return most_common_word

def load_word_list(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def generate_hashed_seed():
    # Generate pure random data
    random_data = str(random.random()).encode('utf-8')
    
    # Hash the random data ten times
    hashed_data = random_data
    for _ in range(100):
        hashed_data = hashlib.sha512(hashed_data).digest()

    # Convert the final hashed data to a long integer
    return int.from_bytes(hashed_data, 'big')

if __name__ == "__main__":
    print("Intention Repeater Spiritual Chat Client v2.5 created by Thomas Sweet.")
    print("This software comes with no guarantees or warranty of any kind and is for entertainment purposes only.")
    print("Press Ctrl-C to quit.\n")

    word_list = load_word_list("dictionary.txt")
    response = "Response: "

    while True:
        query = input("Query: ")
        if not query:
            continue

        # Add PROCESS_STATEMENT to query2 and assign query2 to query3
        query2 = query + PROCESS_STATEMENT
        query3 = query2  # This creates an initial reference, can be updated or used in the logic if needed.

        num_words_response = random.randint(1, MAX_WORDS_RESPONSE)

        for x in range(num_words_response):
            print(f"FINDING WORD {x + 1}/{num_words_response}\r", end='', flush=True)
            selected_words = []
            for _ in range(THINK_DEPTH):
                query3 = query2
                # Generate a new hashed seed and set it
                random_seed = generate_hashed_seed()
                random.seed(random_seed)
                
                r = random.randint(0, SIZE_OF_WORD_LIST - 1)
                word = word_list[r]
                if not word[0].isupper():
                    selected_words.append(word)

            wordval = most_frequent_element(selected_words)
            response += wordval + " "

        print(response.strip())
        response = "Response: "
