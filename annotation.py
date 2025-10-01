import mytextgrid as mtg
import parselmouth
from os import path

class Annotation:

    def __init__(self, file):
        self.tg = mtg.read_from_file(file)
        self.snd = parselmouth.Sound(path.splitext(file)[0] + '.wav')
        self.intervals = []
        self.syntagms = file.read_interval(1)
        self.sentence = file.read_interval(0)

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
        max_syll, text_max_syll = self.syllabe(max_pitch, snd.to_pitch().xs(), pitch)
        min_syll, text_min_syll = self.syllabe(min_pitch, snd.to_pitch().xs(), pitch)
        return max_syll, text_max_syll, min_syll, text_min_syll

    def read_intensity(self, snd):
        intensity = snd.to_intensity()
        max_intensity = max(intensity.values.T)
        min_intensity = min(intensity.values.T)
        max_syll, text_max_syll = self.syllabe(max_intensity, intensity.xs(), intensity.values.T)
        min_syll, text_min_syll = self.syllabe(min_intensity, intensity.xs(), intensity.values.T)
        return max_syll, text_max_syll, min_syll, text_min_syll

    def read_interval(self, tier):
        for interval in self.tg.tiers[tier]:
            if len(interval.text) > 1:
                interval_lb = interval.xmin
                interval_rb = interval.xmax
                snd_interval = self.snd.extract_part(from_time=interval_lb, to_time=interval_rb,
                                                         preserve_times=True)
                self.intervals.append(snd_interval)
        return self.intervals

    def chars(self, interval):
        data = {}
        data['max_pitch'], data['max_pitch_text'], data['min_pitch'], data['min_pitch_text'] = self.read_pitch(interval)
        data['max_intensity'], data['max_intensity_text'], data['min_intensity'], data['min_intensity_text'] = self.read_intensity(interval)
        return data

    def __del__(self):
        pass


def annotate(self, file_path):
    file = Annotation(file_path)

    sentence = file.read_interval(0)
    sentence_chars = file.chars(sentence)
    syntagm_tier = file.tg.tiers[2]

    syntagms = file.read_interval(1)
    for syntagm in syntagms:
        syntagm_chars = file.chars(syntagm)
        syntagm_tier.set_text_at_index(syntagm_chars['max_pitch'], syntagm_chars['max_pitch_text'] + ' HP')
        syntagm_tier.set_text_at_index(syntagm_chars['min_pitch'], syntagm_chars['min_pitch_text'] + ' LP')
        syntagm_tier.set_text_at_index(syntagm_chars['max_intensity'], syntagm_chars['max_intensity_text'] + ' HI')
        syntagm_tier.set_text_at_index(syntagm_chars['min_intensity'], syntagm_chars['min_intensity_text'] + ' LI')

    syntagm_tier.set_text_at_index(sentence_chars['max_pitch'], sentence_chars['max_pitch_text'] + '!')
    syntagm_tier.set_text_at_index(sentence_chars['min_pitch'], sentence_chars['min_pitch_text'] + '!')
    syntagm_tier.set_text_at_index(sentence_chars['max_intensity'], sentence_chars['max_intensity_text'] + '!')
    syntagm_tier.set_text_at_index(sentence_chars['min_intensity'], sentence_chars['min_intensity_text']  + '!')

    self.tg.write(file_path)
