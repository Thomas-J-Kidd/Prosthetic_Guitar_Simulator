# process data from music parser here
import xml.etree.ElementTree as ET
from music_classes import Note, Song

def processMusic(fileName: str):
    tree = ET.parse(fileName)
    score = tree.getroot()
    songNotes = []
    songName = score.find('part-list').find('score-part').find('part-name').text

    for part in score.iter('part'): 
        for measure in part: 
            if(measure.attrib['number'] == '1'):
                divisions = int(measure.find('attributes').find('divisions').text)
                keySig = int(measure.find('attributes').find('key').find('fifths').text)
                beats = int(measure.find('attributes').find('time').find('beats').text)
                beatType = int(measure.find('attributes').find('time').find('beat-type').text)
                timeSig = [beats, beatType]
                tempo = float(measure.find('sound').attrib['tempo'])
                print(tempo)
            else:
                for note in measure:
                    if note.find('pitch') is not None:
                        name = note.find('pitch').find('step').text
                        accidental = int(note.find('pitch').find('alter').text)
                        octave = int(note.find('pitch').find('octave').text)
                        duration = int(note.find('duration').text)
                    elif note.find('rest') is not None:
                        name = 'rest'
                        accidental = 0
                        octave = 0
                        duration = int(note.find('duration').text)
                    songNotes.append(Note(name, accidental, octave, duration))

    song = Song(songNotes, tempo, keySig, timeSig)
    song.printAttribs()
    return song
            


