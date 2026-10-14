import math
from pathlib import Path


def parse_obj(text):
    vertices,faces = [],[]
    for number,line in enumerate(text.splitlines(),1):
        parts = line.split('#',1)[0].split()
        if not parts: continue
        if parts[0]=='v':
            if len(parts)<4:
                raise ValueError(f'Line {number}: vertex needs x, y, z.')
            xyz = tuple(float(value) for value in parts[1:4])
            if not all(math.isfinite(value) and abs(value)<=1e12 for value in xyz):
                raise ValueError('Vertex coordinates must be finite and within ±1e12.')
            vertices.append(xyz)
            if len(vertices)>10000: raise ValueError('At most 10,000 vertices supported.')
        elif parts[0]=='f':
            if len(parts)<4: raise ValueError(f'Line {number}: face needs at least three vertices.')
            indices = []
            for part in parts[1:]:
                index = int(part.split('/')[0])
                if index==0: raise ValueError('OBJ indices start at one.')
                index = index-1 if index>0 else len(vertices)+index
                if not 0<=index<len(vertices): raise ValueError(f'Line {number}: invalid vertex reference.')
                indices.append(index)
            faces.append(indices)
            if len(faces)>20000: raise ValueError('At most 20,000 faces supported.')
    if not vertices or not faces:
        raise ValueError('Model must contain vertices and polygon faces.')
    edges = set()
    for face in faces:
        for a,b in zip(face,face[1:]+face[:1]):
            if a!=b: edges.add(tuple(sorted((a,b))))
    return vertices,sorted(edges)


def load_obj(path):
    path = Path(path)
    if path.stat().st_size>10*1024*1024: raise ValueError('OBJ file must be under 10 MB.')
    return parse_obj(path.read_text(encoding='utf-8'))


def normalize(vertices):
    low = [min(vertex[i] for vertex in vertices) for i in range(3)]
    high = [max(vertex[i] for vertex in vertices) for i in range(3)]
    centre = [(a+b)/2 for a,b in zip(low,high)]
    scale = max(b-a for a,b in zip(low,high)) or 1
    return [tuple((vertex[i]-centre[i])*2/scale for i in range(3)) for vertex in vertices]


def project(vertices,yaw=0,pitch=0,zoom=1,width=800,height=600):
    yaw,pitch = math.radians(yaw),math.radians(pitch)
    result = []
    scale = min(width,height)*.32*zoom
    for x,y,z in vertices:
        x,z = x*math.cos(yaw)+z*math.sin(yaw),-x*math.sin(yaw)+z*math.cos(yaw)
        y,z = y*math.cos(pitch)-z*math.sin(pitch),y*math.sin(pitch)+z*math.cos(pitch)
        result.append((width/2+x*scale,height/2-y*scale))
    return result
