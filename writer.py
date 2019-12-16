import pandas as pd
import os.path as osp
from utils import group_data, ungroup_data


def to_asc(data, filepath, student_column, skill_column, correct_column):
    grouped_data = group_data(data.applymap(str), student_column)
    with open(filepath, 'w') as f:
        for skill_ids, corrects in zip(grouped_data[skill_column], grouped_data[correct_column]):
            assert len(skill_ids) == len(corrects), "Skill id and correct sequence lengths do not match: {} != {}" \
                .format(len(skill_ids), len(corrects))
            n_attempts = len(skill_ids)
            f.write(str(n_attempts) + '\n')
            f.write(','.join(skill_ids) + '\n')
            f.write(','.join(corrects) + '\n')


format_suffix_map = {
    'csv': '.csv',
    'pickle': '.pkl',
    'hdf': '.hdf',
    'asc': '.asc'
}


def write(data, filepath, format='csv', student_column='user_id', skill_column='skill_id', correct_column='correct'):
    file_extension = osp.splitext(filepath)[-1]
    standard_extension = format_suffix_map[format]
    if file_extension != standard_extension:
        print('Warning: filepath extension {} does not match default format extension {}'.format(
            file_extension, standard_extension))
    if format == 'csv':
        data.to_csv(filepath, index=False)
    elif format == 'hdf':
        data.to_hdf(filepath)
    elif format == 'pickle':
        data.to_pickle(filepath)
    elif format == 'asc':
        to_asc(data, filepath, student_column, skill_column, correct_column)
    else:
        raise NotImplementedError("Provided output format {} is not supported".format(format))
