from unittest import TestCase
from unittest.mock import MagicMock

from lib.modelwriter import ModelWriter
from lib.model import Model


class WriterTest(TestCase):
    def setUp(self):
        self._writing_strategy_mock = MagicMock()
        self._writer = ModelWriter(self._writing_strategy_mock)

    def test_parse_should_call_given_parser_strategy(self):
        path = 'dummy/path'
        model = Model([], [])
        self._writer.write(path, model)

        self._writing_strategy_mock.assert_called_once_with(path, model)
