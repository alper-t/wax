__author__ = 'tunnell'

import sys
import pymongo
import mongomock
sys.modules['pymongo'] = mongomock

import unittest
import pickle
import gzip

from tqdm import tqdm

from wax.Database import OutputDBInterface, InputDBInterface
from wax.EventBuilder.Processor import ProcessTask


class TestOnGoodEvents(unittest.TestCase):
    def setUp(self):
        f = gzip.open('tests/test_data.pkl.gz', 'rb')
        x = pickle.load(f)
        self.answer = pickle.load(f)
        hostname = '127.0.0.1'
        self.input = InputDBInterface.MongoDBInput(collection_name='dataset',
                                                 hostname=hostname)
        self.output = OutputDBInterface.MongoDBOutput(collection_name='dataset',
                                                 hostname=hostname)

        while (1):
            try:
                print('.', end='')
                self.input.collection.insert(pickle.load(f))
            except Exception as e:
                print(e)
                break

        print('')

    def test_something(self):
        p = ProcessTask('dataset', '127.0.0.1')

        for i in range(15):
            print('i %d' % i)
            p.process_time_range(i * 10**8, (i+1) * 10**8, padding=0)

        collection = self.output.get_collection()
        cursor = collection.find()
        ranges = []
        n = cursor.count()
        for i in tqdm(range(n)):
            event = next(cursor)
            ranges.append(event['range'])

        def check_in_range(time):
            for myrange in ranges:
                if myrange[0] < time < myrange[1]:
                    return True
            return False

        good = 0
        all_count = 0
        for value in self.answer:
            all_count += 1
            if check_in_range(value['time']):
                good += 1
                print('.', end='')
            else:
                print('fail', value)

        self.assertGreater((float(good)/all_count), 0.8)





if __name__ == '__main__':
    unittest.main()
