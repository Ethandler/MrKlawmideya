import tkinter as tk
from tkinter import ttk, simpledialog
import random
from collections import defaultdict
import json
import os


class MrKlawmideya:
    def __init__(self):
        # File to store persistent data
        self.data_file = "chatbot_data.json"
        self.responses = {
            "hi": ["Hello! *hic!* How may I assist you today?"],
            "how are you": ["I'm feeling as light as a feather, *hic!* but ready to help!"],
            "what is your name": ["I am Mr. Klawmideya, your loyal, slightly tipsy assistant."],
            "goodbye": ["Farewell! *hic!* Until next time, traveler."],
            "thank you": ["You're most welcome! *hic!*"],
        }
        self.meanings = {}
        self.reinforcement_memory = defaultdict(int)
        self.disliked_memory = defaultdict(int)

        # Load persistent data
        self.load_data()

    def get_face(self):
        """Simple ASCII art face for Mr. Klawmideya."""
        return " (¬‿¬) *hic!*"

    def introduce(self):
        """Initial greeting with ASCII face."""
        return f"{self.get_face()} Greetings, traveler! I am Mr. Klawmideya, the wandering drunken master of wisdom and nonsense."

    def like_response(self, key):
        """Simulate reinforcement learning by prioritizing liked responses."""
        if key in self.responses:
            self.reinforcement_memory[key] += 1
            return f"*hic!* You liked responses for '{key}'! I'll prioritize them more."
        return "*hic!* I don’t know that one yet. Teach me first!"

    def dislike_response(self, key):
        """Track disliked responses and reduce their priority."""
        if key in self.responses:
            self.disliked_memory[key] += 1
            return f"*hic!* You didn’t like responses for '{key}'! I'll use them less often."
        return "*hic!* I don’t know that one yet. Teach me first!"

    def learn_response(self, key, response):
        """Add a new response for a specific key."""
        if key in self.responses:
            self.responses[key].append(response)
        else:
            self.responses[key] = [response]
        self.save_data()
        return f"*hic!* I’ve learned something new for '{key}': {response}"

    def learn_meaning(self, word, meaning):
        """Add a new word and its meaning."""
        self.meanings[word.lower()] = meaning
        self.save_data()
        return f"*hic!* I now know that '{word}' means: {meaning}"

    def get_response(self, user_input):
        """Generate a response based on user input."""
        user_input = user_input.lower().strip()

        # Handle questions about word meanings
        if user_input.startswith("what does") and user_input.endswith("mean"):
            word = user_input.replace("what does", "").replace("mean", "").strip()
            return self.meanings.get(word, f"*hic!* I don’t know what '{word}' means yet. Teach me, perhaps?")

        # Check for exact matches or mapped meanings in user input
        for key, response_list in self.responses.items():
            if key in user_input or any(meaning in user_input for meaning in self.meanings.get(key, [])):
                responses = self._apply_weighting(response_list, key)
                return random.choice(responses)

        # Fallback response for unknown queries
        return "*hic!* I'm not sure what you mean. Could you rephrase?"

    def _apply_weighting(self, response_list, key):
        """Adjust response priorities based on user feedback."""
        responses = response_list[:]
        if key in self.reinforcement_memory:
            responses += response_list * self.reinforcement_memory[key]
        if key in self.disliked_memory:
            responses = responses[: max(1, len(responses) - self.disliked_memory[key])]
        return responses

    def save_data(self):
        """Save responses and meanings to a JSON file for persistence."""
        data = {
            "responses": self.responses,
            "meanings": self.meanings,
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        """Load responses and meanings from a JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.responses.update(data.get("responses", {}))
                self.meanings.update(data.get("meanings", {}))


class ChatApp:
    def __init__(self, root, bot):
        self.bot = bot
        self.root = root
        self.root.title("Mr. Klawmideya Chat")
        self.root.geometry("500x700")

        # Add menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Working Prompts", command=self.show_help)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Chat Display
        self.chat_frame = tk.Frame(root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.text_widget = tk.Text(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.chat_frame, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, pady=10)

        self.input_box = tk.Text(self.input_frame, font=("Arial", 14), height=3, wrap=tk.WORD)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.input_box.bind("<Control-Return>", lambda event: self.handle_user_input())  # Ctrl+Enter binding
        self.input_box.bind("<Return>", self.newline_in_input)  # Enter binding

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.handle_user_input)
        self.send_button.pack(side=tk.RIGHT, padx=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, pady=10)

        self.like_button = tk.Button(self.button_frame, text="Like (Ctrl+1)", command=self.like_response)
        self.like_button.pack(side=tk.LEFT, padx=5)

        self.dislike_button = tk.Button(self.button_frame, text="Dislike (Ctrl+2)", command=self.dislike_response)
        self.dislike_button.pack(side=tk.LEFT, padx=5)

        self.learn_button = tk.Button(self.button_frame, text="Teach Response (Ctrl+3)", command=self.learn_response)
        self.learn_button.pack(side=tk.LEFT, padx=5)

        self.meaning_button = tk.Button(self.button_frame, text="Teach Meaning (Ctrl+4)", command=self.learn_meaning)
        self.meaning_button.pack(side=tk.LEFT, padx=5)

        self.root.bind("<Control-1>", lambda event: self.like_response())
        self.root.bind("<Control-2>", lambda event: self.dislike_response())
        self.root.bind("<Control-3>", lambda event: self.learn_response())
        self.root.bind("<Control-4>", lambda event: self.learn_meaning())

        self.display_bot_message(self.bot.introduce())

    def display_bot_message(self, message):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"Mr. Klawmideya: {message}\n\n")
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def display_user_message(self, message):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"You: {message}\n\n")
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def handle_user_input(self):
        user_input = self.input_box.get("1.0", tk.END).strip()
        if user_input:
            self.display_user_message(user_input)
            bot_response = self.bot.get_response(user_input)
            self.display_bot_message(bot_response)
            self.input_box.delete("1.0", tk.END)

    def newline_in_input(self, event):
        """Handle the Enter key to add a new line instead of sending."""
        self.input_box.insert(tk.INSERT, "\n")
        return "break"

    def like_response(self):
        key = self.input_box.get("1.0", tk.END).strip()
        if key:
            response = self.bot.like_response(key)
            self.display_bot_message(response)

    def dislike_response(self):
        key = self.input_box.get("1.0", tk.END).strip()
        if key:
            response = self.bot.dislike_response(key)
            self.display_bot_message(response)

    def learn_response(self):
        key = self.input_box.get("1.0", tk.END).strip()
        if key:
            response = simpledialog.askstring("Teach Response", f"Enter a response for '{key}':")
            if response:
                bot_response = self.bot.learn_response(key, response)
                self.display_bot_message(bot_response)

    def learn_meaning(self):
        word = self.input_box.get("1.0", tk.END).strip()
        if word:
            meaning = simpledialog.askstring("Teach Meaning", f"Enter the meaning of '{word}':")
            if meaning:
                bot_response = self.bot.learn_meaning(word, meaning)
                self.display_bot_message(bot_response)

    def show_help(self):
        """Display a new window with working prompts."""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - Working Prompts")
        help_window.geometry("400x400")

        help_text = tk.Text(help_window, wrap=tk.WORD, font=("Arial", 12), state=tk.NORMAL)
        help_text.insert(
            tk.END,
            "Working Prompts:\n\n"
            "- hi: Greet the bot\n"
            "- how are you: Ask about the bot's well-being\n"
            "- what is your name: Learn the bot's name\n"
            "- goodbye: End the conversation\n"
            "- thank you: Show gratitude\n"
            "- what does <word> mean: Ask the meaning of a word\n\n"
            "You can teach the bot new responses or meanings using the buttons below the input box.\n"
        )
        help_text.config(state=tk.DISABLED)
        help_text.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    bot = MrKlawmideya()
    app = ChatApp(root, bot)
    root.mainloop()
