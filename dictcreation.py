# jack elder
# creates dictionary based on csv file for good / bad words
tweets = open("dict.txt", "r")
wavelength_dictionary = {}

for line in tweets:
    s = line.strip()
    sp = s.split(",")
    wavelength_dictionary[sp[0]] = sp[1]
