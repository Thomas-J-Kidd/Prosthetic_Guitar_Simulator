from music_classes import Note, Song
import yaml

# import test yaml file
with open('unit_test.yml', 'r') as file:
    testfile = yaml.safe_load(file)

# import music file as something, parse into helpful objects
    

for i in range(len(testfile)):
    notes = []
    timeSig = testfile[i]['beat-type']/testfile[i]['beats']
    keySig = testfile[i]['fifths']
    rhythm = 60
    for note in range(len(testfile[i]['notes'])):
        name = testfile[i]['notes'][note]['name']
        print(name)
        number = testfile[i]['notes'][note]['octave']
        beat = testfile[i]['notes'][note]['duration']
        accidental = testfile[i]['notes'][note]['accidental']
        newNote = Note(name, accidental, number, beat)
        notes.append(newNote)
    test = Song(notes, rhythm, keySig, timeSig)
    print('end','\n')
