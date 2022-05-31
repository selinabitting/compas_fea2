from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gmsh
import sys
import itertools


def compas_to_gmsh_2d(mesh, lc=100, write_path=None, inspect=False):
    gmsh.initialize(sys.argv)
    gmsh.model.add("mesh")

    for v in mesh.vertices():
        gmsh.model.geo.addPoint(*mesh.vertex_coordinates(v), lc, v)

    # Generate elements between nodes
    key_index = mesh.key_index()
    faces = [[key_index[key]
              for key in mesh.face_vertices(face)] for face in mesh.faces()]

    c = 1
    for n, f in enumerate(faces):
        n = n+1
        for i in range(len(f)):
            p1 = f[i]
            p2 = f[(i + 1) % len(f)]
            gmsh.model.geo.addLine(p1, p2, c)
            c += 1
        gmsh.model.geo.addCurveLoop([c-4, c-3, c-2, c-1], n)
        # gmsh.model.geo.addPlaneSurface([n], n)
        gmsh.model.geo.addSurfaceFilling([n], n)
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.refine()
    gmsh.model.mesh.generate(2)
    if inspect:
        gmsh.fltk.run()
    if write_path:
        gmsh.write("{}/t1.stl".format(write_path))
    return gmsh.model


def compas_to_gmsh_3d(mesh, lc, write_path=None, inspect=False, kernel='occ', refine=False, planar=True, hex_mesh=False, verbose=False):

    gmsh.initialize(sys.argv)
    gmsh.model.add("block")
    gmsh.option.set_number("General.Terminal", int(verbose))

    factory = gmsh.model.occ if kernel == 'occ' else gmsh.model.geo

    # Add nodes
    nodes = [list(vertex.values()) for vertex in mesh.vertex.values()]
    for node in nodes:
        factory.addPoint(*node, lc)

    # Add lines
    faces = [face for face in mesh.face.values()]
    face_edges = {f: [(face[i-1], face[i]) for i in range(len(face))] for f, face in enumerate(faces)}
    edges = list(itertools.chain.from_iterable(face_edges.values()))
    for edge in edges:
        e = (edge[1], edge[0])
        if e in edges:
            edges.remove(e)

    lines = [factory.addLine(edge[1]+1, edge[0]+1) for edge in edges]

    # Add surfaces
    surfs = []
    for f, face_edges in face_edges.items():
        cloop = []
        for e in face_edges:
            if e in edges:
                cloop.append(edges.index(e)+1)
            else:
                cloop.append(-(edges.index((e[1], e[0]))+1))
        cl = factory.addCurveLoop(cloop)
        # if hex_mesh:
        #     for tag in cloop:
        #         factory.mesh.setTransfiniteCurve(tag, 5)
        # surfs.append(factory.addPlaneSurface([cl]))
        if kernel == 'geo':
            cl = [cl]
        surfs.append(factory.add_surface_filling(cl))
        # surfs.append(factory.addPlaneSurface(cl) if planar else factory.add_surface_filling(cl))

    sloop = factory.addSurfaceLoop(surfs)
    # if hex_mesh:
    #     factory.mesh.setTransfiniteSurface(tag)
    #     factory.mesh.setRecombine(2, tag)

    # Add volumes
    vol = factory.addVolume([sloop])

    factory.synchronize()
    gmsh.model.addPhysicalGroup(3, [1])
    gmsh.model.setPhysicalName(3, 1, "block")

    gmsh.option.setNumber('Mesh.Algorithm3D', 1)
    # gmsh.option.setNumber('Mesh.MeshSizeMax', lc*1.5)
    # gmsh.option.setNumber('Mesh.MeshSizeMin', lc*0.5)

    if hex_mesh:
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 2)
        gmsh.option.setNumber("Mesh.RecombineAll", 2)
        gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 1)

    factory.synchronize()
    gmsh.model.mesh.generate(gmsh.model.get_dimension())
    if refine:
        gmsh.model.mesh.refine()
        factory.synchronize()

    if inspect:
        gmsh.fltk.run()
    if write_path:
        gmsh.write("{}/block.stl".format(write_path))
        gmsh.finalize()
    return gmsh.model

# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

