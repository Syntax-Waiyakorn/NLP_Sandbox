# from classes import Character, Syllable

from dict import *

class Character():
    def __init__(self, char, syllable, position, before=[], after=[], cluster='unknown', char_role='unknown'):
        self.char = char
        self.position = position
        self.syllable = syllable
        self.before = before
        self.after = after
        self.cluster = cluster
        self.role = char_role
        for consonant_class_key in CONSONANT_CLASSES.keys():
            if self.char in CONSONANT_CLASSES[consonant_class_key]:
                self.consonant_class = consonant_class_key
    def getInformation(self):
        chars_before = []
        chars_after = []
        for char in self.before:
            chars_before.append(char.char)
        for char in self.after:
            chars_after.append(char.char)
        return f'''
            Character: {self.char}
            In Syllable: {self.syllable.string}
            Position: {self.position}
            Class: {self.consonant_class}
            In Cluster: {self.cluster}
            Role: {self.role}\nChracters Before: {chars_before}\nCharacters After: {chars_after}
            '''
    def getBefore(self, distance):
        distance += 1
        if len(self.before) < distance:
            return None
        return self.before[-distance]
    def getAfter(self, distance):
        if len(self.after) <= distance:
            return None
        return self.after[distance]
    def selfCluster(self, cluster):
        return self.syllable.assignCluster(self, cluster)
    def selfRole(self, role):
        return self.syllable.assignRole(self, role)

class Syllable:
    def __init__(self, string):
        self.string = string
        self.chars = []
        
        self.initial_vowels_cluster = []
        self.initial_consonants_cluster = []
        self.tone_marks_cluster = []
        self.final_vowels_cluster = []
        self.final_consonants_cluster = []

        self.leading_consonants = []
        self.initial_consonants = []
        self.blending_consonants = []
        self.vowels = []
        self.tone_marks = []
        self.final_consonants = []
        self.silent_characters = []

        self.initial_sound = ''
        self.initial_class = ''
        self.final_sound = ''

        self.vowel_default = ''
        self.vowel_duration = ''
        self.vowel_short = ''

        self.vowel_long = ''
        
        self.live_dead = ''

        self.tone_mark = ''
        self.tone = ''

        for index, char in enumerate(string):
            thischar = Character(char, self, index)
            self.chars.append(thischar)
        for index, char in enumerate(self.chars):
            char.before = self.chars[:index]
            char.after = self.chars[index+1:]
    def getInformation(self):
        initial_vowels = []
        initial_consonants = []
        tone_marks = []
        final_vowels = []
        final_consonants = []
        initial_vowels_roles = []

        vowels = []

        for char in self.initial_vowels_cluster:
            initial_vowels.append([char.char, char.role])
        for char in self.initial_consonants_cluster:
            initial_consonants.append([char.char, char.role])
        for char in self.tone_marks_cluster:
            tone_marks.append([char.char, char.role])
        for char in self.final_vowels_cluster:
            final_vowels.append([char.char, char.role])
        for char in self.final_consonants_cluster:
            final_consonants.append([char.char, char.role])

        for char in self.getVowel():
            vowels.append(char.char)

        information = f'''
            Syllable String: {self.string}
            Initial Vowels Cluster: {initial_vowels}
            Initial Consonants Cluster: {initial_consonants}
            Tone Marks Cluster: {tone_marks}
            Final Vowels Cluster: {final_vowels}
            Final Consonants Cluster: {final_consonants}

            Initial Sound: {self.initial_sound}
            Inital Class: {self.initial_class}
            Final Sound: {self.final_sound}
            
            Vowel Form: {vowels}
            Vowel Default Form: {self.vowel_default}
            Vowel Duration: {self.vowel_duration}

            Vowel Short Form: {self.vowel_short}
            Vowel Long Form: {self.vowel_long}

            Live/Dead: {self.live_dead}

            Tone Mark: {self.tone_mark}
            Tone: {self.tone}
            '''
        return information
    def assignCluster(self, char, cluster):
        if cluster == 'initial_vowels_cluster':
            char.cluster = cluster
            self.initial_vowels_cluster.append(char)
        elif cluster == 'initial_consonants_cluster':
            char.cluster = cluster
            self.initial_consonants_cluster.append(char)
        elif cluster == 'tone_marks_cluster':
            char.cluster = cluster
            self.tone_marks_cluster.append(char)
        elif cluster == 'final_vowels_cluster':
            char.cluster = cluster
            self.final_vowels_cluster.append(char)
        elif cluster == 'final_consonants_cluster':
            char.cluster = cluster
            self.final_consonants_cluster.append(char)
        else:
            return None
    def assignRole(self, char, role):
        if role == 'leading_consonant':
            char.role = role
            self.leading_consonants.append(char)
        elif role == 'initial_consonant':
            char.role = role
            self.initial_consonants.append(char)    
        elif role == 'blending_consonant':
            char.role = role
            self.blending_consonants.append(char)
        elif role == 'vowel':
            char.role = role
            self.vowels.append(char)
        elif role == 'tone_mark':
            char.role = role
            self.tone_marks.append(char)
        elif role == 'final_consonant':
            char.role = role
            self.final_consonants.append(char)
        elif role == 'silent_character':
            char.role = role
            self.silent_characters.append(char)
        else:
            return None
    def getVowel(self):
        return self.initial_vowels_cluster + self.final_vowels_cluster
    def getVowelString(self):
        vowel_string = ''
        for char in self.getVowel():
            vowel_string = vowel_string + char.char
        return vowel_string

