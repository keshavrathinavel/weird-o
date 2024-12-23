import numpy as np
from stl import mesh
import struct

class MeshDataStorage:
    def __init__(self, scale_factor=1000.0):
        self.scale_factor = scale_factor
        
    def text_to_coordinates(self, text):
        bytes_data = text.encode('utf-8')
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
            return bytes(bytes_data).decode('utf-8').rstrip('\x00')
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

if __name__ == "__main__":
    storage = MeshDataStorage()
    
    secret_message = "This is a secret message hidden in a 3D mesh!"
    storage.store_data(secret_message, 'secret_mesh.stl')
    
    retrieved_message = storage.retrieve_data('secret_mesh.stl')
    print(f"Retrieved message: {retrieved_message}")