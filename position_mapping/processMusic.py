# process data from music parser here
import xml.etree.ElementTree as ET

tree = ET.parse('Twinkle')
score = tree.getroot()
print(score)

for part in score.iter('part-list'):
    for partInfo in part.iter('score-part'):
        songName = partInfo.find('part-name').text
        

for part in score.iter('part'): 
    print(part)
    for measure in part: 
        
