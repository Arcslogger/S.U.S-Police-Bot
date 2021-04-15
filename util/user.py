class user():
    def __init__(self, id, word, time, score):
        self.id = id
        self.word = word
        self.time = time
        self.score = score
    def __gt__(self, other):
        return self.score < other.score