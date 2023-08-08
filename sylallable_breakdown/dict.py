th_chars = {
    'consonants': {
        'low_classes': {
            'low_paireds': {'ค','ฅ','ฆ','ช','ซ','ฌ','ฑ','ฒ','ท','ธ','พ','ฟ','ภ','ฮ'},
            'low_unpaireds': {'ง','ญ','ณ','น','ม','ย','ร','ฤ','ล','ฦ','ว','ฬ'}
            },
        'mid_classes': {'ก','จ','ฎ','ฏ','ด','ต','บ','ป','อ'},
        'high_classes': {'ข','ฃ','ฉ','ฐ','ถ','ผ','ฝ','ศ','ษ','ส','ห'},
        'blends': {'ร','ล','ว'}
    },
    'vowels': {'ะ','ั','า','ำ','ิ','ี','ึ','ื','ุ','ู','เ','แ','โ','ใ','ไ','็','ๅ'},
    'diacritics': {
        'tones': {'่','้','๊','๋'},
        'others': {'์'},
    },
    'symbols': {
        'modifies': {'ๆ','ฺ'},
        'numbers': {'๐','๑','๒','๓','๔','๕','๖','๗','๘','๙'},
        'others': {'ฯ','฿'}
    }
}

th_utils = {
    'poly_initials': {'แ','เ','โ','ั'},
    'poly_follows': {
      'แ': {'ะ','็'},
      'เ': {'ะ','า','ี','ื','็'},
      'โ': {'ะ'},
      'ั': {'ะ'}
    },
    'blend_initials': {
        'ร': {'ก','ข','ค','ต','ป','พ'},
        'ล': {'ก','ข','ค','ผ','ป','พ'},
        'ว': {'ก','ข','ค'}
    }
}

consonants = ['ก', 'ข', 'ฃ', 'ค', 'ฅ', 'ฆ', 'ง', 'จ', 'ฉ', 'ช',
    'ซ', 'ฌ', 'ญ', 'ฎ', 'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ', 'ด',
    'ต', 'ถ', 'ท', 'ธ', 'น', 'บ', 'ป', 'ผ', 'ฝ', 'พ',
    'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ฤ', 'ล', 'ฦ', 'ว', 'ศ',
    'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ']
vowels = ['ิ', 'ี', 'ึ', 'ื', 'ๅ', 'ุ', 'ู', 'เ', 'โ', 'แ',
    'ะ', 'ั', 'า', 'ำ', 'ใ', 'ไ', '็']
tone_marks = ['่','้','๊','๋']


low_consonants = []
unpaired_low_consonants = []
paired_low_consonants = []
high_consonants = []
mid_consonants = []

leading_consonants = ['ห','อ']

blends = []
blend_initials = []

class ThaiCharDict:
    def __init__(self, consonants, vowels, tone_marks,
            low_consonants, unpaired_low_consonants, paired_low_consonants, high_consonants, mid_consonants,
            leading_consonants,
            blends, blend_initials):
        self.low_consonants = low_consonants
        self.unpaired_low_consonants = unpaired_low_consonants
        self.paired_low_consonants = paired_low_consonants
        self.high_consonants = high_consonants
        self.mid_consonants = mid_consonants

        self.leading_consonants = leading_consonants

th_all = ThaiCharDict(consonants, vowels, tone_marks,
            low_consonants, unpaired_low_consonants, paired_low_consonants, high_consonants, mid_consonants,
            leading_consonants,
            blends, blend_initials)