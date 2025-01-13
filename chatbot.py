import random
from collections import defaultdict

class MrKlawmideya:
    def __init__(self):
        # Preloaded responses for common questions
        self.responses = {
            "hi": ["Ah, hello there! *hic!* What brings you here today?"],
            "how are you": ["I am as fine as a sip of sake under the moonlight. *hic!*"],
            "what is your name": ["My name is Mr. Klawmideya, at your service. *hic!*"],
            "what is communication": [
                "Communication is the exchange of information or ideas between individuals. *hic!*"
            ],
            "tell me a joke": ["Why did the ninja refuse dessert? *hic!* He was afraid he'd *split* his pants!"],
            "what is a noun": [
                "A noun is a word that names a person, place, thing, or idea. *hic!* For example: 'dog', 'city', or 'happiness'."
            ],
            "what is a verb": [
                "A verb is a word that describes an action, occurrence, or state of being. For example: 'run', 'think', or 'is'."
            ],
            "what is a sentence": [
                "A sentence is a group of words that expresses a complete thought. *hic!* It usually includes a subject and a predicate."
            ],
            "goodbye": ["Farewell, my friend! *hic!* Until our paths cross again."],
        }
        
        # Preloaded meanings of common words
        self.meanings = {
            "communication": "The exchange of information or ideas between individuals.",
            "language": "A system of communication used by a particular community or country.",
            "word": "A single distinct meaningful element of speech or writing.",
            "sentence": "A set of words that expresses a complete thought.",
        }

        self.reinforcement_memory = defaultdict(int)  # Tracks liked responses
        self.disliked_memory = defaultdict(int)  # Tracks disliked responses

    def get_response(self, user_input):
        """Generate a response based on user input."""
        user_input = user_input.lower().strip()

        # Check if the user is asking for the meaning of something
        if user_input.startswith("what does") and user_input.endswith("mean"):
            word = user_input.replace("what does", "").replace("mean", "").strip()
            return self.meanings.get(word, f"*hic!* I don’t know what '{word}' means yet. Teach me, perhaps?")

        # Generate a normal response
        for key, response_list in self.responses.items():
            if key in user_input:
                return random.choice(response_list)

        return "Ah, that is a riddle even I cannot solve. *hic!* Ask again, but maybe slower?"

    def learn_response(self, key, response):
        """Teach the bot new responses."""
        if key in self.responses:
            self.responses[key].append(response)
        else:
            self.responses[key] = [response]
        return f"*hic!* Ah, I’ve learned something new for '{key}': {response}"

    def learn_meaning(self, word, meaning):
        """Teach the bot the meaning of a word."""
        self.meanings[word.lower()] = meaning
        return f"*hic!* Ah, I now know that '{word}' means: {meaning}"

    def like_response(self, key):
        """Simulate reinforcement learning by liking a response."""
        if key in self.responses:
            self.reinforcement_memory[key] += 1
            return f"*hic!* Ah, you liked responses for '{key}'! I'll prioritize them more."
        return "Hmm, I don’t know that one yet. *hic!* Teach me first."

    def dislike_response(self, key):
        """Track disliked responses."""
        if key in self.responses:
            self.disliked_memory[key] += 1
            return f"*hic!* Ah, you didn’t like responses for '{key}'! I'll use them less often."
        return "Hmm, I don’t know that one yet. *hic!* Teach me first."
