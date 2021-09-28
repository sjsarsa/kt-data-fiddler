import pandas as pd

from src.util import ungroup_data


def read_csv(filepath, usecols=None):
    return pd.read_csv(filepath, encoding='latin', low_memory=False, usecols=usecols)


def read_tsv(filepath, usecols=None):
    return pd.read_csv(filepath, encoding='latin', low_memory=False, sep='\t', usecols=usecols)


def read_asc(filepath, student_column, skill_column, correct_column):
    line = 0
    all_skill_ids = []
    all_corrects = []

    with open(filepath, 'r') as f:

        def next_line(may_be_none=True):
            if may_be_none:
                return f.readline()
            next_line = f.readline()
            if not next_line or len(next_line.strip()) == 0:
                raise Exception("Error: files line count should be divisible by three")
            return next_line

        while True:
            # First line of a triplet contains number of attempts
            student_attempt_count = next_line(may_be_none=True)

            # If there is not first line of triple, we have reached the end of file
            if not student_attempt_count:
                break

            student_attempt_count = int(student_attempt_count.strip())
            student_skill_ids = next_line(may_be_none=False).strip().split(',')
            student_corrects = next_line(may_be_none=False).strip().split(',')

            assert student_attempt_count == len(student_skill_ids) and student_attempt_count == len(student_corrects), \
                """
                Error reading student line triplet starting from line {}: mismatching counts.
                Student attempt count: {}
                Number of skill ids: {}
                Number of correctnesses: {}
                """.format(line, student_attempt_count, len(student_skill_ids), len(student_corrects))

            all_skill_ids.append(student_skill_ids)
            all_corrects.append(student_corrects)
            line += 3
    grouped = pd.DataFrame({skill_column: all_skill_ids, correct_column: all_corrects})
    grouped[student_column] = grouped.index.to_series().apply(lambda x: [x] * len(grouped[correct_column][x]))
    ungrouped = ungroup_data(grouped)
    return ungrouped.applymap(int)


read_func_map = {
    'asc': read_asc,
    'pickle': pd.read_pickle,
    'hdf': pd.read_hdf,
    'csv': read_csv
}


def read_results(filepath, format='csv', usecols=None):
    print('Reading data...')
    assert format != 'asc', 'asc format is supported only for conversion'
    return read_func_map[format](filepath, usecols=usecols)


def read_kt_data(filepath, format='csv', student_column='user_id', skill_column='skill_id', correct_column='correct'):
    print('Reading data...')
    if format == 'asc':
        return read_asc(filepath, student_column, skill_column, correct_column)
    return read_func_map[format](filepath)
