from numpy import inf
from datetime import datetime

args_map = {
    'min_attempt_count': {
        'default': 2,
        'type': int,
        'help': 'Remove students with less than min attempt count attempts.'
    },
    'max_attempt_count': {
        'default': inf,
        'type': int,
        'help': 'Apply maximum attempt count to filter or split attempt sequences'
    },
    'max_attempt_filter': {
        'default': 'split',
        'choices': ['split', 'remove', 'cut'],
        'type': str,
        'help': 'Determine how maximum attempt count is applied. \
                  \nSplit creates more data (implemented chiefly to test SAKT). \
                  \nRemove removes students similarly to min_attempt_count). \
                  \nCut removes attempts beyond max attempt count'
    },
    'in_data_file': {
        'default': 'data/code-mooc-df.pkl',
        'type': str,
        'help': ' '
    }, 'out_data_file': {
        'default': 'data/new-dkt-data-file.csv',
        'type': str,
        'help': ' '
    }, 'in_format': {
        'default': 'pickle',
        'choices': ['pickle_dataframe', 'csv', 'hdf_dataframe', 'asc'],
        'type': str,
        'help': '"hdf" assumes only one dataframe is saved in the file \
                 \n"asc" is a file format where row triplets contain data per student: \
                 \n #1: number of attempts \
                 \n #2: skill_ids \
                 \n #3: correctnesses'
    },
    'out_format': {
        'default': 'csv',
        'type': str,
        'choices': ['pickle_dataframe', 'csv', 'hdf_dataframe', 'asc'],
    },
    'skill_column': {
        'default': 'skill_id',
        'type': str,
    },
    'correct_column': {
        'default': 'correct',
        'type': str,
    },
    'user_column': {
        'default': 'user_id',
        'type': str,
    },
    'clean': {
        'default': 0,
        'type': int,
        'help': 'Set to 1 to clean data. Cleaning catgegorizes skill ids and turns correctnesses into binary variables. \
                 Maximum correctness value per skill id is considered as correct for correctness binarization.'
    },
    'is_grouped': {
        'default': 0,
        'type': int,
        'help': 'Set to 1 if data is grouped into student attempts. This is redundant for "asc" format as it is always grouped.'
    },
    'group_data': {
        'default': 0,
        'type': int,
        'help': 'Set to 1 to group ungrouped data into student sequences. \
                 \nThis will have no effect for grouped data.'
    }
}
