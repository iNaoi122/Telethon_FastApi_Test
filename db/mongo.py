import copy
from pymongo import MongoClient
import pymongo.errors as errors


class MongoDB:
    def __init__(self):
        self._mongo = None
        self._messages = None
        self.connect()

    def connect(self):
        try:
            self._mongo = MongoClient("mongodb://root:example@localhost:27017/")
            self._messages = self._mongo["message"]["message"]
            print("Connect to MongoDB successful")
        except errors.ServerSelectionTimeoutError:
            raise errors.ServerSelectionTimeoutError("Connection timeout")
        except errors.AutoReconnect:
            raise errors.AutoReconnect("Auto reconnect errors")
        except errors.ConnectionFailure:
            raise errors.ConnectionFailure("Connection Fail")
        except errors.InvalidURI:
            raise errors.InvalidURI("Invalid URL for connection")

    def check_connect(self):
        try:
            self._mongo.server_info()
            print("Connect to MongoDB successful")
        except errors.ServerSelectionTimeoutError:
            print("Error to connect Mongo")

    def errors(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except TypeError:
            pass
        except errors.WriteError:
            raise errors.WriteError("Write Error")
        except errors.ExecutionTimeout:
            raise errors.ExecutionTimeout("Timeout")
        except errors.AutoReconnect:
            raise errors.AutoReconnect("Auto reconnect errors")
        except errors.ConnectionFailure:
            raise errors.ConnectionFailure("Connection Fail")
        except errors.BulkWriteError:
            raise errors.BulkWriteError(*args, *kwargs)
        except errors.DocumentTooLarge:
            raise errors.DocumentTooLarge

    def get_database(self):
        database = self._mongo.list_database_names()
        print(database)

    def add_message_(self, username: str, is_self: bool, text: str):
        self.errors(self._messages.insert_one, {"username": username, "is_self": is_self, "text": text})

    def add_messages(self, data: iter):
        data_for_db = copy.deepcopy(data)
        self.errors(self._messages.insert_many, data_for_db)

    def get_all_data(self):
        return self._messages.find()


if __name__ == '__main__':
    a = MongoDB()
    a.connect()
    a.get_database()
    # a.add_message("jjg", True, "j;ldjfs")
    # a.add_messages([{"username": "qekdfpi", "is_self": True, "text": "flsfisos"},
    # {"username": "pjjanda,", "is_self": False, "text": "fkgfaad"}])
    messages = a.get_all_data()
    for ms in messages:
        print(ms)
