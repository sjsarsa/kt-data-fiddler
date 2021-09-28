import argparse
from sklearn.model_selection import KFold

import pandas as pd
import arg_conf
from src import reader, util
from src import writer


def save_data(args, out_data):
    if args.test_rate is not None:
        # Write to train and test files
        save_to_train_test(out_data, args)
    if args.kfold is not None:
        # Write to kfold files train and test files
        save_to_kfold(out_data, args)
    if args.out_file is not None:
        # Write data to file
        writer.write(out_data, args.out_file, args.out_format, args.user_col, args.skill_col, args.correct_col,
                     args.exercise_col)
        print('Wrote', args.out_file)


def show_stats(data, format, student_col, exercise_col, skill_col, correct_col):
    def round_to_k(x):
        return f'{int(round(x, -3) / 1000)}'

    usecols = [student_col, skill_col, correct_col]
    if exercise_col != skill_col and exercise_col is not None:
        usecols.append(exercise_col)

    grouped = util.group_data(data[usecols].dropna(), student_col)
    stats_dict = {
        'Max attempts': grouped[student_col].apply(len).max(),
        'Students': len(grouped),
        'Records': round_to_k(len(data)),
        'Correct count': round_to_k(data[correct_col].sum()),
        'Exercise tags': len(data[exercise_col].unique()) if exercise_col is not None else len(data[skill_col].unique()),
        'Skill tags': len(data[skill_col].unique()) if exercise_col is not None and skill_col != exercise_col else '-'
    }

    stats = pd.DataFrame({k: [v] for k, v in stats_dict.items()})

    if format == 'json':
        stats_str = stats.to_json()
    elif format == 'txt':
        stats_str = stats.to_string(index=False)
    elif format == 'csv':
        stats_str = stats.to_csv(index=False)
    elif format == 'tex':
        stats_str = stats.to_latex(index=False)
    else:
        raise NotImplementedError(f'Statistics format {format} is not implemented.')

    print(stats_str)
    return stats_str


def fiddle(args):
    if args is None:
        args = arg_conf.Args(arg_conf.converter_args_map)

    in_data = reader.read_kt_data(args.in_file, args.in_format)

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
        out_data = util.clean_data(out_data, user_col=args.user_col, skill_col=args.skill_col, correct_col=args.correct_col)
    else:
        out_data = in_data

    if args.shuffle:
        grouped = util.group_data(out_data, args.user_col)
        out_data = util.ungroup_data(grouped.sample(frac=1).reset_index(drop=True))

    show_stats(out_data, args.stat_format, args.user_col, args.exercise_col, args.skill_col, args.correct_col)

    save_data(args, out_data)


def save_to_train_test(out_data, args):
    out_file = args.out_file or args.in_file
    if args.test_rate > .5:
        print("Warning: train test split rate is above .5, this means test set will be larger than train test.")
    n_test = int(len(out_data) * args.test_rate)
    test_out_file = out_file + '.test'
    writer.write(out_data.iloc[:n_test], test_out_file, args.out_format, args.user_col, args.skill_col,
                 args.correct_col, args.exercise_col)
    print('Wrote', test_out_file)

    n_valid = 0
    if args.validation_rate is not None and 0 < args.validation_rate < 1:
        n_valid = int(len(out_data) * args.validation_rate)
        validation_out_file = out_file + '.valid'
        writer.write(out_data.iloc[n_test:n_test + n_valid], validation_out_file, args.out_format, args.user_col,
                     args.skill_col, args.correct_col, args.exercise_col)
        print('Wrote', validation_out_file)

    train_out_file = out_file + '.train'
    writer.write(out_data.iloc[n_test + n_valid:], train_out_file, args.out_format, args.user_col, args.skill_col,
                 args.correct_col, args.exercise_col)
    print('Wrote', train_out_file)


def save_to_kfold(out_data, args):
    out_file = args.out_file or args.in_file
    kfold = KFold(n_splits=args.kfold, shuffle=args.shuffle)

    users = out_data[args.user_col].unique()

    for i, (train_i, test_i) in enumerate(kfold.split(users)):
        # Train-test split
        for split_name, split_index in [('train', train_i), ('test', test_i)]:
            filename = f'{out_file}.{split_name}.{i}'
            split_data = out_data[out_data[args.user_col].isin(users[split_index])].copy()
            writer.write(split_data, filename, args.out_format, args.user_col, args.skill_col,
                         args.correct_col, args.exercise_col)
            print('Wrote', filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Knowledge Tracing Data converter',
                                     formatter_class=argparse.RawTextHelpFormatter)
    args = arg_conf.parse_args(parser, arg_conf.converter_args_map)
    fiddle(args)
