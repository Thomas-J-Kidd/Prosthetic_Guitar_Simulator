# process data from music parser here
import xml.etree.ElementTree as ET
from position_mapping.musicClasses import Note, Song

def XMLInterpret(fileName: str):
    """Parses MusicXML file into Song class containing objects of class Notes"""
    tree = ET.parse(fileName)
    score = tree.getroot()
    songNotes = []
    # Depending XML file structure this section may have to be changed
    songName = score.find('part-list').find('score-part').find('part-name').text 

    for part in score.iter('part'): 
        for measure in part: 
            if(measure.attrib['number'] == '1'):
                divisions = int(measure.find('attributes').find('divisions').text)
                # keySig = int(measure.find('attributes').find('key').find('fifths').text)
                # The current output xml files do not contain the key signature, so it is automatically set to C major
                beats = int(measure.find('attributes').find('time').find('beats').text)
                beatType = int(measure.find('attributes').find('time').find('beat-type').text)
                timeSig = [beats, beatType]
                

            else:
                for note in measure:
                    if note.find('pitch') is not None:
                        name = str(note.find('pitch').find('step').text)
                        
                        if note.find('pitch').find('alter') is not None:
                            accidental = int(note.find('pitch').find('alter').text)
                        else: 
                            accidental = 0
                        
                        octave = int(note.find('pitch').find('octave').text)
                        duration = int(note.find('duration').text)


                    elif note.find('rest') is not None:
                        name = 'rest'
                        accidental = 0
                        octave = 0
                        duration = int(note.find('duration').text)
                        
                    songNotes.append(Note(name, accidental, octave, duration))

    song = Song(songNotes, 60, 0, timeSig, divisions)
    # song.printAttribs()
    return song
            