# from compas.geometry import add_vectors
# from compas.geometry import centroid_points
# from compas.geometry import cross_vectors
# from compas.geometry import length_vector
# from compas.geometry import normalize_vector
# from compas.geometry import scale_vector
# from compas.geometry import subtract_vectors

# try:
#     from numpy import array
#     from numpy import arctan2
#     from numpy import cos
#     from numpy import dot
#     from numpy import newaxis
#     from numpy import pi
#     from numpy import sin
#     from numpy.linalg import inv
# except:
#     pass

# try:
#     from meshpy.tet import MeshInfo
#     from meshpy.tet import build
#     from meshpy.triangle import MeshInfo as MeshInfo_tri
#     from meshpy.triangle import build as build_tri
# except:
#     pass


# # Author(s): Andrew Liew (github.com/andrewliew)


# __all__ = [
#     'discretise_faces',
#     'extrude_mesh',
#     'tets_from_vertices_faces',
# ]


# def extrude_mesh(structure, mesh, layers, thickness, mesh_name, links_name, blocks_name):

#     """ Extrudes a Mesh and adds elements to a Structure.

#     Parameters
#     ----------
#     structure : obj
#         Structure object to update.
#     mesh : obj
#         Mesh datastructure
#     layers : int
#         Number of layers.
#     thickness : float
#         Layer thickness.
#     mesh_name : str
#         Name of set for mesh on final surface.
#     links_name : str
#         Name of set for adding links along extrusion.
#     blocks_name : str
#         Name of set for solid elements.

#     Returns
#     -------
#     None

#     Notes
#     -----
#     - Extrusion is along the Mesh vertex normals.

#     """

#     ki     = {}
#     faces  = []
#     links  = []
#     blocks = []
#     slices = {i: [] for i in range(layers)}

#     for key in mesh.vertices():

#         normal = normalize_vector(mesh.vertex_normal(key))
#         xyz    = mesh.vertex_coordinates(key)
#         ki['{0}_0'.format(key)] = structure.add_node(xyz)

#         for i in range(layers):

#             xyzi = add_vectors(xyz, scale_vector(normal, (i + 1) * thickness))
#             ki['{0}_{1}'.format(key, i + 1)] = structure.add_node(xyzi)

#             if links_name:

#                 node1 = ki['{0}_{1}'.format(key, i + 0)]
#                 node2 = ki['{0}_{1}'.format(key, i + 1)]
#                 L  = subtract_vectors(xyzi, xyz)
#                 ez = normalize_vector(L)
#                 try:
#                     ey = cross_vectors(ez, [1, 0, 0])
#                 except:
#                     pass
#                 axes = {'ez': ez, 'ey': ey}

#                 ekey = structure.add_element(nodes=[node1, node2], type='SpringElement', thermal=False, axes=axes)
#                 structure.elements[ekey].A = mesh.vertex_area(key)
#                 structure.elements[ekey].L = L
#                 links.append(ekey)

#     for face in mesh.faces():

#         vs = mesh.face_vertices(face)

#         for i in range(layers):

#             bot = ['{0}_{1}'.format(j, i + 0) for j in vs]
#             top = ['{0}_{1}'.format(j, i + 1) for j in vs]

#             if blocks_name:

#                 eltype  = 'PentahedronElement' if len(vs) == 3 else 'HexahedronElement'
#                 nodes  = [ki[j] for j in bot + top]
#                 ekey   = structure.add_element(nodes=nodes, eltype=eltype, thermal=False)
#                 blocks.append(ekey)
#                 slices[i].append(ekey)

#             if (i == layers - 1) and mesh_name:
#                 nodes = [ki[j] for j in top]
#                 ekey = structure.add_element(nodes=nodes, type='ShellElement', acoustic=False, thermal=False)
#                 faces.append(ekey)

#     if blocks_name:
#         structure.add_set(name=blocks_name, type='element', selection=blocks)
#         for i in range(layers):
#             structure.add_set(name='{0}_layer_{1}'.format(blocks_name, i), type='element', selection=slices[i])

#     if mesh_name:
#         structure.add_set(name=mesh_name, type='element', selection=faces)

#     if links:
#         structure.add_set(name=links_name, type='element', selection=links)


