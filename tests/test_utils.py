from unittest import TestCase
from src import util

from shared_test_data import test_dataframes, grouped_test_dataframes


class UtilsTest(TestCase):
    def test_group_ungroup_does_not_change_data(self):
        for data in test_dataframes:
            grouped = util.group_data(data, 'user_id')
            ungrouped = util.ungroup_data(grouped)
            self.assertTrue(data.equals(ungrouped), """
Grouped and ungrouped data:
{}
should be the same as original data:
{}
            """.format(ungrouped, data))

    def test_ungroup_group_does_not_change_data(self):
        for data in grouped_test_dataframes:
            ungrouped = util.ungroup_data(data)
            grouped = util.group_data(ungrouped, 'user_id')
            self.assertTrue(data.equals(grouped), """
Ungrouped and grouped data:
{}
should be the same as original data:
{}
            """.format(grouped, data))
