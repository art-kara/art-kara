#!/usr/bin/env python3
"""Render a tiny animated 3D builder with sunglasses. Requires numpy and Pillow.

Geometry, lighting, rotation, and the GIF are generated locally; no model assets
or external services are required. Run with the bundled workspace Python.
"""
from pathlib import Path
from math import sin, cos, pi
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
SIZE = 360
SCALE = 102
LIGHT = np.array([-0.5, 0.9, 1.0])
LIGHT /= np.linalg.norm(LIGHT)
SILVER = (204, 218, 230)
BLUE = (75, 139, 235)
DARK = (21, 32, 48)
GLINT = (165, 226, 250)


def sphere(center, radii, color, lat=8, lon=14):
    vertices = []
    for i in range(lat + 1):
        a = pi * i / lat
        for j in range(lon):
            b = 2 * pi * j / lon
            vertices.append(np.array(center) + np.array(radii) * [sin(a)*cos(b), cos(a), sin(a)*sin(b)])
    faces = []
    for i in range(lat):
        for j in range(lon):
            a = i*lon+j
            b = i*lon+(j+1)%lon
            c = (i+1)*lon+(j+1)%lon
            d = (i+1)*lon+j
            faces.extend([(a,b,c),(a,c,d)])
    return np.array(vertices), faces, color


def rounded_box(center, size, radius, color, steps=5):
    half = np.array(size) / 2
    inner = half - radius
    vertices, faces = [], []
    for axis in range(3):
        other = [a for a in range(3) if a != axis]
        for sign in (-1,1):
            start = len(vertices)
            for i in range(steps+1):
                for j in range(steps+1):
                    p = np.zeros(3)
                    p[axis] = sign*half[axis]
                    p[other[0]] = (2*i/steps-1)*half[other[0]]
                    p[other[1]] = (2*j/steps-1)*half[other[1]]
                    q = np.clip(p,-inner,inner)
                    delta = p-q
                    vertices.append(np.array(center)+q+radius*delta/np.linalg.norm(delta))
            for i in range(steps):
                for j in range(steps):
                    a = start+i*(steps+1)+j
                    b = a+steps+1
                    faces.extend([(a,a+1,b+1),(a,b+1,b)])
    return np.array(vertices), faces, color


def transform(mesh, matrix, pivot=(0,0,0)):
    v,f,c = mesh
    return (v-np.array(pivot))@matrix.T+np.array(pivot),f,c


def rz(a):
    return np.array([[cos(a),-sin(a),0],[sin(a),cos(a),0],[0,0,1]])


def scene(t):
    meshes = []
    add = meshes.append
    # Oversized rounded head, little ears, and a short antenna.
    add(rounded_box((0,.68,0),(1.48,1.02,.94),.21,SILVER,7))
    add(sphere((-.79,.68,0),(.12,.2,.22),BLUE))
    add(sphere((.79,.68,0),(.12,.2,.22),BLUE))
    add(rounded_box((0,1.3,0),(.075,.3,.075),.03,DARK,2))
    add(sphere((0,1.48,0),(.095,.095,.095),GLINT))
    # Chunky sunglasses with a bridge and narrow reflected highlights.
    for x in (-.35,.35):
        add(rounded_box((x,.76,.476),(.59,.34,.13),.075,DARK,4))
        add(rounded_box((x-.11,.82,.55),(.18,.035,.025),.01,GLINT,2))
    add(rounded_box((0,.78,.5),(.16,.065,.11),.025,DARK,2))
    add(rounded_box((.08,.39,.478),(.29,.045,.025),.012,DARK,2))
    # Neck, blue coveralls, and a small chest display.
    add(sphere((0,.05,0),(.19,.19,.19),DARK))
    add(rounded_box((0,-.53,0),(.96,.97,.66),.18,BLUE,6))
    add(rounded_box((0,-.42,.337),(.53,.27,.045),.04,DARK,3))
    for x in (-.15,0,.15):
        add(sphere((x,-.42,.37),(.035,.035,.025),GLINT,5,8))
    # Tiny planted boots. One arm stays on the hip, the other waves.
    for x in (-.27,.27):
        add(rounded_box((x,-1.14,0),(.24,.37,.27),.07,SILVER,3))
        add(rounded_box((x,-1.4,.12),(.41,.23,.6),.08,DARK,3))
    add(sphere((-.61,-.27,0),(.17,.17,.17),SILVER))
    add(rounded_box((-.75,-.57,.03),(.23,.59,.25),.09,SILVER,3))
    add(sphere((-.76,-.88,.08),(.17,.17,.17),DARK))
    pivot = (.58,-.25,0)
    wave = -.6+.15*sin(t*3)
    arm = [
        sphere(pivot,(.17,.17,.17),SILVER),
        rounded_box((.77,-.07,0),(.24,.59,.25),.09,SILVER,3),
        sphere((.83,.26,0),(.19,.2,.16),DARK),
    ]
    # Three equal fingers and a thumb read as an open wave, even at 210px.
    for x in (.70,.82,.94):
        arm.append(rounded_box((x,.45,0),(.075,.23,.115),.03,DARK,3))
    arm.append(rounded_box((1.02,.26,0),(.18,.08,.12),.03,DARK,3))
    for m in arm:
        add(transform(m,rz(wave),pivot))
    return meshes


