import utils
from utils import group_data


def to_asc(data, filepath, student_col, skill_col, correct_col):
    grouped_data = group_data(data.applymap(str), student_col)
    with open(filepath, 'w') as f:
        for skill_ids, corrects in zip(grouped_data[skill_col], grouped_data[correct_col]):
            assert len(skill_ids) == len(corrects), "Skill id and correct sequence lengths do not match: {} != {}" \
                .format(len(skill_ids), len(corrects))
            n_attempts = len(skill_ids)
            f.write(str(n_attempts) + '\n')
            f.write(','.join(skill_ids) + '\n')
            f.write(','.join(corrects) + '\n')


def write(data, filepath, format='csv', student_col='user_id', skill_col='skill_id', correct_col='correct', exercise_col=None):
    utils.validate_file_suffix(filepath, format=format)
    if format == 'csv':
        data.to_csv(filepath, index=False)
    elif format == 'tsv':
        data.to_csv(filepath, index=False, sep='\t')
    elif format == 'hdf':
        data.to_hdf(filepath)
    elif format == 'pickle':
        data.to_pickle(filepath)
    elif format == 'asc':
        to_asc(data, filepath, student_col, skill_col, correct_col)
    elif format == 'yudelson_bkt':
        to_yudelson_bkt(data, filepath, student_col, skill_col, correct_col, exercise_col)
    else:
        raise NotImplementedError("Provided output format {} is not supported".format(format))


def to_yudelson_bkt(data, filepath, student_col, skill_col, correct_col, exercise_col):
    if exercise_col == skill_col:
        skill_col = exercise_col + '-is-actually-exercise'
        data[skill_col] = data[exercise_col]
    data = data[[correct_col, student_col, exercise_col, skill_col]]
    print('Cleaning data...')
    data = utils.clean_data(data.dropna(), skill_col, correct_col)
    data[correct_col] = -(data[correct_col] - 1) + 1
    data[exercise_col] = 'exercise' + data[exercise_col].astype(str)
    data[skill_col] = 'skill' + data[skill_col].astype(str)
    data[student_col] = 'student' + data[student_col].astype(str)
    data.to_csv(filepath, index=False, sep='\t', header=False)
