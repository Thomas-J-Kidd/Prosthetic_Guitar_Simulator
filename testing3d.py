"""This file contains the integration of the 3D environment and the
position mapping module
"""

from position_mapping import XMLInterpret, musicClasses
# from CadenCV import sheetMusicInterpret
from ursina.prefabs.file_browser import FileBrowser
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina import *
from ursina.shaders import *
import sys
import time



class dotModel(Entity): 
    def update(self):
        self.world_position = self.world_position


space = Ursina()

Light()
rotation_info = Text(position=window.top_left)



guitar = Entity(model='Guitar2.obj', world_rotation=(67,158,40),color=rgb(102, 255, 255), scale=(1,1,1),
                world_position=Vec3(-1.5,-9,9),  texture='heightmap_1', 
                eternal=True, collider='Guitar2.obj')

guitar.enable


dot1 = dotModel(world_parent=guitar, model='circle', colorize=True, scale=(0.15,0.15,0.15), world_position=(0, 4, 3.9),
            rotation=(67,158,40), collider='circle', color=rgb(255, 0, 0))


filePath = 'musicXML_Files/Mary.xml'
noteName = ''
# demo running logic 
def demo():
    song = XMLInterpret.XMLInterpret(filePath)
    i = 0
    while(i < len(song.notes)):
        
        note = song.notes[i]    
        length = note.noteLengthTime
        noteButton.text=note.name + str(note.noteNumber)
        dot1.world_position = (note.posX, note.posY, 3.9)
        print(note.posX, note.posY)
        time.sleep(length)
        i = i + 1
        

noteButton = Button(text='Note', model='circle', scale=0.1, origin=(-6.5,-1,0))


# for choosing musicxml file to parse
fb = FileBrowser(file_types=('.xml'), enabled=False)

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
playButton = Button(text='Play', model='circle', scale=0.15, origin=(-4.5,-2,0))
playButton.on_click = demo


song = XMLInterpret.XMLInterpret(filePath)
i = 0
while(i < len(song.notes)):
    
    note = song.notes[i]    
    length = note.noteLengthTime
    noteButton.text=note.name + str(note.noteNumber)
    dot1.world_position = (note.posX, note.posY, 3.9)
    print(note.posX, note.posY)
    time.sleep(length)
    i = i + 1
# demo()
# space.run()
