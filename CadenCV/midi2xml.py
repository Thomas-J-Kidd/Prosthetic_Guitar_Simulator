import os
from music21 import converter
from pathlib import Path

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

def convert_all_midis_in_folder(input_directory, output_directory):
    """
    Converts all MIDI files in the specified input directory to MusicXML files in the output directory.

    Args:
        input_directory (str): The directory containing MIDI files.
        output_directory (str): The directory to save the MusicXML files.
    """
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loop through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.mid') or filename.lower().endswith('.midi'):
            # Create paths for input and output files
            midi_file_path = os.path.join(input_directory, filename)
            musicxml_file_name = filename.rsplit('.', 1)[0] + '.xml'
            musicxml_file_path = os.path.join(output_directory, musicxml_file_name)
            
            # Convert the MIDI file to MusicXML
            midi_to_musicxml(midi_file_path, musicxml_file_path)
            print(f"Converted {midi_file_path} to {musicxml_file_path}")

# Example usage
input_midi = Path('output')
output_xml = Path('output/XML')
convert_all_midis_in_folder(str(input_midi), str(output_xml))
