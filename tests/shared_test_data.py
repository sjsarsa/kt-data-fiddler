import pandas as pd
from collections import namedtuple

import utils
from reader import read

test_csv_filepath = 'data/assistments2009-skill-builders-corrected_1000.csv'
test_asc_filepath = 'data/test.asc'

data1 = pd.DataFrame({'user_id': [1, 2, 2, 2, 3, 3], 'skill_id': [1, 1, 2, 1, 3, 4], 'correct': [0, 1, 0, 0, 1, 0]})
data2 = read(test_csv_filepath, format='csv')
test_dataframes = [data1, data2]

grouped_data1 = pd.DataFrame({'user_id': [[1, 1], [2, 2, 2]],
                              'skill_id': [[1, 2], [3, 3, 4]],
                              'correct': [[1, 1], [0, 0, 0]]})
grouped_data2 = utils.group_data(read(test_asc_filepath, 'asc', 'user_id', 'skill_id', 'correct'), 'user_id')
grouped_test_dataframes = [grouped_data1, grouped_data2]


def dict_to_obj(my_dict, name='X'):
    return namedtuple(
        name.replace('-', '_'), (k.replace('-', '_') for k in my_dict.keys())
    )(*[x if not isinstance(x, dict) else dict_to_obj(x) for x in my_dict.values()])
