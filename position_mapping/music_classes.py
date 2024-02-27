from dataclasses import dataclass
import yaml

with open('KeySig.yaml', 'r') as file: 
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
        self.noteNumber = noteNumber
        self.noteLengthBeats = noteLengthBeats

        self.findPos()


    def findLen(self, rhythm: int): 
        """Function to calculate noteLengthTime in seconds"""
        self.noteLengthTime = self.noteLengthBeats*(1/rhythm)*60.0

    def findPos(self): 
        """Function to find the position String, Fret, and Physical Position"""
        self.guitarString, self.guitarFret = posStrFrt_file[self.name][self.noteNumber]
        self.guitarFret = self.guitarFret + self.noteAccidental
        self.posX, self.posY = posPhys_file['String'][self.guitarString]['Fret'][self.guitarFret]
    

@dataclass
class Song:
    """Class for keeping track of song"""
    notes: list[Note] 
    rhythm: int # in bpm
    keySig: str # key signature example: AShMajor (A# Major)
    timeSig: tuple # time signature example: [4,4]

    def __init__(self, notes: list[Note], rhythm: int, keySig: str, timeSig: tuple): 
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
        if self.notes is not None:
            for note in self.notes:
                newAccidental = newKeySig[note.name]
                note.noteAccidental = note.noteAccidental + newAccidental
                # perform some kind of transform on note
