#Andree Toledo 18439
#Laboratorio 3 OBJ

from gl import Render

render = Render()
render.glColor(0.130, 0.240, 0.750) #Color Azul Mustang

render.load('./mustang_GT.obj', translate=[550, 50], scale = [36, 36])
render.glFinish()