from dataclasses import dataclass

@dataclass
class Note: 
    """Class for keeping track of music notes"""
    name: str
    noteLength: float # in beats
    guitarString: int
    fret: int

    def position(self) -> list:
        """Function to return physical guitar position"""
        return [self.guitarString,self.fret]
    
@dataclass
class song:
    """Class for keeping track of song"""
    notes: list[Note] 
    rhythm: int # in bpm
    key: str 
    timeSignature: tuple

    def keyTransform (self):
        """Function to transform notes to actual notes based on key"""
        

        for i in self.notes:
            
        newKeyNotes = self.notes
        return newKeyNotes

    def noteTime(self) -> list:
        """Function to calculate actual time for each note"""
        noteTimes = self.notes.noteLength*(1/self.rhythm) # correct for iterating through notes
        return noteTimes



n = Note()
