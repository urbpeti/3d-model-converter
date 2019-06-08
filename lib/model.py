class Model:
    def __init__(self, vertices=[], textures=[], normals=[], faces=[]):
        self._vertices = vertices
        self._textures = textures
        self._normals = normals
        self._faces = faces

    def get_triangles(self):
        triangles = []
        for face in self._faces:
            face_triangles = self._get_triangles_from_face(face)
            triangles.extend(face_triangles)
        return triangles

    def _subtitute_vertices(self, face):
        return [[
            self._index_resolver(self._vertices, face_parts[0]),
            self._index_resolver(self._textures, face_parts[1]),
            self._index_resolver(self._normals, face_parts[2]),
        ] for face_parts in face]

    def _get_triangles_from_face(self, face):
        face_with_elements = self._subtitute_vertices(face)
        triangles = self._fan_triangulation(face_with_elements)

        return triangles

    def _fan_triangulation(self, face):
        vertices = [face_element[0] for face_element in face]
        normals = [face_element[2] for face_element in face]

        triangles = []
        i = 2
        while i < len(vertices):
            ns = [normals[0], normals[i-1], normals[i]]
            triangle = [
                self._avg_normal(ns),
                vertices[0],
                vertices[i - 1],
                vertices[i]
            ]
            triangles.append(triangle)
            i += 1

        return triangles

    def _index_resolver(self, elements, index):
        if index == 0:
            return [0.0, 0.0, 0.0]

        return elements[index - 1]

    def _avg_normal(self, normals):
        summa = [0] * len(normals[0])

        for normal in normals:
            summa = map(sum, zip(summa, normal))

        return [s / len(normals) for s in summa]