def render(t,bg):
    factor = 2
    im = Image.new('RGB',(SIZE*factor,SIZE*factor),bg)
    draw = ImageDraw.Draw(im)
    angle = t + .15
    rotate = np.array([[cos(angle),0,sin(angle)],[0,1,0],[-sin(angle),0,cos(angle)]])
    camera = np.array([[1,0,0],[0,cos(.13),-sin(.13)],[0,sin(.13),cos(.13)]])
    matrix = camera@rotate
    triangles = []
    bob = .045*sin(t*2)
    for v,faces,color in scene(t):
        v = v@matrix.T
        v[:,1] += bob
        center = v.mean(axis=0)
        for a,b,c in faces:
            p = v[[a,b,c]]
            n = np.cross(p[1]-p[0],p[2]-p[0])
            length = np.linalg.norm(n)
            if length < 1e-7:
                continue
            n /= length
            # Orient each convex mesh outwards and hide its back faces.
            if np.dot(n,p.mean(axis=0)-center) < 0:
                n = -n
            if n[2] <= 0:
                continue
            intensity = .48+.48*max(0,float(np.dot(n,LIGHT)))
            rgb = tuple(int(min(255,ch*intensity)) for ch in color)
            xy = [(int((SIZE/2+x*SCALE)*factor),int((SIZE/2+2-y*SCALE)*factor)) for x,y,z in p]
            triangles.append((float(p[:,2].mean()),xy,rgb))
    for _,xy,color in sorted(triangles,key=lambda x:x[0]):
        draw.polygon(xy,fill=color)
    return im.resize((SIZE,SIZE),Image.Resampling.LANCZOS)


if __name__ == '__main__':
    frames = 80
    for theme,bg in [('dark',(13,17,23)),('light',(255,255,255))]:
        images = [render(2*pi*i/frames,bg) for i in range(frames)]
        # A shared palette avoids color flicker during rotation.
        palette_source = Image.new('RGB',(SIZE*4,SIZE*2))
        for i in range(8):
            palette_source.paste(images[i*frames//8],((i%4)*SIZE,(i//4)*SIZE))
        palette = palette_source.quantize(colors=96,method=Image.Quantize.MEDIANCUT)
        quantized = [im.quantize(palette=palette,dither=Image.Dither.NONE) for im in images]
        path = OUT/f'builder-{theme}.gif'
        quantized[0].save(path,save_all=True,append_images=quantized[1:],duration=90,loop=0,optimize=True,disposal=2)
        images[0].save(OUT/f'builder-{theme}-poster.png')
        print(path.name,path.stat().st_size,'bytes')
        if theme == 'dark':
            sheet = Image.new('RGB',(SIZE*4,SIZE*2),bg)
            for i in range(8):
                sheet.paste(images[i*frames//8],((i%4)*SIZE,(i//4)*SIZE))
            sheet.save(ROOT/'preview-robot-frames.png')
