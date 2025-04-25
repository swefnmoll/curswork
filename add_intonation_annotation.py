import mytextgrid as mtg
import os
import parselmouth
import numpy as np

for dictor in os.scandir('static'):
    for file in dictor:
        if file.name.endswith('.TextGrid'):
            tg = mtg.read_from_file(file)
            snd = parselmouth.Sound(file.name.splitext() + '.wav')
            intensity_tier = tg.insert_tier('Intensity', False)
            pitch_tier = tg.insert_tier('Pitch', False)

            for interval in tg.tiers[0]:
                if len(interval.text) > 2:
                    lb = interval.xmin
                    rb = interval.xmax

            for syntagm in tg.tiers[1]:
                syntagm_snd = snd.extract_part(from_time=syntagm.xmin, to_time=syntagm.xmax, preserve_times=True)
                syntagm_pitch = syntagm_snd.to_pitch().get_array
                syntagm_intensity = syntagm_snd.to_intensity().get_array
                min_pitch = np.argmin(syntagm_pitch)
                max_pitch = np.argmax(syntagm_pitch)
                min_intens = np.argmin(syntagm_intensity)
                max_intens = np.argmax(syntagm_intensity)
                intensity_tier.insert_point()