# def discretise_faces(vertices, faces, target, min_angle=15, factor=3):

#     """ Make discretised triangles from input coarse triangles data.

#     Parameters
#     ----------
#     vertices : list
#         Co-ordinates of coarse vertices.
#     faces : list
#         Vertex indices of each face of the coarse triangles.
#     target : float
#         Target edge length of each triangle.
#     min_angle : float
#         Minimum internal angle of triangles.
#     factor : float
#         Factor on the maximum area of each triangle.

#     Returns
#     -------
#     list
#         Vertices of the discretised trianlges.
#     list
#         Vertex numbers of the discretised trianlges.

#     Notes
#     -----
#     - An experimental script.

#     """

#     points_all = []
#     faces_all  = []

#     Amax = factor * 0.5 * target**2

#     for count, face in enumerate(faces):

#         # Seed

#         face.append(face[0])

#         points = []
#         facets = []

#         for u, v in zip(face[:-1], face[1:]):
#             sp  = vertices[u]
#             ep  = vertices[v]
#             vec = subtract_vectors(ep, sp)
#             l   = length_vector(vec)
#             div = l / target
#             n   = max([1, int(div)])
#             for j in range(n):
#                 points.append(add_vectors(sp, scale_vector(vec, j / n)))
#         facets = [[i, i + 1] for i in range(len(points) - 1)]
#         facets.append([len(points) - 1, 0])

#         # Starting orientation

#         cent = centroid_points(points)
#         vec1 = subtract_vectors(points[1], points[0])
#         vec2 = subtract_vectors(cent, points[0])
#         vecn = cross_vectors(vec1, vec2)

#         # Rotate about x

#         points   = array(points).transpose()
#         phi      = -arctan2(vecn[2], vecn[1]) + 0.5 * pi
#         Rx       = array([[1, 0, 0], [0, cos(phi), -sin(phi)], [0, sin(phi), cos(phi)]])
#         vecn_x   = dot(Rx, array(vecn)[:, newaxis])
#         points_x = dot(Rx, points)
#         Rx_inv   = inv(Rx)

#         # Rotate about y

#         psi      = +arctan2(vecn_x[2, 0], vecn_x[0, 0]) - 0.5 * pi
#         Ry       = array([[cos(psi), 0, sin(psi)], [0, 1, 0], [-sin(psi), 0, cos(psi)]])
#         points_y = dot(Ry, points_x)
#         Ry_inv   = inv(Ry)

#         V = points_y.transpose()

#         try:

#             new_points = [list(i) for i in list(V[:, :2])]

#             info = MeshInfo_tri()
#             info.set_points(new_points)
#             info.set_facets(facets)

#             tris = build_tri(info, allow_boundary_steiner=False, min_angle=min_angle, max_volume=Amax)
#             new_points = [list(j) + [V[0, 2]] for j in tris.points]
#             new_tris   = [list(j) for j in tris.elements]

#             V = array(new_points)
#             points = dot(Ry_inv, V.transpose())
#             points_all.append([list(i) for i in list(dot(Rx_inv, points).transpose())])
#             faces_all.append(new_tris)

#         except:

#             print('***** ERROR discretising face {0} *****'.format(count))

#     return points_all, faces_all


# def tets_from_vertices_faces(vertices, faces, volume=None):

#     """ Generate tetrahedron points and elements with MeshPy (TetGen).

#     Parameters
#     ----------
#     vertices : list
#         List of lists of vertex co-ordinates for the input surface mesh.
#     faces : list
#         List of lists of face indices for the input surface mesh.
#     volume : float
#         Volume constraint for each tetrahedron element.

#     Returns
#     -------
#     list
#         Points of the tetrahedrons.
#     list
#         Indices of points for each tetrahedron element.

#     """

#     try:
#         info = MeshInfo()
#         info.set_points(vertices)
#         info.set_facets(faces)

#         tets     = build(info, max_volume=volume)
#         points   = [list(i) for i in list(tets.points)]
#         elements = [list(i) for i in list(tets.elements)]

#         return points, elements

#     except:

#         print('***** MeshPy failed *****')


# # ==============================================================================
# # Debugging
# # ==============================================================================

# if __name__ == "__main__":

#     pass
