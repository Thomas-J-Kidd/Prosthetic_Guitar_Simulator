from music_classes import Note, Song
import yaml


def tester(fileName: str, keySigTest: bool, accidentalTest: bool, rhythm: int) -> list[Song]:
    # load in test data file
    with open(fileName, 'r') as file:
        testFile = yaml.safe_load(file)
    # initialize tests list
    tests = []
    # unpack data from testing file
    for i in range(len(testFile)):
        notes = []
        timeSig = (testFile[i]['beat-type'],testFile[i]['beats'])
        keySig = testFile[i]['fifths']

        for note in range(len(testFile[i]['notes'])):
            name = testFile[i]['notes'][note]['name'] # collect note name
            octave = testFile[i]['notes'][note]['octave'] # collect note octave
            duration = testFile[i]['notes'][note]['duration'] # collect note duration in beats
            accidental = testFile[i]['notes'][note]['accidental'] # collect sharps/flats
            
            if accidentalTest == True: 
                for acc in range(-2,2):
                    newNote = Note(name, acc, octave, duration)
                    notes.append(newNote)
            else: 
                newNote = Note(name, accidental, octave, duration)
                notes.append(newNote)

            
        if keySigTest == True: 
            for key in range(-7,7):
                newSong = Song(notes, rhythm, key, timeSig)
                # newSong.printAttribs()
                tests.append(newSong)
        else: 
            newSong = Song(notes, rhythm, keySig, timeSig)
            # newSong.printAttribs()
            tests.append(newSong)
        
            
    return tests

testFile = 'unit_tests.yml'
normalTest = tester(testFile, False, False, 60)
for test in normalTest: 
    test.printAttribs()

print("Accidentals test:  \n")
accidentalTest = tester(testFile, False, True, 60)
for test in accidentalTest: 
    test.printAttribs()
# keySigTest = tester(testFile, True, False, 60)

