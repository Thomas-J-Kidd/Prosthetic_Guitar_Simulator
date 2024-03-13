# process data from music parser here
import xml.etree.ElementTree as ET
import music_classes

tree = ET.parse('Twinkle')
score = tree.getroot()

songName = score.find('part-list').find('score-part').find('part-name').text

for part in score.iter('part'): 
    for measure in part: 
        if(measure.attrib['number'] == '1'):
            divisions = int(measure.find('attributes').find('divisions').text)
            keySig = int(measure.find('attributes').find('key').find('fifths').text)
            beats = int(measure.find('attributes').find('time').find('beats').text)
            beatType = int(measure.find('attributes').find('time').find('beat-type').text)
            timeSig = [beats, beatType]
            tempo = measure.find('sound').attrib['tempo']
            print(tempo)
        else:
            for note in measure:
                if note.find('pitch') is not None:
                    name = note.find('pitch').find('step').text
                    accidental = note.find('pitch').find('alter').text
                    octave = note.find('pitch').find('octave').text
                    duration = note.find('duration').text
                elif note.find('rest') is not None:
                    name = 'rest'
                    duration = note.find('duration').text
        


