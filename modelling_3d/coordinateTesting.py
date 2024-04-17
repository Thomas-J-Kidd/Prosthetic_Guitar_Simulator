"""This file can be run to show a demo of the guitar model in the 3D 
environment, and can also be used to locate the coordinates of each
string and fret relative to the guitar object in the 3D environment.
"""

from ursina import *
from ursina.prefabs import hot_reloader
import sys
from ursina.shaders import *

original_stdout = sys.stdout

space = Ursina()

ec = EditorCamera(ignore_scroll_on_ui=True)
rotation_info = Text(position=window.top_left)
Light()

guitar = Entity(model='Guitar2.obj', world_rotation=(67,158,40),color=rgb(102, 255, 255), scale=(1,1,1),
                world_position=Vec3(-1.5,-9,9),  texture='heightmap_1',
                eternal=True, collider='Guitar2.obj')

inverseRot = -guitar.world_rotation
#guitar.rotation = inverseRot
#guitar.transform_setter(((0,-7,30), (62,167,33), (1,1,1)))
guitar.enable


dot = Entity(world_parent=guitar, model='circle', colorize=True, scale=(0.15,0.15,0.15), world_position=(0, 4, 3.9),
            rotation=(67,158,40), collider='circle')
xSlide = Slider(default=0, max=2, min=-0.6, position=(-0.7, 0.2,0), step=0.05, setattr=(dot, 'world_x'))
ySlide = Slider(default=0, max=4, min=-3.8, position=(-0.7, 0.1,0), step=0.05, setattr=(dot, 'world_y'))
#zSlide = Slider(default=15.5, max=15.5, min=14.9, position=(-0.7, 0,0), step=0.1, setattr=(dot, 'world_z'))

#xRotSlide = Slider(default=67, max=360, min=0, position=(0.2, 0.2,0), step=1, setattr=(guitar, 'world_rotation_x'))
#yRotSlide = Slider(default=158, max=360, min=0, position=(0.2, 0.1,0), step=1, setattr=(guitar, 'world_rotation_y'))
#zRotSlide = Slider(default=40, max=360, min=0, position=(0.2, 0,0), step=1, setattr=(guitar, 'world_rotation_z'))

space.run()
