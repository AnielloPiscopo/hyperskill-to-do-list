import unittest

from core.utils.logs import LogHelper


class LogHelperBuildPrefixTest(unittest.TestCase):

    def test_request_direction_format(self):
        prefix = LogHelper.build_prefix('users', 'RegisterView', 'POST', LogHelper.Direction.REQUEST)
        self.assertEqual(prefix, '[USERS]-[RegisterView]-[POST] - [REQUEST]')

    def test_response_direction_format(self):
        prefix = LogHelper.build_prefix('board', 'BoardListView', 'GET', LogHelper.Direction.RESPONSE)
        self.assertEqual(prefix, '[BOARD]-[BoardListView]-[GET] - [RESPONSE]')

    def test_app_name_is_uppercased(self):
        prefix = LogHelper.build_prefix('task', 'TaskDetailView', 'DELETE', LogHelper.Direction.REQUEST)
        self.assertIn('[TASK]-', prefix)

    def test_method_is_uppercased(self):
        prefix = LogHelper.build_prefix('task', 'TaskDetailView', 'patch', LogHelper.Direction.REQUEST)
        self.assertIn('-[PATCH]', prefix)

    def test_view_name_case_is_preserved(self):
        prefix = LogHelper.build_prefix('board', 'BoardArchiveView', 'POST', LogHelper.Direction.REQUEST)
        self.assertIn('-[BoardArchiveView]-', prefix)

    def test_direction_enum_values(self):
        self.assertEqual(LogHelper.Direction.REQUEST.value, 'REQUEST')
        self.assertEqual(LogHelper.Direction.RESPONSE.value, 'RESPONSE')