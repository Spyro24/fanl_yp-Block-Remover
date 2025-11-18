#!/bin/python3
"""
    Render The VVoxels top faces from a block
    (c) 2025 Spyro24
"""
import pygame as p
from fanl_yp.types import faceColors

def render(objectContainer):
    if objectContainer.faces != None:
        allYFaces = objectContainer.faces.positiveY
        surf = p.Surface((8,8), flags=p.SRCALPHA)
        c = 0
        for z in range(8):
            for y in range(8):
                for x in range(8):
                    color = allYFaces[c]
                    c += 1
                    if color > 0:
                        try:
                            surf.set_at((x, -z + 7), faceColors[color])
                        except: pass
    return surf