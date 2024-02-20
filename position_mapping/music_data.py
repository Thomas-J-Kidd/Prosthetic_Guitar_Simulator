from dataclasses import dataclass
import yaml

with open('KeySig.yml', 'r') as file: 
    keySig_file = yaml.safe_load_all(file)


@dataclass
class Note: 
    """Class for keeping track of music notes"""
    name: str
    noteNumber: int # Tells which note. Example: A2 has a noteNumber 2
    noteLength: float # in beats
    guitarString: int
    guitarFret: int

    def __init__(self, name: str, noteNumber: int guitarString: int, guitarFret: int): 
        self.name = name
        self.guitarString = guitarString
        self.guitarFret = guitarFret


    def setlength(self, noteLength: float): 
        self.noteLength


    def position(self) -> list:
        """Function to return physical guitar position"""
        return [self.guitarString,self.guitarFret]
    

@dataclass
class song:
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


    def keyTransform (self):
        """Function to transform notes to actual notes based on key"""
        newKeySig = keySig_file[self.keySig]
        for note in self.notes:
            
            # perform some kind of transform on note
            return None

    def noteTime(self) -> list:
        """Function to calculate actual time for each note"""
        noteTimes = self.notes.noteLength*(1/self.rhythm) # correct for iterating through notes
        return noteTimes



n = Note()
