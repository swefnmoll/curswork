import mytextgrid as mtg
import parselmouth
from os import path

class Annotation:

    def __init__(self, file):
        self.tg = mtg.read_from_file(file)
        self.snd = parselmouth.Sound(path.splitext(file)[0] + '.wav')
        self.syntagms = []

#    def sentence_read(self):
#        for interval in self.tg[0]:
#            if len(interval.text) > 1:
#                sentence_lb = interval.xmin
#                sentence_rb = interval.xmax
#                self.snd_sentence = self.snd.extract_part(from_time=sentence_lb, to_time=sentence_rb, preserve_times=True)
#                return self.snd_sentence

    def syllabe(self, point, xs, values):
        time = xs[list(values).index(point)]
        for interval in self.tg[2]:
            if time >= interval.xmin and time <= interval.xmax:
                return list(self.tg.tiers[2]).index(interval), interval.text

    def read_pitch(self, snd):
        raw_pitch = snd.to_pitch().selected_array['frequency']
        pitch = list(filter(lambda x: x != 0, raw_pitch))
        max_pitch = max(pitch)
        min_pitch = min(pitch)
        max_syll, text_max_syll = self.syllabe(max_pitch, snd.to_pitch().xs(), raw_pitch)
        min_syll, text_min_syll = self.syllabe(min_pitch, snd.to_pitch().xs(), raw_pitch)
        return max_syll, text_max_syll, min_syll, text_min_syll

    def read_intensity(self, snd):
        intensity = snd.to_intensity()
        max_intensity = max(intensity.values.T)
        min_intensity = min(intensity.values.T)
        max_syll, text_max_syll = self.syllabe(max_intensity, intensity.xs(), intensity.values.T)
        min_syll, text_min_syll = self.syllabe(min_intensity, intensity.xs(), intensity.values.T)
        return max_syll, text_max_syll, min_syll, text_min_syll

    def syntagm_read(self):
        for interval in self.tg.tiers[1]:
            if len(interval.text) > 1:
                syntagm_lb = interval.xmin
                syntagm_rb = interval.xmax
                snd_syntagm = self.snd.extract_part(from_time=syntagm_lb, to_time=syntagm_rb,
                                                         preserve_times=True)
                self.syntagms.append(snd_syntagm)
        return self.syntagms

    def annotate(self, syntagm_pitch, syntagm_intensity, file_path):
        absolute_max_pitch = max()
        text_max_pitch = max
        self.tg.tiers[2].set_text_at_index(pitch[0][0], pitch[0][1] + ' HP')
        self.tg.tiers[2].set_text_at_index(pitch[1][0], pitch[1][1] + ' L')
        self.tg.tiers[2].set_text_at_index(intensity[0][0], intensity[0][1] + ' ')
        self.tg.tiers[2].set_text_at_index(intensity[1][0], intensity[0][1] + ' LI!')
        self.tg.write(file_path)

    def __del__(self):
        pass

def read_and_annotate(file_path):
    syntagm_pitch = []
    syntagm_intensity = []
    file = Annotation(file_path)
#    sentence = file.sentence_read()
#    sentence_pitch = file.read_pitch(sentence)
#    sentence_intensity = file.read_intensity(sentence)
    syntagms = file.syntagm_read()
    for syntagm in syntagms:
        syntagm_pitch.append(file.read_pitch(syntagm))
        syntagm_intensity.append(file.read_intensity(syntagm))
    file.annotate(syntagm_pitch, syntagm_intensity, file_path)