from numpy import inf

args_map = {
    'show_statistics': {
        'default': 'txt',
        'type': str,
        'choices': ['txt', 'tex', 'csv', 'json']
    },
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
    'in_format': {
        'default': 'csv',
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
        'choices': ['pickle_dataframe', 'csv', 'tsv', 'hdf_dataframe', 'asc', 'yudelson_bkt'],
    },
    'in_header': {
        'default': False,
        'action': 'store_true',
        'help': 'For csv and tsv: whether the input file contains a header or not.'
    },
    'out_header': {
        'default': False,
        'action': 'store_true',
        'help': 'For csv and tsv: whether to include header in outpute file.'
    },
    'skill_col': {
        'default': 'skill_id',
        'type': str,
    },
    'exercise_col': {
        'default': None,
        'type': str,
    },
    'correct_col': {
        'default': 'correct',
        'type': str,
    },
    'user_col': {
        'default': 'user_id',
        'type': str,
    },
    'clean': {
        'default': False,
        'action': 'store_true',
        'help': 'Whether to clean data. Cleaning categorizes skill ids and turns correctnesses into binary variables. \
                 Maximum correctness value per skill id is considered as correct for correctness binarization.'
    },
    'is_grouped': {
        'default': False,
        'action': 'store_true',
        'help': 'Whether data is grouped into student attempts. This is redundant for "asc" format as it is always grouped.'
    },
    'group_data': {
        'default': False,
        'action': 'store_true',
        'help': 'Whether to group ungrouped data into student sequences. \
                 \nThis will have no effect for grouped data.'
    },
    'test_rate': {
        'default': 0.,
        'type': float,
        'help': 'Provide a test data rate value between 0 and 1 to create a train and test split. \
                \nCreates two additional files named out_data_file.train and out_data_file.test'
    },
    'validation_rate': {
        'default': 0.,
        'type': float,
        'help': 'Provide a validation rate value between 0 and 1 to create a validation split in addition to train and test split. \
                \nSplits test set further into validation and test set and creates out_data_file.val'
    },
    'kfold': {
        'default': 0,
        'type': int,
        'help': 'Integer above 1 will generate a k-fold split of train and test files'
    },
    'shuffle': {
        'default': False,
        'type': bool,
        'action': 'store_true',
        'help': 'Whether to shuffle data'
    }
}
