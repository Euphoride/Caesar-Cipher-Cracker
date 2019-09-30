# The alphabet
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Caesar Cipher Encryption Function
def encrypt(data, key, letterIDLookup):
    lettersData = list(data)

    ciphertext = ""

    for letter in lettersData:
        if letter not in list("abcdefghijklmnopqrstuvwxyz"):
            noForLetter = letterIDLookup[str(hash(letter))]

            noForLetter = (noForLetter + key) % 26

            cipherLetter = letterIDLookup[noForLetter]

            ciphertext = ciphertext + cipherLetter
        else:
            ciphertext = ciphertext + letter

    return(ciphertext)

# Caesar Cipher Decryption Function
def decrypt(data, key, letterIDLookup):
    lettersData = list(data)

    plaintext = ""

    for letter in lettersData:
        if letter in list("abcdefghijklmnopqrstuvwxyz"):
            noForLetter = letterIDLookup[str(hash(letter))]

            noForLetter = (noForLetter - key) % 26

            cipherLetter = letterIDLookup[noForLetter]

            plaintext = plaintext + cipherLetter
        else:
            plaintext = plaintext + letter

    return(plaintext)

# Define lookup table for letters
def initLookupLetters(letters):
    newDict = {}

    count = 0

    for letter in letters:
        newDict[str(hash(letter))] = count
        newDict[count]  = letter
        count += 1

    return(newDict)

# Chi Squared Tests
def chiSquaredTest(disLookup, letters, letterIDLookup, ciphertext):
    keyRange = len(letters)

    chiSquaredPerKey = {}

    for key in range(keyRange):
        possiblePlainText = decrypt(ciphertext, key, letterIDLookup)

        chiSquared = 0

        for letter in letters:
            count = 0
            for character in possiblePlainText:
                if letter == character:
                    count += 1

            disLetterCount = disLookup[letter]

            letterCount = (count / len(possiblePlainText)) * 100

            chiSquared = chiSquared + (((letterCount - disLetterCount) ** 2) / disLetterCount)

        chiSquaredPerKey[key] = chiSquared

    return(chiSquaredPerKey)

# Assess probabilities of each key being the right key
def assessProbabilities(chiSquaredDict):
    keys = len(chiSquaredDict)

    # It's weird. First it should find the total for the chiSquared, then calculate
    # probabilities "normally" (largest gets highest probabilities), then invert it
    totalChi = 0

    # total the chi
    for key in range(keys):
        totalChi = totalChi + chiSquaredDict[key]

    probabilitiesInv = []

    # Find inverted probabilities
    for key in range(keys):
        # * 1000 to try to amplify the difference between the right key and the wrong keys
        # allowing for better distinction
        probabilitiesInv.append((chiSquaredDict[key] / totalChi) * 1000)

    probabilities = []

    # Find probabilities (invert by 100-)
    for prob in probabilitiesInv:
        probabilities.append(100 - prob)

    return(probabilities)