def find_initial_vowels_cluster(syllable):
    initial_vowels = []
    current_index = 0
    if syllable.chars[0].char in INITIAL_VOWELS:
        initial_vowels = [syllable.chars[0]]
        current_index += 1

    return [current_index, initial_vowels]

def find_initial_consonants_cluster(syllable, current_index, ee_initial, ay_initial):
    w_vowel = False

    first_consonant = syllable.chars[current_index]

    initial_consonants = [first_consonant]
    current_index += 1

    if first_consonant.getAfter(0):
        potential_second_consonant = first_consonant.getAfter(0)
        if potential_second_consonant.char in CONSONANTS:

            if potential_second_consonant.char == 'อ':
                return [current_index, initial_consonants, w_vowel]
            
            if potential_second_consonant.char == 'ย' and (ee_initial or ay_initial):
                return [current_index, initial_consonants, w_vowel]

            if potential_second_consonant.char == 'ร' or potential_second_consonant.char == 'ล':
                if first_consonant.char in R_L_BLENDING_INITIALS:
                    initial_consonants.append(potential_second_consonant)
                    current_index += 1
                    return [current_index, initial_consonants, w_vowel]
            
            if potential_second_consonant.char == 'ว':
                if first_consonant.char not in W_BLENDING_INITIALS:
                    return [current_index, initial_consonants, w_vowel]
                for chars in syllable.chars:
                    if chars.char in VOWELS:
                        initial_consonants.append(potential_second_consonant)
                        current_index += 1
                        return [current_index, initial_consonants, w_vowel]
                w_vowel = True
                return [current_index, initial_consonants, w_vowel]
            
            if potential_second_consonant.getAfter(0):
                if potential_second_consonant.char == 'ร' and potential_second_consonant.getAfter(0).char == 'ร':
                    return [current_index, initial_consonants, w_vowel]
                if first_consonant.char == 'อ' and potential_second_consonant.char == 'ย' or \
                    first_consonant.char == 'ห' and potential_second_consonant.char in UNPAIRED_LOW_CONSONANTS:
                    initial_consonants.append(potential_second_consonant)
                    current_index += 1
                    return [current_index, initial_consonants, w_vowel]
                if potential_second_consonant.char not in BLENDING_CONSONANTS:
                    return [current_index, initial_consonants, w_vowel]
                initial_consonants.append(potential_second_consonant)
                current_index += 1
                return [current_index, initial_consonants, w_vowel]
            
            return [current_index, initial_consonants, w_vowel]

    return [current_index, initial_consonants, w_vowel]

