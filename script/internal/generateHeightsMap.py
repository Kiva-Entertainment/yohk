# Used when making heightMaps for basic gridded maps
# X and y must be adjusted manually to match map
import bpy
import math
import os


x = 18
y = 31
a = []
for i in range(0, x):
	aj = [0.0 for j in range(0, y)]
	a.append(aj)

o = bpy.context.selected_objects[0]
m = o.data.polygons
for face in m.values():
	x = int(face.center[0])
	y = int(face.center[1])
	z = round(face.center[2], 2)
	a[x][y] = z

path = bpy.path.abspath('//groundHeight.txt')
with open(path,'w') as file:
	file.write(str(a))