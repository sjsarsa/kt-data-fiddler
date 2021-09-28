import pandas as pd
from collections import namedtuple
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import util
from src.reader import read_kt_data

test_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
test_csv_filepath = os.path.join(test_data_dir, 'assistments2009-skill-builders-corrected_1000.csv')
test_simple_csv_filepath = os.path.join(test_data_dir, 'simple.csv')
test_asc_filepath = os.path.join(test_data_dir, 'test.asc')

data1 = pd.DataFrame({'user_id': [1, 2, 2, 2, 3, 3], 'skill_id': [1, 1, 2, 1, 3, 4], 'correct': [0, 1, 0, 0, 1, 0]})
data2 = read_kt_data(test_csv_filepath, format='csv')
test_dataframes = [data1, data2]

grouped_data1 = pd.DataFrame({'user_id': [[1, 1], [2, 2, 2]],
                              'skill_id': [[1, 2], [3, 3, 4]],
                              'correct': [[1, 1], [0, 0, 0]]})
grouped_data2 = util.group_data(read_kt_data(test_asc_filepath, 'asc', 'user_id', 'skill_id', 'correct'), 'user_id')
grouped_test_dataframes = [grouped_data1, grouped_data2]


def dict_to_obj(my_dict, name='X'):
    return namedtuple(
        name.replace('-', '_'), (k.replace('-', '_') for k in my_dict.keys())
    )(*[x if not isinstance(x, dict) else dict_to_obj(x) for x in my_dict.values()])
