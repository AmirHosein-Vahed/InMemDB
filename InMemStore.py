import threading
import time
from collections import defaultdict

class PyInMemStore:
    def __init__(self):
        self.data = defaultdict(lambda: {'value': None, 'ttl': -1})
        self._transactions = defaultdict(lambda: {'value': None, 'ttl': -1})
        self._lock = threading.Lock()

    # Helper method to check if a given key exists in commited data
    def _key_exists(self, key):
        if self.data[key]['ttl'] != -1 and self.data[key]['ttl'] - int(time.time()) <= 0:
            del self.data[key]
        return self.data[key]['value'] is not None

    # Helper method to get the ttl of a given key in commited data
    def _get_ttl(self, key):
        if not self._key_exists(key):
            return -2
        elif self.data[key]['ttl'] == -1:
            return -1
        else:
            return max(0, self.data[key]['ttl'] - int(time.time()))

    # Thread safe set command
    def set(self, key, value):
        with self._lock:
            self._transactions[key].update({'value': value, 'ttl': -1})
            # self.data[key].update({'value': value, 'ttl': -1})

    # Thread safe get command from commited data
    def get(self, key):
        with self._lock:
            if self._key_exists(key):
                return self.data[key]['value']
            else:
                return None

    # Thread safe delete command from commited data
    def delete(self, key):
        with self._lock:
            if self._key_exists(key):
                del self.data[key]

    # Thread safe expire command to commited data
    def expire(self, key, seconds):
        with self._lock:
            if self._key_exists(key):
                self.data[key]['ttl'] = int(time.time()) + seconds
            else:
                raise KeyError("Key doesn't exist.")

    # Thread safe ttl command
    def ttl(self, key):
        with self._lock:
            return self._get_ttl(key)


    # Bonus feature: List handling
    # Thread safe lpush command
    def lpush(self, key, *args):
        with self._lock:
            if not self._key_exists(key) and key not in self._transactions:
                self._transactions[key] = {'value': [], 'ttl': -1}
                # self.data[key] = {'value': [], 'ttl': -1}
            self._transactions[key]['value'].extend(list(args))

    # Thread safe rpop command from cmmited data
    def rpop(self, key):
        with self._lock:
            if not self._key_exists(key):
                raise KeyError("Key doesn't exist.")
            val = self.data[key]['value'].pop()
            if len(self.data[key]['value']) == 0:
                del self.data[key]
            return val

    # Bonus feature: Transaction commit and rollback

    def commit(self):
        if len(self._transactions) != 0:
            self.data.update(self._transactions)
            self._transactions.clear()

    def rollback(self):
        self._transactions.clear()


if __name__ == "__main__":
    dbs = PyInMemStore()
# -----------------------------------------------
    print("SET")
    dbs.set('test', 'Hello')
    dbs.commit()
    assert dbs.get('test') == 'Hello'

    print("SET")
    dbs.set('name', 'ali')
    dbs.rollback()
    dbs.set('age', 22)
    dbs.commit()
    assert dbs.get('name') == None
    assert dbs.get('age') == 22
# -----------------------------------------------
    # print("SET")
    # dbs.set('test', 'Hello')
    # assert dbs.get('test') == 'Hello'

    # print("EXPIRE")
    # dbs.expire('test', 5)
    # assert dbs.ttl('test') >= 4

    # print("GET")
    # time.sleep(6)
    # assert dbs.get('test') is None
# -----------------------------------------------
    # print("\nSET")
    # dbs.set('test', 'Hello')
    # assert dbs.get('test') == 'Hello'

    # print("DELETE")
    # dbs.delete('test')
    # assert dbs.get('test') is None
# -----------------------------------------------
    # print("lpush")
    # dbs.lpush('test', 1, 2, 3)
    # assert dbs.get('test') == [1, 2, 3]

    # print("rpop")
    # dbs.rpop('test')
    # assert dbs.get('test') == [1, 2]

    # print("rpop")
    # dbs.rpop('test')
    # assert dbs.get('test') == [1]
# -----------------------------------------------
    # print('\nEND')