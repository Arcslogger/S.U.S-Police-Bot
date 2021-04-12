class user():
    def __init__(self, id, word, time):
        self.id = id
        self.word = word
        self.time = time
    def __lt__(self, other):
        return self.time < other.time