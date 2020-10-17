import time

from tinydb import TinyDB, where

from store.store import Store


class TinyDbStore(Store):

    def now(self):
        return int(round(time.time() * 1000))

    def minus_days(self, timestamp, days):
        return timestamp - days * 24 * 60 * 1000 * 1000

    def __init__(self, file_store):
        self.fileStore = file_store
        self.db = TinyDB(file_store)

    def put(self, tag, value):
        self.db.insert({
            'timestamp': self.now(),
            'tag': tag,
            'value': value})

    def get_last(self, tag):
        values = self.db.search((where('tag') == tag) & (where('timestamp') >= self.minus_days(self.now(), 2)))
        if len(values) == 0:
            return None
        last_value = sorted(values, key=lambda x: x['timestamp'], reverse=True)[0]['value']
        return last_value

