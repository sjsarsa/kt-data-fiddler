import argparse
import os
from os import path as osp

import conf
import reader
import utils
import writer


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

    utils.validate_file_suffix(args.out_data_file, format=args.out_format)
    if args.train_test_split > 0 and args.train_test_split < 1:
        if args.train_test_split > .5:
            print("Warning: train test split rate is above .5, this means test set will be larger than train test.")
        n_train = int(len(out_data) * (1 - args.train_test_split))

        train_out_file = args.out_data_file + '.train'
        writer.write(out_data.iloc[:n_train], train_out_file, args.out_format)
        print('Wrote', train_out_file)

        test_out_file = args.out_data_file + '.test'
        writer.write(out_data.iloc[n_train:], test_out_file, args.out_format)
        print('Wrote', test_out_file)
    else:
        writer.write(out_data, args.out_data_file, args.out_format)
        print('Wrote', args.out_data_file)


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
