import os
from os import path as osp

import reader


def init_ipython():
    """
    Ipython config

    Adds local dependencies to syspath
    """

    # Set work dir as parent folder of code-dkt
    home = os.environ['HOME']
    workdir = osp.join(home, 'tohtori/models/code-dkt/')
    os.chdir(workdir)

    import sys

    sys.path.append(workdir)


import argparse
import conf
import utils


class Args(object):
    def __init__(self, args_dict):
        for key, val in args_dict.items():
            self.__dict__[key] = val['default']


def run(args=None):
    if args is None:
        args = Args(conf.args_map)

    print('Reading data...')
    in_data = reader.read(args.in_data_file, args.in_format)

    use_cols = [args.user_column, args.correct_column, args.skill_column]

    if args.clean:
        print('Removing rows with nan values in columns {}, {} or {}...'.format(*use_cols))
        print('Data rows before dropping nan rows: {}'.format(len(in_data)))
        out_data = in_data[use_cols].dropna()
        print('Data rows after dropping nan rows: {}'.format(len(out_data)))
        print('Categorizing skill_column and ensuring correctness is a binary variable...')
        out_data = utils.clean_data(out_data, skill_column=args.skill_column, correct_column=args.correct_column)
    else:
        out_data = in_data
    utils.write(out_data, args.out_data_file, args.out_format)
    print('Wrote ', args.out_data_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parametrized knowledge tracing done simple, maybe',
                                     formatter_class=argparse.RawTextHelpFormatter)
    for key, val in conf.args_map.items():
        parser.add_argument('--' + key,
                            default=val.get('default'),
                            nargs=val.get('nargs'),
                            help=str(val.get('help') or '') + '(default: %(default)s)',
                            choices=val.get('choices'),
                            type=val.get('type'))

    args = parser.parse_args()
    run(args)
