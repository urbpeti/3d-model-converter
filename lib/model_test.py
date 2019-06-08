from unittest import TestCase

from lib.model import Model


class ModelTest(TestCase):
    def test_get_triangles_return_trianlge_when_it_is_one_triangle(self):
        model = Model(
            vertices=[
                [0.0, 2.0, 2.0],
                [0.0, 0.0, 0.0],
                [2.0, 0.0, 0.0],
                [2.0, 2.0, 0.0],
            ],
            faces=[
                [1, 2, 3],
                [2, 1, 3],
            ]
        )

        expected_triangles = [
            [
                [0.0, 0.0, 0.0],
                [0.0, 2.0, 2.0],
                [0.0, 0.0, 0.0],
                [2.0, 0.0, 0.0],
            ],
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 2.0, 2.0],
                [2.0, 0.0, 0.0],
            ]
        ]

        triangles = model.get_triangles()

        self.assertEqual(str(triangles), str(expected_triangles))

    def test_get_triangles_return_fan_triangles(self):
        model = Model(
            vertices=[
                [0.0, 2.0, 2.0],
                [0.0, 0.0, 0.0],
                [2.0, 0.0, 0.0],
                [2.0, 2.0, 0.0],
            ],
            faces=[
                [1, 2, 3, 4],
            ]
        )

        expected_triangles = [
            [
                [0.0, 0.0, 0.0],
                [0.0, 2.0, 2.0],
                [0.0, 0.0, 0.0],
                [2.0, 0.0, 0.0],
            ],
            [
                [0.0, 0.0, 0.0],
                [0.0, 2.0, 2.0],
                [2.0, 0.0, 0.0],
                [2.0, 2.0, 0.0],
            ]
        ]

        triangles = model.get_triangles()

        self.assertEqual(str(triangles), str(expected_triangles))
