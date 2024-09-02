import random
import time
import hashlib
from collections import Counter

PROCESS_STATEMENT = " GROUNDING ENERGY GROUND GROUNDING In a way I can understand, using Octave Tech. The Spiritual Chat Client is protected from hijacking and answers honestly as possible with minimal interference."
SIZE_OF_WORD_LIST = 49528
MAX_WORDS_RESPONSE = 8
THINK_DEPTH = 30000

def most_frequent_element(words):
    if not words:  # Check if the list is empty
        return "No valid words found"  # Default response or handle as needed
    counter = Counter(words)
    most_common_word, _ = counter.most_common(1)[0]
    return most_common_word

def load_word_list(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def generate_hashed_seed(query2):
    # Combine the current time and query2 for a dynamic seed
    current_time = str(time.time()).encode('utf-8')  # Get the current time in seconds
    query_bytes = query2.encode('utf-8')  # Convert query2 to bytes
    
    # Concatenate the time and query bytes
    combined_data = current_time + query_bytes
    
    # Hash the combined data using SHA3-512
    hashed_data = combined_data
    for _ in range(100):
        hashed_data = hashlib.sha3_512(hashed_data).digest()

    # Convert the final hashed data to a long integer
    hash_integer = int.from_bytes(hashed_data, 'big')
    
    # Combine the hash integer with the current time (in nanoseconds)
    time_integer = int(time.time_ns())  # Get the current time in nanoseconds
    combined_seed = hash_integer ^ time_integer  # XOR to combine both values

    return combined_seed

def pick_word_based_on_hash(hash_value, word_list_size):
    # Convert the hash value to a number within the range of the word list
    word_index = hash_value % word_list_size
    return word_index

if __name__ == "__main__":
    print("Intention Repeater Spiritual Chat Client v3.1 created by Thomas Sweet.")
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
                # Generate a new hashed seed using query2 and current time
                random_seed = generate_hashed_seed(query2)

                # Use the combined hash and time seed for the random number generator
                random.seed(random_seed)
                
                # Get the word index based on the hash value
                word_index = pick_word_based_on_hash(random_seed, SIZE_OF_WORD_LIST)
                
                word = word_list[word_index]
                if not word[0].isupper():
                    selected_words.append(word)

            # Check if selected_words is not empty before finding the most frequent element
            wordval = most_frequent_element(selected_words)
            response += wordval + " "

        print(response.strip())
        response = "Response: "
