from dataclasses import dataclass
import yaml
from pathlib import Path

# absolute path for static data files
keySig_path = Path('staticData/KeySig.yml')
with open(str(keySig_path), 'r') as file: 
    keySig_file = yaml.safe_load(file)

#with open('PosDataPhys.yml', 'r') as file:
#    posPhys_file = yaml.safe_load(file)
# change in accordance to model being used
posPhys_path = Path('staticData/model2Phys.yml')
with open(str(posPhys_path), 'r') as file:
    posPhys_file = yaml.safe_load(file)

posStrFrt_path = Path('staticData/PosDataStrFrt.yml')
with open(str(posStrFrt_path), 'r') as file:
    posStrFrt_file = yaml.safe_load(file)

posStrAnimation_path = Path('staticData/PosDataAnimation.yml')
with open(str(posStrAnimation_path), 'r') as file:
    posStrAnimation_file = yaml.safe_load(file)

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
        self.animation = "default"
        self.sound = "FRET1A"

    def findAnimation(self):
        try:
            self.animation = posStrAnimation_file['String'][self.guitarString]['Fret'][self.guitarFret][0]
        except KeyError as ke:
            print(f"Key error: {ke}. Check if the correct guitarString and guitarFret are being used.")
            self.animation = "default"
        except Exception as e:
            self.animation = "default"
            print(f"Could not pull position from yaml file: {e}")

    def findSound(self):
        try:
            self.sound = posStrAnimation_file['String'][self.guitarString]['Fret'][self.guitarFret][1]
        except KeyError as ke:
            print(f"Key error: {ke}. Check if the correct guitarString and guitarFret are being used.")
            self.sound = "FRET1A"
        except Exception as e:
            self.sound = "FRET1A"
            print(f"Could not pull sound from yaml file: {e}")

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
        print('Animation: ', self.animation)
        print('Sound', self.sound)

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
        self.Transpose()
        if notes is not None: 
            for note in notes:
                note.findLen(self.divisions, self.tempo)
                note.findPos()
                note.findAnimation()
                note.findSound()

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


    def Transpose(self):
        """Function to transpose sheet music to guitar correctly"""
        if self.notes is not None: # Check if note exists
            for note in self.notes:
                note.noteNumber = note.noteNumber - 1

    def printAttribs(self): 
        """Function to print attributes of song to console for testing and debugging"""
        print('Start of Song \n')
        print('tempo: ', self.tempo)
        print('Key Signature: ', self.keySig)
        print('Time Signature: ', self.timeSig, '\n')
        if self.notes is not None:
            for note in self.notes: 
                note.printNoteAttribs()


