from dataclasses import dataclass
import yaml

# absolute path for static data files
with open('c:/Users/cocon/GitHub/Prosthetic_Guitar_Simulator/position_mapping/staticData/KeySig.yml', 'r') as file: 
    keySig_file = yaml.safe_load(file)

#with open('PosDataPhys.yml', 'r') as file:
#    posPhys_file = yaml.safe_load(file)
# change in accordance to model being used
with open('c:/Users/cocon/GitHub/Prosthetic_Guitar_Simulator/position_mapping/staticData/model2Phys.yml', 'r') as file:
    posPhys_file = yaml.safe_load(file)

with open('c:/Users/cocon/GitHub/Prosthetic_Guitar_Simulator/position_mapping/staticData/PosDataStrFrt.yml', 'r') as file:
    posStrFrt_file = yaml.safe_load(file)

@dataclass
class Note: 
    """Class for keeping track of music notes"""

    def __init__ (self, name: str, noteAccidental: int, noteNumber: int, noteLength: float): 
        """initializer function"""
        self.name = name
        self.noteNumber = noteNumber
        self.noteAccidental = noteAccidental
        self.noteLength = noteLength
        self.guitarString = 0
        self.guitarFret = 0
        self.posX = -0.7
        self.posY = 4

    def findLen(self, divisions: float, tempo: float): 
        """Function to calculate noteLengthTime in seconds"""
        self.noteLengthTime = (self.noteLength/divisions)*(60.0/tempo)

    def findPos(self): 
        """Function to find the position String, Fret, and Physical Position.
        To apply a sharp or flat, the note octave and name are not transformed,
        instead just changing the string and fret. If the note is a rest, string
        and fret position are set to 0.
        """
        if self.name == 'rest': 
            self.guitarFret = 0
            self.guitarString = 0
        try:
            self.guitarString, self.guitarFret = posStrFrt_file[self.name][self.noteNumber]
        except KeyError: 
            print("Octave is not valid")
            return None
        else:
            self.guitarString, self.guitarFret = posStrFrt_file[self.name][self.noteNumber]

        if(self.guitarFret + self.noteAccidental) < 0:
            self.guitarFret = 0
        else: 
            self.guitarFret = self.guitarFret + self.noteAccidental
            self.posX, self.posY = posPhys_file['String'][self.guitarString]['Fret'][self.guitarFret]

            
    def printNoteAttribs(self): 
        """Prints attributes of each note"""
        print('Name: ', self.name)
        print('Octave: ', self.noteNumber)
        print('Accidental: ', self.noteAccidental)
        print('Duration: ', self.noteLength)
        print('Time: ', self.noteLengthTime)
        print('String: ', self.guitarString)
        print('Fret: ', self.guitarFret)

@dataclass
class Song:
    """Class for keeping track of song
    Parameters: 
    notes: list[Note]
    tempo: float
    keySig: int
    timeSig: tuple
    """
    def __init__(self, notes: list[Note], tempo: float, keySig: int, timeSig: tuple, divisions: float): 
        self.notes = notes
        self.tempo = tempo
        self.keySig = keySig
        self.timeSig = timeSig
        self.divisions = divisions
        
        self.keyTransform()
        if notes is not None: 
            for note in notes:
                note.findLen(self.divisions, self.tempo)
                note.findPos()

    def keyTransform (self):
        """Function to transform notes to actual notes based on key"""
        newKeySig = keySig_file[self.keySig]

        if self.notes is not None: # Check if note exists
            for note in self.notes:
                if note.name != 'rest':
                    # get new accidental from key signature file
                    newAccidental = newKeySig[note.name] 
                    # add key signature change to note
                    note.noteAccidental = note.noteAccidental + newAccidental
                    # find new finger position 
                    note.findPos() 


    def printAttribs(self): 
        """Function to print attributes of song to console for testing and debugging"""
        print('Start of Song \n')
        print('tempo: ', self.tempo)
        print('Key Signature: ', self.keySig)
        print('Time Signature: ', self.timeSig, '\n')
        if self.notes is not None:
            for note in self.notes: 
                note.printNoteAttribs()