def find_final_vowels_and_tone_marks_clusters(syllable, current_index, ee_initial, ay_initial, w_vowel):
    final_vowels = []
    tone_marks = []

    if len(syllable.chars) <= current_index:
        return [current_index, final_vowels, tone_marks]

    def append_loop(first_index, final_index):
        final_index += 1
        for index in range(first_index, final_index):
            if syllable.chars[index].char in TONE_MARKS:
                tone_marks.append(syllable.chars[index])
                continue
            final_vowels.append(syllable.chars[index])
        return final_index

    for potential_a_index in range(current_index, len(syllable.chars)):
        if syllable.chars[potential_a_index].char == 'ะ':
            current_index = append_loop(current_index, potential_a_index)
            return [current_index, final_vowels, tone_marks]
    
    for potential_oo_index in range(current_index, len(syllable.chars)):
        if syllable.chars[potential_oo_index].char == 'อ':
            current_index = append_loop(current_index, potential_oo_index)
            return [current_index, final_vowels, tone_marks]
    
    for potential_y_index in range(current_index, len(syllable.chars)):
        if syllable.chars[potential_y_index].char == 'ย':
            y = syllable.chars[potential_y_index]
            if ay_initial:
                current_index = append_loop(current_index, potential_y_index)
                return [current_index, final_vowels, tone_marks]
            if ee_initial:
                for potential_ii_index in range(current_index, potential_y_index):
                    if syllable.chars[potential_ii_index].char == 'ี':
                        current_index = append_loop(current_index, potential_y_index)
                        return [current_index, final_vowels, tone_marks]
                if y.getAfter(0):
                    if y.getAfter(0).char == '์':
                        break
                current_index = append_loop(current_index, potential_y_index)
                return [current_index, final_vowels, tone_marks]

    after0_char = ''
    if current_index + 1 < len(syllable.chars):
        after0_char = syllable.chars[current_index].getAfter(0).char

    after1_char = ''
    if current_index + 2 < len(syllable.chars):
        after1_char = syllable.chars[current_index].getAfter(1).char

    if syllable.chars[current_index].char == 'ฤ':
        final_vowels.append(syllable.chars[current_index])
        current_index += 1
        return [current_index, final_vowels, tone_marks]

    if syllable.chars[current_index].char == 'ร' and after0_char == 'ร':
        final_vowels.append(syllable.chars[current_index])
        final_vowels.append(syllable.chars[current_index].getAfter(0))
        current_index += 2
        return [current_index, final_vowels, tone_marks]

    if (syllable.chars[current_index].char in TONE_MARKS and after0_char == 'ว') or \
        (syllable.chars[current_index].char == 'ั' and after0_char == 'ว') or \
        (syllable.chars[current_index].char == 'ั' and after0_char in TONE_MARKS and after1_char == 'ว'):
            w_vowel = True

    if w_vowel:
        w_index = None
        for potential_w_index in range(current_index, len(syllable.chars)):
            if syllable.chars[potential_w_index].char == 'ว':
                w_index = potential_w_index
        current_index = append_loop(current_index, w_index)
        return [current_index, final_vowels, tone_marks]
    
    if syllable.chars[current_index].char in TONE_MARKS and after0_char in VOWELS:
        tone_marks.append(syllable.chars[current_index])
        final_vowels.append(syllable.chars[current_index].getAfter(0))
        current_index += 2
        return [current_index, final_vowels, tone_marks]
    
    if syllable.chars[current_index].char in VOWELS:
        final_vowels.append(syllable.chars[current_index])
        current_index += 1
        return [current_index, final_vowels, tone_marks]
    
    if syllable.chars[current_index].char in TONE_MARKS:
        tone_marks.append(syllable.chars[current_index])
        current_index += 1
        return [current_index, final_vowels, tone_marks]

    return [current_index, final_vowels, tone_marks]

def find_final_consonants_cluster(syllable, current_index):
    return syllable.chars[current_index:]

