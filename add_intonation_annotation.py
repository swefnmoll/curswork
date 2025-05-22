import mytextgrid as mtg
import os
import parselmouth
import numpy as np

class Annotation:

    def __init__(self, file):
        self.tg = mtg.read_from_file(file)
        self.snd = parselmouth.Sound(file.name.splitext() + '.wav')
        self.intensity_tier = tg.insert_tier('Intensity', False)
        self.pitch_tier = tg.insert_tier('Pitch', False)

    def interval_borders(self):
        self.lb = interval.xmin
        self.rb = interval.xmax

    def syntagm_read(self, syntagm):
        self.snd = snd.extract_part(from_time=syntagm.xmin, to_time=syntagm.xmax, preserve_times=True)
        self.pitch = syntagm_snd.to_pitch().get_array
        self.intensity = syntagm_snd.to_intensity().get_array
        self.min_pitch = np.argmin(self.pitch)
        self.max_pitch = np.argmax(self.pitch)
        self.min_intens = np.argmin(self.intensity)
        self.max_intens = np.argmax(self.intensity)

    def annotation(self):

    def __del__(self):
        pass

for dictor in os.scandir('reserv'):
    for file in dictor:
        if file.name.endswith('.TextGrid'):
            annotation = Annotation(file)
            for interval in tg.tiers[0]:
                if len(interval.text) > 2:
