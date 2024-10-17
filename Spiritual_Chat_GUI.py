import hashlib
import time
import sys
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from openai import OpenAI  # Ensure you have the correct OpenAI client
from datetime import datetime

# Constants
THINK_DEPTH = 88888
MAX_WORDS = 8

class SpiritualChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spiritual Chat 4.5 Python")
        self.root.geometry("800x600")

        # Initialize variables
        self.api_key = None
        self.wordlist = []
        self.logfile = None
        self.client = None

        # Default model and model selection variable
        self.selected_model_var = tk.StringVar(value="openai/chatgpt-4o-latest")

        # Setup GUI components
        self.setup_menu()
        self.setup_widgets()
        self.load_wordlist('wordlist.txt')
        self.load_api_key('OPENROUTER_API_KEY.txt')

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load API Key", command=self.load_api_key_dialog)
        file_menu.add_command(label="Specify Log File", command=self.specify_log_file)
        file_menu.add_separator()

        # Model Selection Submenu
        model_menu = tk.Menu(file_menu, tearoff=0)
        
        models = [
            "openai/chatgpt-4o-latest",
            "openai/gpt-4o-mini",
            "openai/o1-preview",
            "openai/o1-mini",
            "anthropic/claude-3.5-sonnet:beta",
            "x-ai/grok-2",
            "nvidia/llama-3.1-nemotron-70b-instruct"
        ]

        # Use Radiobuttons to allow selection with a dot next to the active model
        for model in models:
            model_menu.add_radiobutton(
                label=model,
                variable=self.selected_model_var,  # Variable to track the selected model
                value=model,
                command=lambda m=model: self.set_model(m)
            )
        
        file_menu.add_cascade(label="Select Model", menu=model_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def set_model(self, model):
        """Set the selected model and log the change."""
        self.selected_model_var.set(model)  # Update the selected model variable
        self.log_output(f"Model changed to: {self.selected_model_var.get()}")
        messagebox.showinfo("Model Changed", f"Model changed to: {self.selected_model_var.get()}")

    def setup_widgets(self):
        # Create a frame to hold both the display_area and the scrollbar
        display_frame = tk.Frame(self.root)
        display_frame.pack(expand=True, fill=tk.BOTH)

        # Scrollbar for the chat display area
        scrollbar = tk.Scrollbar(display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Display area for chat with the scrollbar configured
        self.display_area = tk.Text(display_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#1e1e1e", fg="#d4d4d4",
                                    yscrollcommand=scrollbar.set)
        self.display_area.pack(expand=True, fill=tk.BOTH)

        # Configure the scrollbar to work with the display area
        scrollbar.config(command=self.display_area.yview)

        # Entry area for user input
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(fill=tk.X)

        self.query_var = tk.StringVar()
        self.query_entry = tk.Entry(self.entry_frame, textvariable=self.query_var)
        self.query_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)
        self.query_entry.bind("<Return>", self.process_query)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.process_query)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def load_api_key(self, filename):
        try:
            with open(filename, 'r') as file:
                self.api_key = file.read().strip()
                self.initialize_client()
        except FileNotFoundError:
            messagebox.showerror("Error", "Please put OpenRouter API Key in OPENROUTER_API_KEY.txt.")
            sys.exit(1)

    def load_api_key_dialog(self):
        filename = filedialog.askopenfilename(title="Select API Key File")
        if filename:
            self.load_api_key(filename)

    def load_wordlist(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.wordlist = file.read().splitlines()
        except FileNotFoundError:
            messagebox.showerror("Error", "wordlist.txt is missing")
            sys.exit(1)
        except UnicodeDecodeError:
            messagebox.showerror("Error", "Error decoding wordlist.txt. Please ensure it is encoded in UTF-8.")
            sys.exit(1)

    def initialize_client(self):
        OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=OPENROUTER_BASE_URL
        )

    def specify_log_file(self):
        filename = filedialog.asksaveasfilename(title="Specify Log File")
        if filename:
            self.logfile = filename
            timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            self.log_output(f"Logging to {self.logfile} - {timestamp}")

    def log_output(self, content):
        """Helper function to write content to log file."""
        if self.logfile:
            with open(self.logfile, 'a', encoding='utf-8') as f:
                f.write(content + "\n")

    def process_query(self, event=None):
        query = self.query_var.get().strip()
        if not query:
            return

        # Clear the entry field
        self.query_var.set("")

        # Display the user's query
        self.display_message(f"User: {query}", "user")

        # Run the response generation in a separate thread to avoid freezing the GUI
        threading.Thread(target=self.generate_response, args=(query,)).start()

    def display_message(self, message, msg_type):
        self.display_area.config(state=tk.NORMAL)
        if msg_type == "user":
            self.display_area.insert(tk.END, f"{message}\n", "user")
        elif msg_type == "bot":
            self.display_area.insert(tk.END, f"{message}\n", "bot")
        elif msg_type == "meaning":
            self.display_area.insert(tk.END, f"{message}\n", "meaning")
        self.display_area.config(state=tk.DISABLED)
        self.display_area.see(tk.END)

    def generate_response(self, query):
        # Display "Thinking..." first in the display area
        self.display_message("Bot: Thinking...", "bot")

        # Now generate the response (simulated delay for demo purposes)
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
            selected_word_index = hash_int % len(self.wordlist)

            # Step 8: Append word to response
            response += self.wordlist[selected_word_index] + " "

        response = response.strip()

        # Now, after generating the response, replace the "Thinking..." message
        meaning = self.get_meaning(query, response)

        if meaning:
            # Clear previous "Thinking..." message by updating the last inserted message
            self.display_area.config(state=tk.NORMAL)
            self.display_area.delete("end-2l", "end-1l")  # Delete the "Thinking..." line
            self.display_area.config(state=tk.DISABLED)

            # Display the response and meaning
            self.display_message(f"Bot: {response}", "bot")
            self.display_message(f"Meaning: {meaning}", "meaning")

            # Log the conversation
            self.log_output(f"Query: {query}")
            self.log_output(f"Response: {response}")
            self.log_output(f"Meaning: {meaning}")
            self.log_output("")  # Newline for readability

    def get_meaning(self, query, response):
        # Prepare the system and user prompts
        system_prompt = "You're an expert at taking seemingly random word response generated from a Spiritual Chat software, and a user query and forming a meaning. Do not mention the words are random. Be fun."
        user_prompt = f"The user asked '{query}' and got the response '{response}'. Please give a very brief definition of each word and the meaning of each word and an overall meaning and how it relates to their query."

        try:
            chat_completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://intentionrepeater.boards.net/thread/977/updated-spiritual-chat",
                    "X-Title": "Spiritual Chat"
                },
                model=self.selected_model_var.get(),  # Use the selected model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            meaning = chat_completion.choices[0].message.content.strip()
            return meaning
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while communicating with OpenRouter API: {e}")
            return None

def main():
    root = tk.Tk()
    
    # Set up text tags for color coding
    text_widget = tk.Text()
    text_widget.tag_configure("user", foreground="#00ff00")  # Green text
    text_widget.tag_configure("bot", foreground="#00bfff")   # Light blue text
    text_widget.tag_configure("meaning", foreground="#ffff00")  # Yellow text
    
    app = SpiritualChatGUI(root)
    app.display_area.tag_configure("user", foreground="#00ff00")  # Green text
    app.display_area.tag_configure("bot", foreground="#00bfff")   # Light blue text
    app.display_area.tag_configure("meaning", foreground="#ffff00")  # Yellow text

    root.mainloop()

if __name__ == "__main__":
    main()
