from music_classes import Note, Song
import yaml

# import test yaml file
with open('unit_test.yml', 'r') as file:
    testfile = yaml.safe_load(file)

# import music file as something, parse into helpful objects

notes1 = []
notes2 = []

# unpack data file and create Note objects
for note, [x, y] in testfile['note_test']['notes'].items(): 
    number = testfile['note_test']['notes'][note][x]
    beat = testfile['note_test']['notes'][note][y]
    newNote = Note(note, 0, number, beat)
    notes1.append(newNote)
timeSig1 = testfile['note_test']['beat-type']/testfile['note_test']['beats']
keySig1 = testfile['note_test']['fifths']
rhythm1 = 60
test1 = Song(notes1, rhythm1, keySig1, timeSig1)
print("end test 1")

# Testing key transform on notes with no accidentals
for note, [x] in testfile['key_test1']['notes'].items(): 
    number = testfile['key_test1']['notes'][note][x]
    newNote = Note(note, 0, number, 4)
    notes2.append(newNote)
timeSig2 = testfile['key_test1']['beat-type']/testfile['key_test1']['beats']
keySig2 = testfile['key_test1']['fifths']
rhythm2 = 60
test2 = Song(notes2, rhythm2, keySig2, timeSig2)
print('end test 2')

# Testing key transform on notes with accidentals
notes3 = []
for note, [x,y] in testfile['key_test2']['notes'].items(): 
    number = testfile['key_test2']['notes'][note][x]
    accidental = testfile['key_test2']['notes'][note][y]
    newNote = Note(note, accidental, number, 4)
    notes3.append(newNote)
timeSig3 = testfile['key_test2']['beat-type']/testfile['key_test2']['beats']
keySig3 = testfile['key_test2']['fifths']
rhythm3 = 60
test3 = Song(notes3, rhythm3, keySig3, timeSig3)
print("end test 3")