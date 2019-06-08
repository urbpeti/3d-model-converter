from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

from lib.modelparser import Parser, ObjParsingStrategy
from lib.model import Model


class ParserTest(TestCase):
    def setUp(self):
        self._parsing_strategy_mock = MagicMock()
        self._parser = Parser(self._parsing_strategy_mock)

    def test_parse_should_call_given_parser_strategy(self):
        path = 'dummy/path'
        self._parser.parse(path)

        self._parsing_strategy_mock.assert_called_once_with(path)

    def test_parse_should_return_with_parser_strategy_returns(self):
        expectedModel = Model([], [])
        self._parsing_strategy_mock.return_value = expectedModel

        path = 'dummy/path'
        model = self._parser.parse(path)

        self.assertEqual(model, expectedModel)


class ObjParsingStrategyTest(TestCase):
    def setUp(self):
        self._strategy = ObjParsingStrategy()

    def test_parse_should_open_the_right_file(self):
        with patch('lib.modelparser.open', mock_open(read_data='')) as file:
            self._strategy.parse('test')
            file.assert_called_once_with('test', 'r')

    def test_parse_should_return_model(self):
        test_data = """v 0.000000 2.000000 2.000000
v 0.000000 0.000000 0.000000
v 2.000000 0.000000 0.000000
v 2.000000 2.000000 0.000000
f 1 2 3 4
"""
        model = None
        with patch('lib.modelparser.open', mock_open(read_data=test_data)):
            model = self._strategy.parse('test')

        expected_vectors = [
            [0.0, 2.0, 2.0],
            [0.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [2.0, 2.0, 0.0],
        ]
        expected_faces = [
            [1, 2, 3, 4],
        ]

        self.assertEqual(str(model._vectors), str(expected_vectors))
        self.assertEqual(model._faces, expected_faces)

    def test_parse_should_skip_lines_with_undefinied_startings(self):
        test_data = "aaaa\nv 0.0 2.0 2.0"
        model = None
        with patch('lib.modelparser.open', mock_open(read_data=test_data)):
            model = self._strategy.parse('test')

        expected_vectors = [
            [0.0, 2.0, 2.0],
        ]
        expected_faces = []

        self.assertEqual(str(model._vectors), str(expected_vectors))
        self.assertEqual(model._faces, expected_faces)
