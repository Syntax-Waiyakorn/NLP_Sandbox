class Character:
    def __init__(self, char, position, cluster_role, char_role, before, after):
        self.char = char
        self.position = position
        self.cluster_role = cluster_role
        self.char_role = char_role
        self.before = before
        self.after = after
    def getInformation(self):
        chars_before = []
        chars_after = []
        for char in self.before:
            chars_before.append(char.char)
        for char in self.after:
            chars_after.append(char.char)
        return f'Character: {self.char}\nPosition: {self.position}\nIn Cluster: {self.cluster_role}\nRole: {self.char_role}\nChracters Before: {chars_before}\nCharacters After: {chars_after}'
    def getBefore(self, distance):
        distance += 1
        if len(self.before) < distance:
            return None
        return self.before[-distance]
    def getAfter(self, distance):
        if len(self.after) < distance:
            return None
        return self.after[distance]

class Syllable:
    def __init__(self, string):
        self.chars = []
        chars = []
        for index, char in enumerate(string):
            thischar = Character(char, index, 'unknown', 'unknown', [], [])
            self.chars.append(thischar)
        for index, char in enumerate(self.chars):
            char.before = self.chars[:index]
            char.after = self.chars[index+1:]
    def getInformation(self):
        information = f''
        return information

class Cluster:
    def __init__(self, cluster_role, chars):
        self.cluster_role = cluster_role
        self.chars = chars
    def findCharRole(self, target_char_role):
        return next((char for char in self.chars if char.char_role == target_char_role), None)