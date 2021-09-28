from numpy import inf
from argparse import ArgumentTypeError


class Args(object):
    def __init__(self, args_dict):
        for key, val in args_dict.items():
            self.__dict__[key] = val['default']


def parse_args(parser, arg_map):
    parser.add_argument('in_file')
    parser.add_argument('out_file', nargs='?')
    for key, val in {**common_args_map, **arg_map}.items():
        if val.get('action'):
            parser.add_argument('--' + key,
                                default=val.get('default'),
                                action=val.get('action'),
                                help=str(val.get('help') or '') + '(default: %(default)s)')
        else:
            parser.add_argument('--' + key,
                                default=val.get('default'),
                                nargs=val.get('nargs'),
                                help=str(val.get('help') or '') + '(default: %(default)s)',
                                choices=val.get('choices'),
                                type=val.get('type'))
    return parser.parse_args()


def positive_int(x):
    try:
        x = int(x)
    except ValueError:
        raise ArgumentTypeError(f"{x} not an integer literal")

    if x < 1:
        raise ArgumentTypeError(f"{x} is less than 1")
    return x


def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise ArgumentTypeError(f"{x} not a floating-point literal")

    if 0.0 > x > 1.0:
        raise ArgumentTypeError(f"{x} not in range [0.0, 1.0]")
    return x


common_args_map = {
    'in-format': {
        'default': 'csv',
        'choices': ['pickle', 'csv', 'hdf', 'asc'],
        'type': str,
        'help': 'pickle assumes a saved dataframe \
                 \n"hdf" assumes only one dataframe is saved in the file \
                 \n"asc" is a file format where row triplets contain data per student: \
                 \n #1: number of attempts \
                 \n #2: skill-ids \
                 \n #3: correctnesses'
    },
}

converter_args_map = {
    'stat-format': {
        'default': 'txt',
        'type': str,
        'choices': ['txt', 'tex', 'csv', 'json']
    },
    'min-attempt-count': {
        'default': 2,
        'type': positive_int,
        'help': 'Remove students with less than min attempt count attempts.'
    },
    'max-attempt-count': {
        'default': inf,
        'type': positive_int,
        'help': 'Apply maximum attempt count to filter or split attempt sequences'
    },
    'max-attempt-filter': {
        'default': 'split',
        'choices': ['split', 'remove', 'cut'],
        'type': str,
        'help': 'Determine how maximum attempt count is applied. \
                  \nSplit creates more data (implemented chiefly to test SAKT). \
                  \nRemove removes students similarly to min-attempt-count). \
                  \nCut removes attempts beyond max attempt count'
    },
    'out-format': {
        'default': 'csv',
        'type': str,
        'choices': ['pickle', 'csv', 'tsv', 'hdf', 'asc', 'yudelson-bkt'],
        'help': 'pickle and hdf will contain a compressed dataframe'
    },
    'in-header': {
        'default': False,
        'action': 'store_true',
        'help': 'For csv and tsv: whether the input file contains a header or not.'
    },
    'out-header': {
        'default': False,
        'action': 'store_true',
        'help': 'For csv and tsv: whether to include header in output file.'
    },
    'skill-col': {
        'default': 'skill_id',
        'type': str,
    },
    'exercise-col': {
        'default': None,
        'type': str,
    },
    'correct-col': {
        'default': 'correct',
        'type': str,
    },
    'user-col': {
        'default': 'user_id',
        'type': str,
    },
    'clean': {
        'default': False,
        'action': 'store_true',
        'help': 'Whether to clean data. Cleaning categorizes skill ids and turns correctnesses into binary variables. \
                 Maximum correctness value per skill id is considered as correct for correctness binarization.'
    },
    'group-data': {
        'default': False,
        'action': 'store_true',
        'help': 'Whether to group ungrouped data into student sequences. \
                 \nThis will have no effect for grouped data.'
    },
    'test-rate': {
        'default': None,
        'type': restricted_float,
        'help': 'Provide a test data rate value between 0 and 1 to create a train and test split. \
                \nCreates two additional files named out-data-file.train and out-data-file.test'
    },
    'validation-rate': {
        'default': None,
        'type': restricted_float,
        'help': 'Provide a validation rate value between 0 and 1 to create a validation split in addition to train and test split. \
                \nSplits test set further into validation and test set and creates out-data-file.val'
    },
    'kfold': {
        'default': None,
        'type': positive_int,
        'help': 'Integer above 1 will generate a k-fold split of train and test files'
    },
    'shuffle': {
        'default': False,
        'type': bool,
        'action': 'store_true',
        'help': 'Whether to shuffle data'
    },
}
