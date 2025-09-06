import mytextgrid as mtg
import parselmouth
from os import path

class Annotation:

    def __init__(self, file):
        self.tg = mtg.read_from_file(file)
        self.snd = parselmouth.Sound(path.splitext(file)[0] + '.wav')
        self.syntagms = []

    def sentence_read(self):
        for interval in self.tg[0]:
            if len(interval.text) > 1:
                sentence_lb = interval.xmin
                sentence_rb = interval.xmax
                self.snd_sentence = self.snd.extract_part(from_time=sentence_lb, to_time=sentence_rb, preserve_times=True)
                return self.snd_sentence

    def syllabe(self, point, xs, values):
        print('snd:', list(values))
        print('len:', len(list(values)))
        time = xs[list(values).index(point)]
        print('time:', time)
        for interval in self.tg[2]:
            print('xmin:', interval.xmin)
            if time >= interval.xmin and time <= interval.xmax:
                return list(self.tg.tiers[2]).index(interval), interval.text

    def read_pitch(self, snd):
        raw_pitch = snd.to_pitch().selected_array['frequency']
        pitch = list(filter(lambda x: x != 0, raw_pitch))
        print(pitch)
        max_pitch = max(pitch)
        min_pitch = min(pitch)
        print('minp: ', min_pitch)
        max_syll = self.syllabe(max_pitch, snd.to_pitch().xs(), raw_pitch)
        min_syll = self.syllabe(min_pitch, snd.to_pitch().xs(), raw_pitch)
        return max_syll, min_syll

    def read_intensity(self, snd):
        intensity = snd.to_intensity()
        max_intensity = max(intensity.values.T)
        min_intensity = min(intensity.values.T)
        print('max: ', max_intensity)
        max_syll = self.syllabe(max_intensity, intensity.xs(), intensity.values.T)
        min_syll = self.syllabe(min_intensity, intensity.xs(), intensity.values.T)
        return max_syll, min_syll

    def syntagm_read(self, syntagm):
        for interval in self.tg.tiers[1]:
            if len(interval.text) > 1:
                syntagm_lb = interval.xmin
                syntagm_rb = interval.xmax
                snd_syntagm = self.snd.extract_part(from_time=syntagm_lb, to_time=syntagm_rb,
                                                         preserve_times=True)
                self.syntagms.append(snd_syntagm)
        return self.syntagms

    def annotate_sentence(self, pitch, intensity, file_path):
        print(pitch, intensity)
        self.tg.tiers[2].set_text_at_index(pitch[0][0], pitch[0][1] + ' HP!')
        self.tg.tiers[2].set_text_at_index(pitch[1][0], pitch[1][1] + ' LP!')
        self.tg.tiers[2].set_text_at_index(intensity[0][0], intensity[0][1] + ' HI!')
        self.tg.tiers[2].set_text_at_index(intensity[1][0], intensity[0][1] + ' LI!')
        self.tg.write(file_path)

    def __del__(self):
        pass

file_path = r'C:\Users\Пользователь\Desktop\Учеба\РАЗНОЕ ПО КОРПУСУ\Кумандинский резерв\2_СНС.TextGrid'
file = Annotation(file_path)
sentence = file.sentence_read()
sentence_pitch = file.read_pitch(sentence)
sentence_intensity = file.read_intensity(sentence)
file.annotate_sentence(sentence_pitch, sentence_intensity, file_path)
