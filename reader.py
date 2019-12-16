import pandas as pd
from utils import group_data, ungroup_data


def read_csv(filepath):
    return pd.read_csv(filepath, encoding='latin', low_memory=False)


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

    ungrouped = ungroup_data(pd.DataFrame({skill_column: all_skill_ids, correct_column: all_corrects}))
    ungrouped[student_column] = ungrouped.index.to_series()
    return ungrouped


read_func_map = {
    'asc': read_asc,
    'pickle': pd.read_pickle,
    'hdf': pd.read_hdf,
    'csv': read_csv
}


def read(filepath, format='csv', student_column='user_id', skill_column='skill_id', correct_column='correct'):
    if format == 'asc':
        return read_asc(filepath, student_column, skill_column, correct_column)
    return read_func_map[format](filepath)
