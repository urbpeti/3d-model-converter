class Model:
    def __init__(self, vectors, faces):
        self._vectors = vectors
        self._faces = faces

    def get_triangles(self):
        return [self._get_triangles_from_face(face) for face in self._faces]

    def _get_face_with_vectors(self, face):
        return [self._vectors[i - 1] for i in face]

    def _get_triangles_from_face(self, face):
        normal = [0.0] * 3
        triangle = self._get_face_with_vectors(face)
        triangle.insert(0, normal)
        return triangle