def extract_clusters(syllable):
    ee_initial = False
    ay_initial = False

    initial_vowels_cluster_info = find_initial_vowels_cluster(syllable)
    current_index = initial_vowels_cluster_info[0]
    initial_vowels_cluster = initial_vowels_cluster_info[1]

    if initial_vowels_cluster:
        if initial_vowels_cluster[0].char == 'เ':
            ee_initial = True
        if initial_vowels_cluster[0].char == 'ไ':
            ay_initial = True

    initial_consonants_cluster_info = find_initial_consonants_cluster(syllable, current_index, ee_initial, ay_initial)
    current_index = initial_consonants_cluster_info[0]
    initial_consonants_cluster = initial_consonants_cluster_info[1]
    w_vowel = initial_consonants_cluster_info[2]

    final_vowels_and_tone_marks_clusters_info = find_final_vowels_and_tone_marks_clusters(syllable, current_index, ee_initial, ay_initial, w_vowel)
    current_index = final_vowels_and_tone_marks_clusters_info[0]
    final_vowels_cluster = final_vowels_and_tone_marks_clusters_info[1]
    tone_marks_cluster = final_vowels_and_tone_marks_clusters_info[2]

    final_consonants_cluster = find_final_consonants_cluster(syllable, current_index)

    for char in initial_vowels_cluster:
        char.selfCluster('initial_vowels_cluster')
    for char in initial_consonants_cluster:
        char.selfCluster('initial_consonants_cluster')
    for char in tone_marks_cluster:
        char.selfCluster('tone_marks_cluster')
    for char in final_vowels_cluster:
        char.selfCluster('final_vowels_cluster')
    for char in final_consonants_cluster:
        char.selfCluster('final_consonants_cluster')

def extract_initial_consonants_cluster(syllable):
    initial_consonants_cluster = syllable.initial_consonants_cluster

    if len(initial_consonants_cluster) == 1:
        initial_consonants_cluster[0].selfRole('initial_consonant')
        return

    if (initial_consonants_cluster[0].char == 'ห' or initial_consonants_cluster[0].char == 'อ') and \
        initial_consonants_cluster[1].char in UNPAIRED_LOW_CONSONANTS:
        initial_consonants_cluster[0].selfRole('leading_consonant')
        initial_consonants_cluster[1].selfRole('initial_consonant')
        return
    
    initial_consonants_cluster[0].selfRole('initial_consonant')
    initial_consonants_cluster[1].selfRole('blending_consonant')

def extract_final_consonants_cluster(syllable):
    final_consonants_cluster = syllable.final_consonants_cluster

    if not final_consonants_cluster:
        return
    
    if len(final_consonants_cluster) == 2 and final_consonants_cluster[-1].char == '์':
        final_consonants_cluster[-1].selfRole('silent_character')
        final_consonants_cluster[-2].selfRole('silent_character')
        return
    if len(final_consonants_cluster) == 2 and final_consonants_cluster[0].char == 'ร':
        final_consonants_cluster[0].selfRole('silent_character')
        final_consonants_cluster[1].selfRole('final_consonant')
        return
    
    final_consonants_cluster[0].selfRole('final_consonant')
    for char in final_consonants_cluster[1:]:
        char.selfRole('silent_character')

def extract_roles(syllable):
    for char in syllable.initial_vowels_cluster + syllable.final_vowels_cluster:
        char.selfRole('vowel')
    for char in syllable.tone_marks_cluster:
        char.selfRole('tone_mark')
    extract_initial_consonants_cluster(syllable)
    extract_final_consonants_cluster(syllable)
    return

def process_initial_sound(syllable):
    for initial_sound_key in INITIAL_SOUNDS.keys():
        if syllable.initial_consonants[0].char in INITIAL_SOUNDS[initial_sound_key]:
            syllable.initial_sound = initial_sound_key

def process_initial_class(syllable):
    syllable.initial_class = syllable.initial_consonants_cluster[0].consonant_class
    
def get_default_vowel(vowel_string):
    for vowel_forms_key in VOWEL_FORMS.keys():
        if vowel_string in VOWEL_FORMS[vowel_forms_key]:
            return vowel_forms_key
    
def process_vowel(syllable):
    vowel_string = syllable.getVowelString()
    if not vowel_string:
        if not syllable.final_consonants:
            syllable.vowel_default = '-ะ'
        else:
            syllable.vowel_default = 'โ-ะ'
    else:
        syllable.vowel_default = get_default_vowel(vowel_string)

    if syllable.vowel_default in SHORT_LONG_VOWEL_PAIRS.get_forward_keys():
        syllable.vowel_duration = 'short'
        syllable.vowel_short = syllable.vowel_default
        syllable.vowel_long = SHORT_LONG_VOWEL_PAIRS[syllable.vowel_default]
    else:
        syllable.vowel_duration = 'long'
        syllable.vowel_short = SHORT_LONG_VOWEL_PAIRS.reverse_get(syllable.vowel_default)
        syllable.vowel_long = syllable.vowel_default
    return

