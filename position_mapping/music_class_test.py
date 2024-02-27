from music_classes import Note, Song
import yaml

with open('unit_test.yml', 'r') as file:
    testfile = yaml.safe_load(file)
# import music file as something, parse into helpful objects

notes1 = []
notes2 = []

# print(testfile['twinkle'])
for note, [x, y] in testfile['twinkle']['notes'].items(): 
    number = testfile['twinkle']['notes'][note][x]
    beat = testfile['twinkle']['notes'][note][y]
    newNote = Note(note, 0, number, beat)
    notes1.append(newNote)
timeSig1 = testfile['twinkle']['beat-type']/testfile['twinkle']['beats']
keySig1 = testfile['twinkle']['fifths']
rhythm1 = 60
test1 = Song(notes1, rhythm1, keySig1, timeSig1)


for note, [x, y] in testfile['key_change_test']['notes'].items(): 
    number = testfile['key_change_test']['notes'][note][x]
    beat = testfile['key_change_test']['notes'][note][y]
    newNote = Note(note, 0, number, beat)
    notes2.append(newNote)

timeSig2 = testfile['key_change_test']['beat-type']/testfile['key_change_test']['beats']
keySig2 = testfile['key_change_test']['fifths']
rhythm2 = 60
test2 = Song(notes2, rhythm2, keySig2, timeSig2)
