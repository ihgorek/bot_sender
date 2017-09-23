from pymongo import MongoClient

"""
Этот класс предназначен для записи всех слов всех пользователей в БД (многопоточность)
"""


class UserWord(object):
    """
    Данный класс предназначен для зранения всех сессий пользователей в БД,
    чтобы бот с каждым играл отдельно
    """

    def __init__(self):
        """Заходит в БД

        :return: UserWord object
        """
        with MongoClient('localhost', 27017) as client:
            db = client.db_userwords
            self.coll = db.coll_users

    def create_new_user(self, first_name, last_name, username, user_id):
        """Создает пользователя по шаблону

        {'username': username,
         'user_id': user_id,
         'session':
             {
                'word': "",
                'word_bot': ""
             }
         }
        :param first_name
        :param last_name
        :param username:
        :param user_id:
        :return:
        """
        d = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'user_id': user_id,
                'session':
                     {
                         'word': "",
                         'word_bot': ""
                    }
             }
        check = self.coll.find({'user_id': user_id}).count()
        if check == 0:
            self.coll.insert(d)
        else:
            self.coll.update({'user_id': user_id},
                             {'$set':
                                  {
                                      'session.word': "",
                                      'session.word_bot': ""
                                  }
                             })

    def set_word(self, user_id, word):
        self.coll.update({'user_id': user_id},
                         {'$set': {'session.word': word}})

    def set_word_bot(self, user_id, word_bot):
        self.coll.update({'user_id': user_id},
                         {'$set': {'session.word_bot': word_bot}})

    def restart(self, user_id):
        self.coll.update({'user_id': user_id},
                         {'$set':
                              {
                                  'session.word': "",
                                  'session.word_bot': ""
                              }
                         })

    def get_word(self, user_id):
        sample = self.coll.find_one({'user_id': user_id})
        word = sample['session']['word']
        return word

    def get_word_bot(self, user_id):
        sample = self.coll.find_one({'user_id': user_id})
        word_bot = sample['session']['word_bot']
        return word_bot

    def how_users(self):
        count = self.coll.find({}).count()
        return count

    def user_check(self, user_id):
        count = self.coll.find({'user_id': user_id}).count()
        if count == 0:
            return False
        else:
            return True

    def get_all(self):
        sample = self.coll.find({})
        for instance in sample:
            print(instance)

    def del_all(self):
        self.coll.remove(None)
        print('all user has been deleted')


def main():
    b = UserWord()
    f = False
    if f:
        b.del_all()
    b.get_all()


if __name__ == '__main__':
    main()
