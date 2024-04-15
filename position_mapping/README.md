This folder contains the code to go from MusicXML to a position in a 3D space.

### Important Files
- musicClasses.py
- processMusic.py
- moduleTester

### musicClasses
This file contains the class definitions and functions for the classes Song and Note.
The class Song is a dataclass which contains information about the song being parsed. The class Note is a dataclasss which contains information about the Note in the song. 

Both classes are written so that they are easily modified, and can be added to and modified when needed for future use. 

### processMusic
This file contains a function to parse MusicXML into a Song class containing Note objects. This file has to be specifically modified depending on what the MusicXML file looks like. 

### moduleTester
This file is a simple unit tester for the musicClasses file. It uses a yaml file as an input and checks the different attributes of the song. Different testing modes can be applied to the module to test the key signature changes, the accidental changes (sharps or flats applied to a note).