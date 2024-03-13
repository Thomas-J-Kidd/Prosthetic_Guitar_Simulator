# process data from music parser here
import xml.etree.ElementTree as ET
import music_classes

tree = ET.parse('Twinkle')
score = tree.getroot()
print(score)


for part in score.iter('part-list'):
    for partInfo in part.iter('score-part'):
        songName = partInfo.find('part-name').text
        print(songName)


for part in score.iter('part'): 
    print(part)
    for measure in part: 
        if(measure.attrib['number'] == '1'):
            for attributes in measure.iter('attributes'):
                divisions = attributes.find('divisions').text
                key = attributes.get('key')
                
                print(key)

        songInfo = measure.find('note').text
        for note in measure.iter('note'):
            for pitch in note.iter('pitch'):
                name = pitch.find('step').text
                accidental = pitch.find('alter').text
                octave = pitch.find('octave').text
    


