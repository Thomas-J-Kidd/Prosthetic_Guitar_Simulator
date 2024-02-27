from music_classes import Note, Song
import yaml

with open('unit_test.yml', 'r') as file:
    testfile = yaml.safe_load(file)

# import music file as something, parse into helpful objects
print(testfile)
notes = []
for note in testfile['twinkle']['notes']: 
    notes = notes.append(note)
# notes = [testfile['twinkle']['notes']]
timeSig = testfile['twinkle']['beat-type']/testfile['twinkle']['beats']
keySig = testfile['twinkle']['fifths']
rhythm = 60
song = Song(notes, rhythm, keySig, timeSig)
print(song.notes)