"""
Util functions
currently mainly data manipulation TODO: maybe refactor as data utils
"""
import numpy as np
import pandas as pd
import os.path as osp


def filter_data(data, correct_column, min_attempt_count=5, max_attempt_count=None, max_filter_mode='split'):
    print("Filtering:")
    print("  min attempt count:", min_attempt_count)
    print("  max attempt count:", max_attempt_count)
    print("  max attempt filtering mode:", max_filter_mode)
    print('  number of students before applying filters: {}'.format(len(data)))
    # Remove student data with insufficient attempts
    attempt_counts = data[correct_column].apply(len)
    data = data[attempt_counts >= min_attempt_count]
    print(
        '  number of students after removing students with less than {} attempts: {}'.format(min_attempt_count,
                                                                                             len(data)))

    # Remove student data with high attempt count
    attempt_counts = data[correct_column].apply(len)
    if max_filter_mode == 'remove':
        data = data[attempt_counts <= max_attempt_count]
    elif max_filter_mode == 'cut':
        data = data.applymap(lambda x: x[:max_attempt_count])
    elif max_filter_mode == 'split':
        to_split = data[attempt_counts > max_attempt_count]
        while len(to_split) > 0:
            no_split = data[attempt_counts <= max_attempt_count]
            split = to_split.applymap(lambda x: x[:max_attempt_count])
            rest = to_split.applymap(lambda x: x[max_attempt_count:])
            data = pd.concat([no_split, split, rest]).reset_index(drop=True)
            attempt_counts = data[correct_column].apply(len)
            to_split = data[attempt_counts > max_attempt_count]

    print("  number of students after applying max attempt filter {}: {}".format(max_filter_mode, len(data)))
    return data.dropna().reset_index(drop=True)


def offset(ar, n=1):
    """
    >>> offset([1, 2, 3])
    [2, 3, nan]
    """
    return ar[n:] + [np.nan] * n


def add_next_attempts_columns(student_groups, skill_column, correct_column):
    # Create columns for skill ids and corrects at time t+1
    next_skill_column = 'next_' + skill_column
    next_correct_column = 'next_' + correct_column
    student_groups[next_skill_column] = student_groups[skill_column].apply(offset)
    student_groups[next_correct_column] = student_groups[correct_column].apply(offset)

    print('Grouped data columns:', end='\n  ')
    print(*student_groups.columns.values, sep='\n  ')

    # Remove final attempts because there are no next correctness targets
    for column in student_groups.columns:
        student_groups[column] = student_groups[column].apply(lambda x: x[:len(x) - 1])

    return student_groups, next_skill_column, next_correct_column


def group_data(data, student_column):
    """
    >>> group_data({'user_id': [0, 1, 1, 2], 'skill_id': [0, 1, 2, 3]}).to

    """
    assert_column_exists(data, student_column, 'User id')
    student_groups = pd.DataFrame(
        [data.groupby(student_column)[x].apply(list) for x in data.columns]).T.reset_index(drop=True)
    return student_groups


def ungroup_series(s):
    """
    >>> ungroup_series(pd.Series([[1, 2], [3, 4], [5, 6]])).tolist()
    [1, 2, 3, 4, 5, 6]
    """
    ungrouped = []
    for group in s:
        ungrouped += group
    return pd.Series(ungrouped)


def ungroup_data(data):
    return data.apply(ungroup_series)


def assert_column_exists(df, col, col_description=None):
    if col_description is not None:
        col_description += ' '
    assert col in df.columns, """
{}column "{}" not found in given data.
Found columns: {}.
Please specify which of the data columns is used for {}.
Run the command with argument --help for more information.
""".format(col_description, col, df.columns.values, col_description.lower())


def clean_data(data, skill_col, correct_col):
    assert_column_exists(data, skill_col, 'Skill')
    # Categorize skill ids
    data[skill_col] = data[skill_col].astype('category')
    data[skill_col].cat.categories = range(len(data[skill_col].cat.categories))
    assert_column_exists(data, correct_col, 'Exercise correctness')
    # Convert correctness to binary
    max_percentages_per_exercise = data.groupby([skill_col])[correct_col].max().to_dict()
    max_pass_percentage = data[skill_col].apply(lambda x: max_percentages_per_exercise[x])
    data[correct_col] = (data[correct_col] == max_pass_percentage).apply(int)
    return data


def validate_file_suffix(filepath, format):
    format_suffix_map = {
        'yudelson_bkt': '.tsv',
        'tsv': '.tsv',
        'csv': '.csv',
        'pickle': '.pkl',
        'hdf': '.hdf',
        'asc': '.asc'
    }

    file_extension = osp.splitext(filepath)[-1]
    standard_extension = format_suffix_map[format]
    if file_extension != standard_extension:
        print('Warning: filepath extension {} does not match default format extension {}'.format(
            file_extension, standard_extension))
        return False
    return True
