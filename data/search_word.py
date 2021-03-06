import random

from pymongo import MongoClient


class BaldaGame:
    def __init__(self):
        self.word = ''
        self.index = 0
        self.letter = ''
        self.f = False
        self.how_word = ''

    def word_search(self, mess):
        with MongoClient('localhost', 27017) as client:
            db = client.db_orf
            coll = db.orf_coll
            tmp = self.word
            reg = '^' + self.word + mess
            mens = coll.find({"word": {"$regex": reg}})
            ch = coll.find({"word": {"$regex": reg}}).count()
            if ch != 0:
                check = random.randint(0,ch-1)
            i = 0
            for men in mens:
                try:
                    self.word = tmp + mess
                    if check != i:
                        i += 1
                    else:
                        word = men['word']
                        self.index = len(self.word)
                        if (len(word) - self.index) % 2 == 0:
                            self.f = True
                        else:
                            self.f = False
                        self.how_word = word
                        self.word = word[:self.index + 1]
                        self.letter = word[self.index]
                        if len(word) == len(self.word):
                            self.word = 'done'
                        return self.word
                except IndexError as e:
                    self.word = 'done'
                    return self.word
            return 'There is no such word'

    def get_letter(self):
        intro = 'Я говорю букву: \n'
        ans = intro + self.letter
        return ans

    def outcome_of_the_game(self):
        return self.f

    def restart(self):
        self.word = ''

    def get_word(self):
        intro = 'Я загадал слово \n'
        ans = intro + self.how_word
        return ans
