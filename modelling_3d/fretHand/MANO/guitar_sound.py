import logging
from pydub import AudioSegment
import simpleaudio as sa

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class GuitarSimulator:
    def __init__(self):
        self.sample = []
        logging.info("GuitarSimulator instance created")

    def load_sound(self, path):
        """Load a guitar sound from the specified path."""
        try:
            self.sample.append(AudioSegment.from_file(path))
            logging.info(f"Loaded sound from {path}")
        except Exception as e:
            logging.error(f"Failed to load sound from {path}: {e}")

    def play_sound(self):
        """Play the loaded sound in its entirety."""
        if self.sample is None:
            logging.warning("No sound loaded. Please load a sound first.")
            return
        
        try:
            # Convert pydub.AudioSegment to bytes and play with simpleaudio
            raw_data = self.sample.pop(0).raw_data
            #play_obj = sa.play_buffer(raw_data, num_channels=self.sample.channels, bytes_per_sample=self.sample.sample_width, sample_rate=self.sample.frame_rate)
            play_obj.wait_done()  # Wait until sound has finished playing
            logging.info("Sound played in its entirety.")
        except Exception as e:
            logging.error(f"Error playing sound: {e}")

if __name__ == "__main__":
    from pathlib import Path
    FRET1A = Path("sound/FRET1A.mp3")
    guitar = GuitarSimulator()
    guitar.load_sound(str(FRET1A))
    guitar.play_sound()  # Simply play the loaded sound
