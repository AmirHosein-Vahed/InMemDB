import sys
import unittest
import threading
import time

import InMemStore

class TestPyInMemStore(unittest.TestCase):

    @staticmethod
    def create_db():
        db = InMemStore.PyInMemStore()
        return db

    def setUp(self):
        self.db = self.create_db()

    def tearDown(self):
        self.db = None

    def test_set_and_get(self):
        self.db.set('foo', 'bar')
        self.db.commit()
        result = self.db.get('foo')
        self.assertEqual(result, 'bar')

    def test_delete(self):
        self.db.set('del_me', 'val')
        self.db.commit()
        self.assertTrue(self.db._key_exists('del_me'))
        self.db.delete('del_me')
        self.assertFalse(self.db._key_exists('del_me'))

    def test_expire(self):
        self.db.set('expired', 'val')
        self.db.commit()
        self.db.expire('expired', 2)
        self.assertEqual(self.db.ttl('expired'), 2)
        time.sleep(3)
        self.assertIsNone(self.db.get('expired'))

    def test_nonexistent_key_with_expire_should_return_minus_two(self):
        self.assertEqual(-2, self.db.ttl('nonexistent_key'))

    def test_nonexistent_key_without_expire_should_return_minus_one(self):
        self.db.set('no_ttl', 'val')
        self.db.commit()
        self.assertEqual(-1, self.db.ttl('no_ttl'))

    def test_concurrent_access(self):
        threads = []

        def run_thread(index):
            time.sleep(index / 10)
            self.db.set('concur', index)
            self.db.commit()

        for i in range(10):
            worker = threading.Thread(target=run_thread, args=(i,))
            threads.append(worker)
            worker.start()

        for thr in threads:
            thr.join()

        result = self.db.get('concur')
        self.assertEqual(result, 9)

    def test_lpush_and_rpop(self):
        self.db.lpush('my_list', 1, 2, 3)
        self.db.commit()
        first_element = self.db.rpop('my_list')
        self.assertEqual(first_element, 3)
        second_element = self.db.rpop('my_list')
        self.assertEqual(second_element, 2)

    def test_commit(self):
        self.db.set('first', '1')
        self.db.set('second', '2')
        self.db.commit()
        self.assertEqual(self.db.get('first'), '1')
        self.assertEqual(self.db.get('second'), '2')

    def test_rollback(self):
        self.db.set('first', '1')
        self.db.set('second', '2')
        self.db.rollback()
        self.assertEqual(self.db.get('first'), None)
        self.assertEqual(self.db.get('second'), None)

if __name__ == '__main__':
    res = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    exit(not res.wasSuccessful())

    # python -m unittest discover -s . -p "*test.py"