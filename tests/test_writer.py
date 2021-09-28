from unittest import TestCase
import os
from shared_test_data import data1

from src import writer

tmpdir = 'test_tmp'


class WriterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        os.mkdir(tmpdir)

    @classmethod
    def tearDownClass(cls):
        os.rmdir(tmpdir)

    def test_to_asc(self):
        filepath = tmpdir + '/test.asc'
        writer.write(data1, filepath, format='asc')

        expected = """
        1
        1
        0
        3
        1,2,1
        1,0,0
        2
        3,4
        1,0
        """.split()

        with open(filepath) as f:
            actual = f.read().splitlines()

        self.assertEqual(expected, actual)

        os.remove(filepath)
