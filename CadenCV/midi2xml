from music21 import converter

def midi_to_musicxml(midi_file_path, musicxml_file_path):
    """
    Converts a MIDI file to a MusicXML file using the music21 library.
    
    Args:
    midi_file_path (str): The file path for the input MIDI file.
    musicxml_file_path (str): The file path where the output MusicXML file will be saved.
    """
    # Load the MIDI file into a music21 stream
    stream = converter.parse(midi_file_path)
    
    # Write the stream to a MusicXML file
    stream.write('musicxml', fp=musicxml_file_path)

# Corrected file paths with raw strings
midi_to_musicxml(
    r'inpout_directory\output.mid',
    r'output_directory\musicxml_file.xml'
)
