from position_mapping import processMusic, music_classes
from ursina import *
from ursina.shaders import *
import sys
import time

song = processMusic.processMusic('Twinkle')

def playSong(song: music_classes.Song, counter: int):
    time.sleep(2)
    note = song.notes[counter]

    b = False
        

space = Ursina()

Light()
rotation_info = Text(position=window.top_left)

guitar = Entity(model='guitarModel.obj', rotation=(0,-90,0), color=rgb(173, 216, 230), scale=(1,1,1),
                position=Vec3(0,-4,-11),  shader='pixelation_shader', texture='heightmap_1',
                eternal=True, collider='guitarModel.obj', billboard=True)

guitar.enable


dot1 = Entity(parent=guitar,model='circle', colorize=True, scale=(0.03,0.03,0.03), position=(-0.75, 0, 0),
            rotation=(0,90,0), color=rgb(255, 0, 0))

i = 0
while(i < len(song.notes)):
    space.step()
    note = song.notes[i]
    dot1.position = (-0.75, note.posX, note.posY)
    print(note.posX, note.posY)
    time.sleep(1)
    i = i + 1




