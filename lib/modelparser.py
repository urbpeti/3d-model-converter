import re
from abc import ABC

from lib.model import Model


class Parser:
    def __init__(self, parsing_strategy):
        self._parsing_strategy = parsing_strategy

    def parse(self, path):
        return self._parsing_strategy(path)


class ObjParsingStrategy:
    def parse(self, path):
        vectors = []
        faces = []
        with open(path, 'r') as file:
            for line in file.readlines():
                parts = line.strip().split(' ')
                dataType = parts[0]
                if dataType == 'v':
                    vector = self._create_vector_from_line_parts(parts)
                    vectors.append(vector)
                elif dataType == 'f':
                    face = self._create_face_from_line_parts(parts)
                    faces.append(face)

        return Model(vectors=vectors, faces=faces)

    def _create_vector_from_line_parts(self, parts):
        return [float(n) for n in parts[1:]]

    def _create_face_from_line_parts(self, parts):
        return [int(n) for n in parts[1:]]
