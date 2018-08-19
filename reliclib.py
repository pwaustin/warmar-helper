class Relic:
    def __init__(self, name):
        self.name = name
        self.quality = ''
        self.commons = []
        self.uncommons = []
        self.rare = ""

    def change_quality(self, quality):
        self.quality = quality

    def add_common(self, common):
        self.commons.append(common)

    def add_uncommon(self, uncommon):
        self.uncommons.append(uncommon)

    def add_rare(self, rare):
        self.rare = rare


def generate_relics(datafile):
    results = []
    file = open(datafile, 'r')
    for line in file:
        line = line.strip()
        fields = line.split(',')

        temp = Relic(fields[0])
        temp.add_common(fields[1])
        temp.add_common(fields[2])
        temp.add_common(fields[3])
        temp.add_uncommon(fields[4])
        temp.add_uncommon(fields[5])
        temp.add_rare(fields[6])

        results.append(temp)

    file.close()
    return results

