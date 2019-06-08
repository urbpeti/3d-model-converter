from struct import pack


class ModelWriter:
    def __init__(self, model_writing_strategy):
        self._write_strategy = model_writing_strategy

    def write(self, path, model):
        self._write_strategy.write(path, model)


class STLWritingStrategy:
    def write(self, path, model):
        triangles = model.get_triangles()
        with open(path, 'wb') as file:
            self._write_header(file)
            self._write_triangle_count(file, triangles)
            self._write_triangles(file, triangles)

    def _write_header(self, file):
        header = b'-' * 80
        file.write(header)

    def _write_triangle_count(self, file, triangles):
        file.write(pack('<I', len(triangles)))

    def _write_triangles(self, file, triangles):
        for triangle in triangles:
            file.write(self._triangle_to_bytes(triangle))

    def _triangle_to_bytes(self, triangle):
        triangles_bytes = b''
        for vector in triangle:
            triangles_bytes += self._vector_to_bytes(vector)

        attr_byte_count = b'\x00\x00'
        triangles_bytes += attr_byte_count

        return triangles_bytes

    def _vector_to_bytes(self, vector):
        vector_bytes = b''
        for coord in vector:
            vector_bytes += pack('<f', coord)

        return vector_bytes
