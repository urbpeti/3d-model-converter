class Model:
    def __init__(self, vertices=[], texture=[], normals=[], faces=[]):
        self._vertices = vertices
        self._texture = texture
        self._normals = normals
        self._faces = faces

    def get_triangles(self):
        triangles = []
        for face in self._faces:
            face_triangles = self._get_triangles_from_face(face)
            triangles.extend(face_triangles)
        return triangles

    def _subtitute_vertices(self, face):
        return [self._vertices[i - 1] for i in face]

    def _get_triangles_from_face(self, face):
        normal = [0.0] * 3
        face_with_vertices = self._subtitute_vertices(face)
        triangles = self._fan_triangulation(face_with_vertices)

        for triangle in triangles:
            triangle.insert(0, normal)

        return triangles

    def _fan_triangulation(self, face_vertices):
        triangles = []
        i = 2
        while i < len(face_vertices):
            triangle = [face_vertices[0],
                        face_vertices[i - 1], face_vertices[i]]
            triangles.append(triangle)
            i += 1

        return triangles
