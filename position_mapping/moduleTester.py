from music_classes import Note, Song
import yaml

# import test yaml file
with open('unit_tests.yml', 'r') as file:
    testfile = yaml.safe_load(file)

def tester(testfile: dict, keySigTest: bool, accidentalTest: bool, rhythm: int) -> list[Song]:
    # initialize tests list
    tests = []
    # unpack data from testing file
    for i in range(len(testfile)):
        notes = []
        timeSig = testfile[i]['beat-type']/testfile[i]['beats']
        keySig = testfile[i]['fifths']

        for note in range(len(testfile[i]['notes'])):
            name = testfile[i]['notes'][note]['name'] # collect note name
            octave = testfile[i]['notes'][note]['octave'] # collect note octave
            duration = testfile[i]['notes'][note]['duration'] # collect note duration in beats
            accidental = testfile[i]['notes'][note]['accidental'] # collect sharps/flats
            if accidentalTest == False:
                newNote = Note(name, accidental, octave, duration)
            else: 
                for acc in range(-2,2):
                    newNote = Note(name, acc, octave, duration)
            notes.append(newNote)
            if keySigTest == False: 
                tests.append(Song(notes, rhythm, keySig, timeSig))
            else: 
                for key in range(-7,7):
                    tests.append(Song(notes, rhythm, key, timeSig))
                    key += 1
    return tests

normalTest = tester(testfile, False, False, 60)
accidentalTest = tester(testfile, False, True, 60)
keySigTest = tester(testfile, True, False, 60)

