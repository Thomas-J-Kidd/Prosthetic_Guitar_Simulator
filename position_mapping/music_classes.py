from dataclasses import dataclass
import yaml

with open('KeySig.yml', 'r') as file: 
    keySig_file = yaml.safe_load(file)

with open('PosDataPhys.yml', 'r') as file:
    posPhys_file = yaml.safe_load(file)

with open('PosDataStrFrt.yml', 'r') as file:
    posStrFrt_file = yaml.safe_load(file)

@dataclass
class Note: 
    """Class for keeping track of music notes"""

    def __init__ (self, name: str, noteAccidental: int, noteNumber: int, noteLengthBeats: int): 
        """initializer function"""
        self.name = name
        self.noteNumber = noteNumber
        self.noteAccidental = noteAccidental
        self.noteLengthBeats = noteLengthBeats

        

    def findLen(self, rhythm: int): 
        """Function to calculate noteLengthTime in seconds"""
        self.noteLengthTime = self.noteLengthBeats*(1/rhythm)*60.0

    def findPos(self): 
        """Function to find the position String, Fret, and Physical Position"""
        try:
            self.guitarString, self.guitarFret = posStrFrt_file[self.name][self.noteNumber]
        except KeyError: 
            # print("Octave is not valid")
            return None
        else:
            self.guitarString, self.guitarFret = posStrFrt_file[self.name][self.noteNumber]

        if(self.guitarFret + self.noteAccidental) < 0:
            self.guitarFret = 0
        else: 
            self.guitarFret = self.guitarFret + self.noteAccidental
        self.posX, self.posY = posPhys_file['String'][self.guitarString]['Fret'][self.guitarFret]
    
    def printNoteAttribs(self): 
        print('Name: ', self.name)
        print('Octave: ', self.noteNumber)
        print('Accidental: ', self.noteAccidental)
        print('Duration: ', self.noteLengthBeats)
        print('Time: ', self.noteLengthTime)
        print('String: ', self.guitarString)
        print('Fret: ', self.guitarFret)

@dataclass
class Song:
    """Class for keeping track of song"""
    def __init__(self, notes: list[Note], rhythm: int, keySig: int, timeSig: tuple): 
        self.notes = notes
        self.rhythm = rhythm
        self.keySig = keySig
        self.timeSig = timeSig

        self.keyTransform()
        if notes is not None: 
            for note in notes:
                note.findLen(self.rhythm)

    def keyTransform (self):
        """Function to transform notes to actual notes based on key"""
        newKeySig = keySig_file[self.keySig]

        if self.notes is not None: # Check if note exists
            for note in self.notes:
                newAccidental = newKeySig[note.name] # get new accidental from key signature file
                note.noteAccidental = note.noteAccidental + newAccidental # add key signature change to note
                note.findPos() # find new finger position 


    def printAttribs(self): 
        """Function to print attributes of song to console for testing and debugging"""
        print('Start of Song \n')
        print('Rhythm: ', self.rhythm)
        print('Key Signature: ', self.keySig)
        print('Time Signature: ', self.timeSig, '\n')
        if self.notes is not None:
            for note in self.notes: 
                note.printNoteAttribs()


