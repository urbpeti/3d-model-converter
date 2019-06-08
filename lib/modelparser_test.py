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

        self._parsing_strategy_mock.parse.assert_called_once_with(path)

    def test_parse_should_return_with_parser_strategy_returns(self):
        expectedModel = Model([], [])
        self._parsing_strategy_mock.parse.return_value = expectedModel

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

        expected_vertices = [
            [0.0, 2.0, 2.0],
            [0.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [2.0, 2.0, 0.0],
        ]
        expected_faces = [
            [[1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 0]],
        ]

        self.assertEqual(str(model._vertices), str(expected_vertices))
        self.assertEqual(model._faces, expected_faces)

    def test_parse_should_parse_normals(self):
        test_data = """vn 1.000000 0.000000 0.000000
vn 0.000000 2.000000 0.000000
"""
        model = None
        with patch('lib.modelparser.open', mock_open(read_data=test_data)):
            model = self._strategy.parse('test')

        expected_normals = [
            [1.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
        ]

        self.assertEqual(str(model._normals), str(expected_normals))

    def test_parse_should_parse_faces(self):
        test_data = """v 0.000000 2.000000 2.000000
vt 1.000000 0.000000 0.000000
vn 1.000000 0.000000 0.000000
f 1 1 1 
f 1//1 1//1 1//1 1//1
f 1/1 1/1 1/1 1/1
"""
        model = None
        with patch('lib.modelparser.open', mock_open(read_data=test_data)):
            model = self._strategy.parse('test')

        expected_faces = [
            [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
            [[1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1]],
            [[1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0]],
        ]

        self.assertEqual(model._faces, expected_faces)

    def test_parse_should_parse_faces_with_negative_indexes(self):
        test_data = """v 1.000000 0.000000 0.000000
vt 0.000000 2.000000 0.000000
vn 0.000000 0.000000 3.000000
f -1/-1/-1 -1/-1/-1 -1/-1/-1 
v 4.000000 0.000000 0.000000
vt 0.000000 5.000000 0.000000
vn 0.000000 0.000000 6.000000
f -1/-1/-1 -1/-1/-1 -1/-1/-1
"""
        model = None
        with patch('lib.modelparser.open', mock_open(read_data=test_data)):
            model = self._strategy.parse('test')

        expected_faces = [
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
        ]

        self.assertEqual(model._faces, expected_faces)

    def test_parse_should_parse_textures(self):
        test_data = """vt 0.000000 2.000000 2.000000
vt 0.000000 0.000000 0.000000
"""
        model = None
        with patch('lib.modelparser.open', mock_open(read_data=test_data)):
            model = self._strategy.parse('test')

        expected_textures = [
            [0.0, 2.0, 2.0],
            [0.0, 0.0, 0.0],
        ]

        self.assertEqual(str(model._textures), str(expected_textures))

    def test_parse_should_skip_lines_with_undefinied_startings(self):
        test_data = "aaaa\nv 0.0 2.0 2.0"
        model = None
        with patch('lib.modelparser.open', mock_open(read_data=test_data)):
            model = self._strategy.parse('test')

        expected_vertices = [
            [0.0, 2.0, 2.0],
        ]
        expected_faces = []

        self.assertEqual(str(model._vertices), str(expected_vertices))
        self.assertEqual(model._faces, expected_faces)
