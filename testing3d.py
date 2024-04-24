"""This file contains the integration of the 3D environment and the
position mapping module
"""


from position_mapping import XMLInterpret, musicClasses
from ursina.prefabs.file_browser import FileBrowser
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina import *
from ursina.shaders import *
import sys
import time




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

filePath = 'musicXML_Files/output.musicxml'



# demo running logic 
def demo():
    song = XMLInterpret.XMLInterpret(filePath)
    i = 0
    time.sleep(1)
    while(i < len(song.notes)):
        note = song.notes[i]    
        length = note.noteLengthTime
        dot1.world_position = (note.posX, note.posY, 3.9)
        print(note.posX, note.posY)
        time.sleep(length)
        i = i + 1


# for choosing musicxml file to parse
fb = FileBrowser(file_types=('.musicxml'), enabled=False)

def on_submit(paths):
    print('-------', paths)
    for p in paths:
        print('---', p)
    filePath = paths
fb.on_submit = on_submit

def input(key):
    if key == 'tab':
        fb.enabled = not fb.enabled

# play button
playButton = Button(text='Play', model='circle', scale=0.2, origin=(-2.5,-1.5,0))
playButton.on_click = demo
space.run()



