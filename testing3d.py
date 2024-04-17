"""This file contains the integration of the 3D environment and the
position mapping module
"""


from position_mapping import processMusic, musicClasses
from ursina import *
from ursina.shaders import *
import sys
import time


song = processMusic.processMusic('Twinkle')

def playSong(song: musicClasses.Song, counter: int):
    time.sleep(2)
    note = song.notes[counter]

    b = False
        

space = Ursina()

Light()
rotation_info = Text(position=window.top_left)

guitar = Entity(model='Guitar2.obj', world_rotation=(67,158,40),color=rgb(102, 255, 255), scale=(1,1,1),
                world_position=Vec3(-1.5,-9,9),  texture='heightmap_1', 
                eternal=True, collider='Guitar2.obj')

guitar.enable


dot1 = Entity(world_parent=guitar, model='circle', colorize=True, scale=(0.15,0.15,0.15), world_position=(0, 4, 3.9),
            rotation=(67,158,40), collider='circle', color=rgb(255, 0, 0))

i = 0
while(i < len(song.notes)):
    space.step()
    note = song.notes[i]
    dot1.world_position = (note.posX, note.posY, 3.9)
    print(note.posX, note.posY)
    time.sleep(1)
    i = i + 1




