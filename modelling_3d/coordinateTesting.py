from ursina import *
from ursina.prefabs import hot_reloader
import sys
from ursina.shaders import *

original_stdout = sys.stdout

space = Ursina()

ec = EditorCamera(ignore_scroll_on_ui=True)
rotation_info = Text(position=window.top_left)
Light()

guitar = Entity(model='guitarModel.obj', rotation=(0,-90,0),color=rgb(102, 255, 255), scale=(1.2,1.2,1.2),
                world_position=Vec3(0,-4.5,-11), shader='unlit_shader', texture='heightmap_1',
                eternal=True, collider='guitarModel.obj', billboard=True)

guitar.enable

dot = Entity(parent=guitar, model='circle', colorize=True, scale=(0.03,0.03,0.03), position=(-0.77, 3.95, 0.095),
            rotation=(0,90,0))

ySlide = Slider(max=4.2, min=2, position=(0.2, 0.1,0), step=0.005, setattr=(dot, 'y'))
zSlide = Slider(max=0.15, min=-0.2, position=(0.2, 0,0), step=0.005, setattr=(dot, 'z'))

space.run()
