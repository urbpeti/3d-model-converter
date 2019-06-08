import re
from abc import ABC

from lib.model import Model


class Parser:
    def __init__(self, parsing_strategy):
        self._parsing_strategy = parsing_strategy

    def parse(self, path):
        return self._parsing_strategy.parse(path)


class ObjParsingStrategy:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.normals = []
        self.textures = []

    def parse(self, path):
        self.vertices = []
        self.faces = []
        self.normals = []
        self.textures = []
        with open(path, 'r') as file:
            for line in file.readlines():
                parts = line.strip().split(' ')
                dataType = parts[0]
                if dataType == 'v':
                    vertex = self._create_vertex_from_line_parts(parts)
                    self.vertices.append(vertex)
                elif dataType == 'vn':
                    normal = self._create_normal_from_line_parts(parts)
                    self.normals.append(normal)
                elif dataType == 'vt':
                    texture = self._create_texture_from_line_parts(parts)
                    self.textures.append(texture)
                elif dataType == 'f':
                    face = self._create_face_from_line_parts(parts)
                    self.faces.append(face)

        return Model(vertices=self.vertices, textures=self.textures, normals=self.normals, faces=self.faces)

    def _create_vertex_from_line_parts(self, parts):
        return [float(n) for n in parts[1:]]

    def _create_texture_from_line_parts(self, parts):
        return [float(n) for n in parts[1:]]

    def _create_normal_from_line_parts(self, parts):
        return [float(n) for n in parts[1:]]

    def _create_face_from_line_parts(self, parts):
        return [self._create_face_part(face_str) for face_str in parts[1:]]

    def _create_face_part(self, face_str):
        parts_str = face_str.split('/')
        parts = [0 if p == '' else int(p) for p in parts_str]
        while len(parts) < 3:
            parts = parts + [0]

        self._fix_negative_indices(parts)
        return parts

    def _fix_negative_indices(self, parts):
        if parts[0] < 0:
            parts[0] = len(self.vertices) + 1 + parts[0]
        if parts[1] < 0:
            parts[1] = len(self.vertices) + 1 + parts[1]
        if parts[2] < 0:
            parts[2] = len(self.vertices) + 1 + parts[2]
