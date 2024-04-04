import numpy as np

def load_obj(filename):
    vertices = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.split()

    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return vertices


vertices = load_obj('FINALMODEL.obj')
vertices_np = np.array(vertices)
print(vertices_np)