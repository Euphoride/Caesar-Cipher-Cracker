# This script is designed to break any caesar cipher

# Nearly everything is relative

from caesarlib import *

# User IO
print("Caesar Cipher Cracker")

print("Please enter the ciphertext:")

ciphertext = input(">> ").lower()

# Right so first it's probably worth loading in the preset file for generic
# english letter distribution
englishDisFileObject = open("englishDis.txt", "r")
disTable             = englishDisFileObject.read()

# Then split it into an array, where each element is "letter freqency"
disTable = disTable.split("\n")

# Define new distribution lookup table
disLookup = {}

for dis in disTable:
    if dis != "":
        # Split as per the tab between the letter and the frequency
        dis = dis.split("\t")

        # Add to lookup to the template letter: freqency
        disLookup[dis[0].lower()] = float(dis[1])


# A few tests
dict = initLookupLetters(letters)
chiSquaredDict = chiSquaredTest(disLookup, letters, dict, ciphertext)
probs = assessProbabilities(chiSquaredDict)

print("Probabilities:")

# Counts for output and lookup table for sorting
count = 0
keyProbLookup = {}

for prob in probs:
    print("For key " + str(count) + ": " + str(prob) + "%")
    keyProbLookup[count] = prob


    count = count + 1

# Sort the lookup table into tuples, in decending order
sortedLookup = sorted(keyProbLookup.items(), key=lambda x: x[1], reverse=True)

# ~output~
print("\n\n")
print("5 Most Probable Keys:")
print("")
for x in range(5):
    sortedLookupSlice = sortedLookup[x]

    print("Key: " + str(sortedLookupSlice[0]) + " with probability " + str(sortedLookupSlice[1]) + "%")
    print("Decryption: " + decrypt(ciphertext, sortedLookupSlice[0], dict))
    print("")

input()
