import argparse
import os
from os import path as osp
from sklearn.model_selection import KFold

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
    in_data = reader.read(args.in_file, args.in_format)

    use_cols = [args.user_col, args.correct_col, args.skill_col]
    if args.exercise_col is not None:
        use_cols.append(args.exercise_col)

    if any([use_col not in in_data.columns for use_col in use_cols]):
        raise ValueError("""
Invalid columns provided: 
    skill col: {}
    correct col: {}
    user col: {}
    exercise col: {}
Found columns:
{}
""".format(args.skill_col, args.correct_col, args.user_col, args.exercise_col, ', '.join(in_data.columns.values)))

    if args.clean:
        print('Removing rows with nan values in columns {}, {} or {}...'.format(*use_cols))
        print('Data rows before dropping nan rows: {}'.format(len(in_data)))
        out_data = in_data[use_cols].dropna()
        print('Data rows after dropping nan rows: {}'.format(len(out_data)))
        print('Categorizing skill_column and ensuring correctness is a binary variable...')
        out_data = utils.clean_data(out_data, skill_col=args.skill_col, correct_col=args.correct_col)
    else:
        print('Data rows before dropping nan rows: {}'.format(len(in_data)))
        out_data = in_data
        print('Data rows after dropping nan rows: {}'.format(len(out_data)))

    if args.shuffle:
        grouped = utils.group_data(out_data, args.user_col)
        out_data = utils.ungroup_data(grouped.sample(frac=1).reset_index(drop=True))

    utils.validate_file_suffix(args.out_file, format=args.out_format)

    if args.test_rate > 0 and args.test_rate < 1:
        # Write to train and test files
        split_to_train_test(out_data, args)
    elif args.kfold > 1:
        # Write to kfold files train and test files
        split_to_kfold(out_data, args)
    else:
        # Write data to file
        writer.write(out_data, args.out_file, args.out_format, args.user_col, args.skill_col, args.correct_col,
                     args.exercise_col)
        print('Wrote', args.out_file)


def split_to_train_test(out_data, args):
    if args.test_rate > .5:
        print("Warning: train test split rate is above .5, this means test set will be larger than train test.")
    n_test = int(len(out_data) * args.test_rate)
    test_out_file = args.out_file + '.test'
    writer.write(out_data.iloc[:n_test], test_out_file, args.out_format, args.user_col, args.skill_col,
                 args.correct_col, args.exercise_col)
    print('Wrote', test_out_file)

    n_valid = 0
    if args.validation_rate > 0 and args.validation_rate < 1:
        n_valid = int(len(out_data) * args.validation_rate)
        validation_out_file = args.out_file + '.valid'
        writer.write(out_data.iloc[n_test:n_test + n_valid], validation_out_file, args.out_format, args.user_col,
                     args.skill_col, args.correct_col, args.exercise_col)
        print('Wrote', validation_out_file)

    train_out_file = args.out_file + '.train'
    writer.write(out_data.iloc[n_test + n_valid:], train_out_file, args.out_format, args.user_col, args.skill_col,
                 args.correct_col, args.exercise_col)
    print('Wrote', train_out_file)


def split_to_kfold(out_data, args):
    kfold = KFold(n_splits=args.kfold, shuffle=args.shuffle)

    for i, (train_i, test_i) in enumerate(kfold.split(out_data)):
        for set_name, set_index in [('train', train_i), ('test', test_i)]:
            filename = '{}.{}.{}'.format(args.out_file, set_name, i)
            writer.write(out_data.iloc[set_index], filename, args.out_format, args.user_col, args.skill_col,
                         args.correct_col, args.exercise_col)
            print('Wrote', filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parametrized knowledge tracing done simple, maybe',
                                     formatter_class=argparse.RawTextHelpFormatter)
    for key, val in conf.args_map.items():
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
    args = parser.parse_args()
    run(args)
