import base64
from pathlib import Path

import numpy as np
from stl import mesh

STR_ENCODING_CODEC = "utf-8"


class MeshDataStorage:
    def __init__(self, scale_factor=1000.0):
        self.scale_factor = scale_factor

    def text_to_coordinates(self, text):
        bytes_data = text.encode(STR_ENCODING_CODEC)
        num_triangles = (len(bytes_data) + 8) // 9

        triangles = np.zeros((num_triangles, 9))

        for i, byte in enumerate(bytes_data):
            triangle_idx = i // 9
            coord_idx = i % 9
            triangles[triangle_idx][coord_idx] = byte / self.scale_factor

        return triangles

    def coordinates_to_text(self, triangles):
        coords = triangles.flatten()
        bytes_data = []

        for coord in coords:
            byte_val = round(coord * self.scale_factor)
            if 0 <= byte_val <= 255:
                bytes_data.append(byte_val)

        try:
            return bytes(bytes_data).decode(STR_ENCODING_CODEC).rstrip('\x00')
        except UnicodeDecodeError:
            return None

    def store_data(self, text, output_file):
        triangles = self.text_to_coordinates(text)

        mesh_data = mesh.Mesh(np.zeros(triangles.shape[0], dtype=mesh.Mesh.dtype))

        for i, triangle in enumerate(triangles):
            mesh_data.vectors[i] = [
                triangle[0:3],
                triangle[3:6],
                triangle[6:9]
            ]

        mesh_data.save(output_file)

    def retrieve_data(self, input_file):
        mesh_data = mesh.Mesh.from_file(input_file)

        triangles = mesh_data.vectors.reshape(-1, 9)

        return self.coordinates_to_text(triangles)


def mesh_image(image_file: str, mesh_file: str) -> None:
    storage = MeshDataStorage()
    encoded_string = base64.b64encode(Path(image_file).read_bytes()).decode(STR_ENCODING_CODEC)
    secret_message = encoded_string
    storage.store_data(secret_message, mesh_file)


def un_mesh_image(mesh_file: str, output_file: str, validate_image_path: str | None = None) -> None:
    storage = MeshDataStorage()
    output_file = Path(output_file)
    output_file.touch(exist_ok=True)
    retrieved_data = storage.retrieve_data(mesh_file)
    image_bytes_base64 = retrieved_data.encode(STR_ENCODING_CODEC)
    output_image_bytes = base64.b64decode(image_bytes_base64)
    output_file.write_bytes(output_image_bytes)

    if validate_image_path:
        validate_image = Path(validate_image_path)
        validate_image_bytes = validate_image.read_bytes()
        assert validate_image_bytes == output_image_bytes
