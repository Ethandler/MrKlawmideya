import tkinter as tk
from tkinter import ttk, simpledialog
import random
from collections import defaultdict


class MrKlawmideya:
    def __init__(self):
        self.responses = {
            "hi": ["Ah, hello there! *hic!* What brings you here today?"],
            "how are you": ["I am as fine as a sip of sake under the moonlight. *hic!*"],
            "what is your name": ["My name is Mr. Klawmideya, at your service. *hic!*"],
            "tell me a joke": ["Why did the ninja refuse dessert? *hic!* He was afraid he'd *split* his pants!"],
            "goodbye": ["Farewell, my friend! *hic!* Until our paths cross again."],
        }
        self.meanings = {
            "communication": "The exchange of information or ideas between individuals.",
            "language": "A system of communication used by a particular community or country.",
            "sentence": "A group of words that expresses a complete thought.",
        }
        self.reinforcement_memory = defaultdict(int)  # Tracks liked responses
        self.disliked_memory = defaultdict(int)  # Tracks disliked responses

    def get_face(self):
        return " (¬‿¬) *hic!*"

    def introduce(self):
        return f"{self.get_face()} Greetings, traveler. I am Mr. Klawmideya, the wandering drunken master. What wisdom or nonsense do you seek?"

    def like_response(self, key):
        if key in self.responses:
            self.reinforcement_memory[key] += 1
            return f"*hic!* Ah, you liked responses for '{key}'! I'll prioritize them more."
        return "Hmm, I don’t know that one yet. *hic!* Teach me first."

    def dislike_response(self, key):
        if key in self.responses:
            self.disliked_memory[key] += 1
            return f"*hic!* Ah, you didn’t like responses for '{key}'! I'll use them less often."
        return "Hmm, I don’t know that one yet. *hic!* Teach me first."

    def learn_response(self, key, response):
        if key in self.responses:
            self.responses[key].append(response)
        else:
            self.responses[key] = [response]
        return f"*hic!* Ah, I’ve learned something new for '{key}': {response}"

    def learn_meaning(self, word, meaning):
        self.meanings[word.lower()] = meaning
        return f"*hic!* Ah, I now know that '{word}' means: {meaning}"

    def get_response(self, user_input):
        user_input = user_input.lower().strip()

        if user_input.startswith("what does") and user_input.endswith("mean"):
            word = user_input.replace("what does", "").replace("mean", "").strip()
            return self.meanings.get(word, f"*hic!* I don’t know what '{word}' means yet. Teach me, perhaps?")

        for key, response_list in self.responses.items():
            if key in user_input:
                responses = self._apply_weighting(response_list, key)
                return random.choice(responses)

        return "Ah, that is a riddle even I cannot solve. *hic!* Ask again, but maybe slower?"

    def _apply_weighting(self, response_list, key):
        responses = response_list[:]
        if key in self.reinforcement_memory:
            responses += response_list * self.reinforcement_memory[key]
        if key in self.disliked_memory:
            responses = responses[: max(1, len(responses) - self.disliked_memory[key])]
        return responses


class ChatApp:
    def __init__(self, root, bot):
        self.bot = bot
        self.root = root
        self.root.title("Mr. Klawmideya Chat")
        self.root.geometry("500x700")

        self.chat_frame = tk.Frame(root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.text_widget = tk.Text(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.chat_frame, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, pady=10)

        self.input_box = tk.Entry(self.input_frame, font=("Arial", 14))
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.handle_user_input)
        self.send_button.pack(side=tk.RIGHT, padx=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, pady=10)

        self.like_button = tk.Button(self.button_frame, text="Like", command=self.like_response)
        self.like_button.pack(side=tk.LEFT, padx=5)

        self.dislike_button = tk.Button(self.button_frame, text="Dislike", command=self.dislike_response)
        self.dislike_button.pack(side=tk.LEFT, padx=5)

        self.learn_button = tk.Button(self.button_frame, text="Teach Response", command=self.learn_response)
        self.learn_button.pack(side=tk.LEFT, padx=5)

        self.meaning_button = tk.Button(self.button_frame, text="Teach Meaning", command=self.learn_meaning)
        self.meaning_button.pack(side=tk.LEFT, padx=5)

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
        user_input = self.input_box.get().strip()
        if user_input:
            self.display_user_message(user_input)
            bot_response = self.bot.get_response(user_input)
            self.display_bot_message(bot_response)
            self.input_box.delete(0, tk.END)

    def like_response(self):
        key = self.input_box.get().strip()
        if key:
            response = self.bot.like_response(key)
            self.display_bot_message(response)

    def dislike_response(self):
        key = self.input_box.get().strip()
        if key:
            response = self.bot.dislike_response(key)
            self.display_bot_message(response)

    def learn_response(self):
        key = self.input_box.get().strip()
        if key:
            response = simpledialog.askstring("Teach Response", f"Enter a response for '{key}':")
            if response:
                bot_response = self.bot.learn_response(key, response)
                self.display_bot_message(bot_response)

    def learn_meaning(self):
        word = self.input_box.get().strip()
        if word:
            meaning = simpledialog.askstring("Teach Meaning", f"Enter the meaning of '{word}':")
            if meaning:
                bot_response = self.bot.learn_meaning(word, meaning)
                self.display_bot_message(bot_response)


if __name__ == "__main__":
    root = tk.Tk()
    bot = MrKlawmideya()
    app = ChatApp(root, bot)
    root.mainloop()
