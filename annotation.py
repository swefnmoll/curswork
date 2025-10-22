import mytextgrid as mtg
import parselmouth
from os import path

class Annotation:

    def __init__(self, file):
        self.path_to_tg = path.splitext(file)[0] + '.TextGrid'
        self.tg = mtg.read_from_file(self.path_to_tg)
        self.snd = parselmouth.Sound(file)
        self.syntagms = self.read_interval(1)

    def syllabe(self, point, xs, values):
        time = xs[list(values).index(point)]
        for interval in self.tg.tiers[2]:
            if interval.xmin <= time <= interval.xmax:
                return list(self.tg.tiers[2]).index(interval), interval.text

    def read_pitch(self, snd):
        if snd != 0:
            raw_pitch = snd.to_pitch().selected_array['frequency']
            pitch = list(filter(lambda x: x != 0, raw_pitch))
            max_pitch = max(pitch)
            min_pitch = min(pitch)
            max_syll, text_max_syll = self.syllabe(max_pitch, snd.to_pitch().xs(), raw_pitch)
            min_syll, text_min_syll = self.syllabe(min_pitch, snd.to_pitch().xs(), raw_pitch)
            return max_syll, text_max_syll, min_syll, text_min_syll
        else:
            pass

    def cut_hesitation(self, intervals):
        snd_no_hes = []
        for interval in intervals:
            if interval != 0:
                snd_no_hes.append(interval)
        return snd_no_hes

    def read_intensity(self, snd):
        if snd != 0:
            raw_intensity = snd.to_intensity()
            intensity = list(filter(lambda x: x != 0, raw_intensity.values.T))
            max_intensity = max(intensity)
            min_intensity = min(intensity)
            max_syll, text_max_syll = self.syllabe(max_intensity, raw_intensity.xs(), intensity)
            min_syll, text_min_syll = self.syllabe(min_intensity, raw_intensity.xs(), intensity)
            return max_syll, text_max_syll, min_syll, text_min_syll
        else:
            pass

    def read_interval(self, tier):
        intervals = []
        for interval in self.tg.tiers[tier]:
            if (interval.text != '-') and (interval.text != ''):
                interval_lb = interval.xmin
                interval_rb = interval.xmax
                snd_interval = self.snd.extract_part(from_time=interval_lb, to_time=interval_rb,
                                                         preserve_times=True)
                intervals.append(snd_interval)
            else:
                intervals.append(0)
        intervals_no_hes = self.cut_hesitation(intervals)
        return intervals_no_hes

    def chars(self, interval):
        data = {}
        data['HP'], data['HP_text'], data['LP'], data['LP_text'] = self.read_pitch(interval)
        data['HI'], data['HI_text'], data['LI'], data['LI_text'] = self.read_intensity(interval)
        return data

    def __del__(self):
        pass

    def annotate_syntagm(self, parameter, syntagm):
        sentence_chars = self.chars(self.sentence)
        syntagm_chars = self.chars(syntagm)
        if syntagm_chars[parameter] == sentence_chars[parameter]:
            self.syllabe_tier.set_text_at_index(syntagm_chars[parameter], syntagm_chars[parameter + '_text'] + ' ' + parameter + '!')
        else:
            self.syllabe_tier.set_text_at_index(syntagm_chars[parameter], syntagm_chars[parameter + '_text'] + ' ' + parameter)

    def annotate(self):
        self.syllabe_tier = self.tg.tiers[2]
        self.sentence = parselmouth.Sound.concatenate(self.syntagms)
        for syntagm in self.syntagms:
            self.annotate_syntagm('HP', syntagm)
            self.annotate_syntagm('LP', syntagm)
            self.annotate_syntagm('HI', syntagm)
            self.annotate_syntagm('LI', syntagm)
        self.tg.write(self.path_to_tg)
nn = Annotation(r'C:\Users\Пользователь\Desktop\Учеба\РАЗНОЕ ПО КОРПУСУ\Кумандинский резерв\5_СНС.wav')
nn.annotate()