# jack elder
# creates dictionary based on csv file for good / bad words
def create_dict(textfile):
    file = open(textfile, "r")
    dictionary = {}
    for line in file:
        s = line.strip()
        sp = s.split(",")
        dictionary[sp[0]] = sp[1]
    return dictionary

create_dict("dict.txt")