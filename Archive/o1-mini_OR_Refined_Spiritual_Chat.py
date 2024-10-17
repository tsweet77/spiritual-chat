import hashlib
import time
import sys
import signal
import os
from openai import OpenAI  # Updated import
from datetime import datetime

# Define THINK_DEPTH at the start
THINK_DEPTH = 88888
MAX_WORDS = 8

# Load API key from OPENROUTER_API_KEY.txt
def load_api_key(filename):
    try:
        with open(filename, 'r') as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        print("Please put OpenRouter API Key in OPENROUTER_API_KEY.txt. https://openrouter.ai/")
        sys.exit(1)

def load_wordlist(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        print("wordlist.txt is missing")
        sys.exit(1)
    except UnicodeDecodeError:
        print("Error decoding wordlist.txt. Please ensure it is encoded in UTF-8.")
        sys.exit(1)

def graceful_exit(signum, frame):
    print("\nExiting Gracefully...")
    sys.exit(0)

def get_meaning(client, query, response):
    # Prepare the system and user prompts
    system_prompt = "You're an expert at taking seemingly random word response generated from a Spiritual Chat software, and a user query and forming a meaning. Do not mention the words are random. Answer in a thoughtful, fun, playful, casual manner."
    user_prompt = f"The user asked \'{query}\' and got the response \'{response}\'. Please give a very brief definition of each word and the meaning of each word and an overall meaning and how it relates to their query."

    try:
        chat_completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://intentionrepeater.boards.net/thread/977/updated-spiritual-chat",
                "X-Title": "Spiritual Chat"
            },
            model="openai/o1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        meaning = chat_completion.choices[0].message.content.strip()
        return meaning
    except Exception as e:
        print(f"An error occurred while communicating with OpenRouter API: {e}")
        return None
    
def log_output(logfile, content):
    """Helper function to write content to both console and log file."""
    print(content)  # Print to console
    if logfile:
        with open(logfile, 'a', encoding='utf-8') as f:  # Append to the log file with UTF-8 encoding
            f.write(content + "\n")

def main():
    print("Spiritual Chat 4.5 Python")
    print("by Anthro Teacher aka Thomas Sweet")
    print("Press Ctrl-C to Quit")

    # Log file setup
    logfile = None
    if len(sys.argv) > 1:
        logfile = sys.argv[1]  # The second argument is the log file name
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        log_output(logfile, f"Logging to {logfile} - {timestamp}")
    
    # Load API key
    OPENROUTER_API_KEY = load_api_key('OPENROUTER_API_KEY.txt')
    OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
    
    words = load_wordlist('wordlist.txt')

    # Set up signal handler for graceful exit
    signal.signal(signal.SIGINT, graceful_exit)

    # Initialize OpenAI client with API key
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL
    )

    while True:
        query = input("Query: ")
        response = ""

        # Step 4: Compute initial hash_value
        epoch_time = str(int(time.time()))
        hash_input = query + ":" + epoch_time
        hash_value = hashlib.sha3_512(hash_input.encode()).hexdigest()

        # Step 5: Convert hash_value to number from 1-8
        hash_int = int(hash_value, 16)
        num_words = (hash_int % MAX_WORDS) + 1  # 1 to 8

        # Step 9: Repeat steps 4-8 num_words times
        for _ in range(num_words):
            # Step 6: Repeat hash computation THINK_DEPTH times
            for _ in range(THINK_DEPTH):
                epoch_time = str(int(time.time()))
                hash_input = query + ":" + hash_value + ":" + epoch_time
                hash_value = hashlib.sha3_512(hash_input.encode()).hexdigest()

            # Step 7: Convert hash_value to selected_word_index
            hash_int = int(hash_value, 16)
            selected_word_index = hash_int % len(words)

            # Step 8: Append word to response
            response += words[selected_word_index] + " "

        # Get the meaning from the OpenAI API
        meaning = get_meaning(client, query, response.strip())
        if meaning:
            # Step 10: Print the response
            log_output(logfile, "Query: " + query)
            log_output(logfile, "Response: " + response.strip())
            log_output(logfile, "Meaning: " + meaning)
            log_output(logfile, "")  # Newline for readability

if __name__ == "__main__":
    main()
