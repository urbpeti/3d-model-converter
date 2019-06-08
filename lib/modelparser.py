import re
from abc import ABC

from lib.model import Model


class Parser:
    def __init__(self, parsing_strategy):
        self._parsing_strategy = parsing_strategy

    def parse(self, path):
        return self._parsing_strategy.parse(path)


class ObjParsingStrategy:
    def parse(self, path):
        vertices = []
        faces = []
        with open(path, 'r') as file:
            for line in file.readlines():
                parts = line.strip().split(' ')
                dataType = parts[0]
                if dataType == 'v':
                    vertex = self._create_vertex_from_line_parts(parts)
                    vertices.append(vertex)
                elif dataType == 'f':
                    face = self._create_face_from_line_parts(parts)
                    faces.append(face)

        return Model(vertices=vertices, faces=faces)

    def _create_vertex_from_line_parts(self, parts):
        return [float(n) for n in parts[1:]]

    def _create_face_from_line_parts(self, parts):
        return [int(n) for n in parts[1:]]
