from musicClasses import Note, Song
import position_mapping.XMLInterpret as XMLInterpret
# interface with music parser here

# import music file as something, parse into helpful objects
fileName = 'file_Name' # Get from parser
fileName = 'output.musicxml'
song = XMLInterpret(fileName)
