import bpy
import bmesh
from collections import defaultdict, namedtuple
from typing import NamedTuple, Union, NewType, Type
import pprint

# typeing
UvIsland = list[dict[str, bmesh.types.BMFace]]
UvIndex = tuple[tuple, int]


def get_uv_islands(obj: bpy.types.Object):
    """オブジェクトのアクティブuvのアイランドを取得"""
    __face_to_verts = defaultdict(set)
    __vert_to_faces = defaultdict(set)

    def __parse_island(
        bm: bmesh.types.BMesh, face_idx: int, faces_left: set, island: UvIsland
    ):
        if face_idx in faces_left:
            faces_left.remove(face_idx)
            island.append({"face": bm.faces[face_idx]})
            for v in __face_to_verts[face_idx]:
                connected_faces = __vert_to_faces[v]
                if connected_faces:
                    for cf in connected_faces:
                        __parse_island(bm, cf, faces_left, island)

    def __get_island(bm: bmesh.types.BMesh):
        uv_island_lists: list[UvIsland] = []
        faces_left = set(__face_to_verts.keys())
        while len(faces_left) > 0:
            current_island: UvIsland = []
            face_idx = list(faces_left)[0]
            __parse_island(bm, face_idx, faces_left, current_island)
            uv_island_lists.append(current_island)
        return uv_island_lists

    obj = bpy.context.active_object
    bm = bmesh.new()
    bm.from_object(obj)
    # https://docs.blender.org/api/current/bmesh.types.html?highlight=bmesh%20verify#bmesh.types.BMLayerCollection.verify
    uv_layer: bmesh.types.BMLayerItem = bm.loops.layers.uv.verify()

    # selected_faces = [f for f in bm.faces if f.select]

    f: bmesh.types.BMFace
    for f in bm.faces:
        l: Union[bmesh.types.BMLayerAccessLoop, bmesh.types.BMLoop]
        for l in f.loops:
            _loop_uv: bmesh.types.BMLoopUV = l[uv_layer]
            # uv:mathutil.Vector
            # https://docs.blender.org/api/current/mathutils.html#mathutils.Vector.to_tuple
            id: UvIndex = (_loop_uv.uv.to_tuple(5), l.vert.index)
            __face_to_verts[f.index].add(id)
            __vert_to_faces[id].add(f.index)

    uv_island_lists = __get_island(bm)
    return uv_island_lists
