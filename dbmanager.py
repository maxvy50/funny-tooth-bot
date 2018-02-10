from vedis import Vedis

import config


def get_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id]
        except KeyError:
            return config.States.START.value


def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False


def get_age(user_id):
    with Vedis(config.age_db_file) as db:
        try:
            return db[user_id]
        except KeyError:
            return config.States.START.value


def set_age(user_id, value):
    with Vedis(config.age_db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False