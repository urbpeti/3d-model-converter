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
                [[1, 0, 0], [2, 0, 0], [3, 0, 0]],
                [[2, 0, 0], [1, 0, 0], [3, 0, 0]],
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

    def test_get_triangles_return_trianlge_with_arg_normals(self):
        model = Model(
            vertices=[
                [0.0, 2.0, 2.0],
                [0.0, 0.0, 0.0],
                [2.0, 0.0, 0.0],
            ],
            normals=[
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
            ],
            faces=[
                [[1, 0, 1], [2, 0, 2], [3, 0, 2]],
                [[2, 0, 1], [1, 0, 1], [3, 0, 1]],
            ]
        )

        expected_triangles = [
            [
                [3.0, 4.0, 5.0],
                [0.0, 2.0, 2.0],
                [0.0, 0.0, 0.0],
                [2.0, 0.0, 0.0],
            ],
            [
                [1.0, 2.0, 3.0],
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
                [[1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 0]],
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
