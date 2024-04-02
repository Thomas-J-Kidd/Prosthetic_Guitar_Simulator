from ursina import *
from ursina.prefabs import hot_reloader
import sys

original_stdout = sys.stdout

space = Ursina()

ec = EditorCamera(ignore_scroll_on_ui=True)
rotation_info = Text(position=window.top_left)

guitar = Entity(model='guitarModel.obj', rotation=(0,-90,0),color=(0,0,0.5), scale=(1,1,1),
                position=Vec3(0,-2,0), texture='grass',  shader='unlit_shader',
                eternal=True, collider='guitarModel.obj')

guitar.enable

dot = Entity(parent=guitar,model='circle', colorize=True, scale=(0.08,0.08,0.08), position=(-0.9,3,0),
            rotation=(0,90,0))

space.run()
