import unittest

from store.tinyDbStore import TinyDbStore


class TestTinyDbStore(unittest.TestCase):

    def test_now(self):
        store = TinyDbStore("test.json")
        store.db.truncate()
        self.assertTrue( store.now() > 1601384579000)
        self.assertTrue( store.now() < 2001384579000)

    def test_minus_days(self):
        store = TinyDbStore("test.json")
        store.db.truncate()

        self.assertTrue(store.minus_days(1601384579000, 2) == 1598504579000)

    def test_put(self):
        store = TinyDbStore("test.json")
        store.db.truncate()

        store.put("asd", 1)
        store.put("asd", 1)
        store.put("asd", 1)
        self.assertTrue(len(store.db.all()) == 3)


    def test_get_last(self):
        store = TinyDbStore("test.json")
        store.db.truncate()

        store.put("asd", 1)
        store.put("asd", 2)
        store.put("asd", 3.0)
        store.put("asd2", 4)
        self.assertTrue(store.get_last("asd") == 3.0)
        store.put("asd", 2.0)
        self.assertTrue(store.get_last("asd") == 2.0)

        # test is empty
        store.db.truncate()
        self.assertTrue(store.get_last("asd") is None)



if __name__ == '__main__':
   unittest.main()
