import numpy as np
from stl import mesh

# Example array of triangles, each sub-array has 9 values (3 vertices per triangle)
triangles = np.array([
    [0, 0, 0,  1, 0, 0,  0, 1, 0],  # Triangle 1
    [1, 0, 0,  1, 1, 0,  0, 1, 0],  # Triangle 2
    [0, 0, 0,  0, 1, 0,  0, 0, 1],  # Triangle 3
    [1, 0, 0,  0, 0, 1,  1, 1, 0],  # Triangle 4
])

# Create an empty mesh with the same number of triangles
mesh_data = mesh.Mesh(np.zeros(triangles.shape[0], dtype=mesh.Mesh.dtype))

# Assign each triangle's vertices to the mesh
for i, triangle in enumerate(triangles):
    mesh_data.vectors[i] = [
        triangle[0:3],   # Vertex 1
        triangle[3:6],   # Vertex 2
        triangle[6:9]    # Vertex 3
    ]

# Save the mesh to an STL file
mesh_data.save('output_mesh.stl')

print("3D object saved as 'output_mesh.stl'")