def process_final_sound(syllable):
    final_sound = '-'
    vowel_string = syllable.getVowelString()
    if not vowel_string:
        syllable.final_sound = final_sound
        return
    if not syllable.final_consonants:
        if vowel_string[-1] == 'ำ':
            final_sound = 'ม'
        if vowel_string[0] == 'ไ' or vowel_string[0] == 'ใ':
            final_sound = 'ย'
        if vowel_string[0] == 'เ' and vowel_string[1] == 'า':
            final_sound = 'ว'
        syllable.final_sound = final_sound
        return final_sound
    for final_sound_key in FINAL_SOUNDS.keys():
        if syllable.final_consonants[0].char in FINAL_SOUNDS[final_sound_key]:
            final_sound = final_sound_key
    syllable.final_sound = final_sound
    return final_sound

def process_live_dead(syllable):
    if syllable.final_sound == '-':
        if syllable.vowel_duration == 'short':
            syllable.live_dead = 'dead'
        if syllable.vowel_duration == 'long':
            syllable.live_dead = 'live'
        return
    if syllable.final_sound in DEAD_FINAL_SOUNDS:
        syllable.live_dead = 'dead'
    elif syllable.final_sound in LIVE_FINAL_SOUNDS:
        syllable.live_dead = 'live'

def process_tone_mark(syllable):
    if not syllable.tone_marks:
        return
    syllable.tone_mark = syllable.tone_marks[0].char

def process_tone(syllable):
    syllable.tone = 'uncalculable'
    if ((syllable.initial_class == 'mid' or syllable.initial_class == 'low') and syllable.live_dead == 'live' and not syllable.tone_mark):
        syllable.tone = 'mid'
        print('mid')
    if  ((syllable.initial_class == 'mid' or syllable.initial_class == 'high') and syllable.live_dead == 'live' and syllable.tone_mark == '่') or \
        ((syllable.initial_class == 'mid' or syllable.initial_class == 'high') and syllable.live_dead == 'dead' and not syllable.tone_mark):
        syllable.tone = 'low'
        print('low')
    if ((syllable.initial_class == 'mid' or syllable.initial_class == 'high') and syllable.tone_mark == '้') or \
        (syllable.initial_class == 'low' and syllable.live_dead == 'live' and syllable.tone_mark == '่') or \
        (syllable.initial_class == 'low' and syllable.live_dead == 'dead' and syllable.vowel_duration == 'short' and syllable.tone_mark == '่') or \
        (syllable.initial_class == 'low' and syllable.live_dead == 'dead' and syllable.vowel_duration == 'long' and not syllable.tone_mark):
        syllable.tone = 'falling'
        print('falling')
    if (syllable.initial_class == 'mid' and syllable.tone_mark == '๊') or \
        (syllable.initial_class == 'low' and syllable.live_dead == 'live' and syllable.tone_mark == '้') or \
        (syllable.initial_class == 'low' and syllable.live_dead == 'dead' and syllable.vowel_duration == 'long' and syllable.tone_mark == '้') or \
        (syllable.initial_class == 'low' and syllable.live_dead == 'dead' and syllable.vowel_duration == 'short' and not syllable.tone_mark):
        syllable.tone = 'high'
        print('high')
    if (syllable.initial_class == 'mid' and syllable.tone_mark == '๋') or \
        (syllable.initial_class == 'low' and syllable.live_dead == 'dead' and syllable.tone_mark == '๋') or \
        (syllable.initial_class == 'high' and syllable.live_dead == 'live' and not syllable.tone_mark):
        syllable.tone = 'rising'
        print('rising')
    return
    
syllable = Syllable('กลัว')
print(f'Syllable Length: {len(syllable.chars)}')
extract_clusters(syllable)
extract_roles(syllable)
process_initial_sound(syllable)
process_initial_class(syllable)
process_final_sound(syllable)
process_vowel(syllable)
process_live_dead(syllable)
process_tone_mark(syllable)
process_tone(syllable)
print(syllable.getInformation())