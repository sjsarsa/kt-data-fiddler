from unittest import TestCase
import os.path as osp
import os
from shared_test_data import data1

import writer


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        os.mkdir('tmp')

    @classmethod
    def tearDownClass(cls):
        os.rmdir('tmp')

    def test_to_asc(self):
        filepath = 'tmp/test.asc'
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
