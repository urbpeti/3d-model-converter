from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

from lib.modelwriter import ModelWriter, STLWritingStrategy
from lib.model import Model


class WriterTest(TestCase):
    def setUp(self):
        self._writing_strategy_mock = MagicMock()
        self._writer = ModelWriter(self._writing_strategy_mock)

    def test_parse_should_call_given_parser_strategy(self):
        path = 'dummy/path'
        model = Model([], [])
        self._writer.write(path, model)

        self._writing_strategy_mock.write.assert_called_once_with(path, model)


class STLWritingTest(TestCase):
    def setUp(self):
        self._strategy = STLWritingStrategy()

    def test_write_should_open_file_to_write_bytes(self):
        with patch('lib.modelwriter.open', mock_open()) as file:
            self._strategy.write('test', MagicMock())
            file.assert_called_once_with('test', 'wb')

    def test_write_header(self):
        with patch('lib.modelwriter.open', mock_open()) as file:
            handle = file()
            header = b'-' * 80

            self._strategy.write('test', MagicMock())

            handle.write.assert_any_call(header)

    def test_write_triangle_count(self):
        with patch('lib.modelwriter.open', mock_open()) as file:
            handle = file()

            model = MagicMock()
            model.get_triangles.return_value = [
                [[1.0] * 3, [1.0] * 3, [1.0] * 3, [1.0] * 3],
            ]

            self._strategy.write('test', model)

            handle.write.assert_any_call(b'\x01\x00\x00\x00')

    def test_write_triangles(self):
        with patch('lib.modelwriter.open', mock_open()) as file:
            handle = file()

            model = MagicMock()
            model.get_triangles.return_value = [
                [[1.0] * 3, [2.0] * 3, [3.0] * 3, [4.0] * 3],
                [[3.0] * 3, [4.0] * 3, [1.0] * 3, [2.0] * 3],
            ]

            self._strategy.write('test', model)

            handle.write.assert_any_call(
                b'\x00\x00\x80?' * 3 +
                b'\x00\x00\x00@' * 3 +
                b'\x00\x00@@' * 3 +
                b'\x00\x00\x80@' * 3 +
                b'\x00\x00'
            )
            handle.write.assert_any_call(
                b'\x00\x00@@' * 3 +
                b'\x00\x00\x80@' * 3 +
                b'\x00\x00\x80?' * 3 +
                b'\x00\x00\x00@' * 3 +
                b'\x00\x00'
            )
