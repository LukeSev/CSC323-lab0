import ciphersXOR
import converting

def scorePlaintext(plaintext):
    # Create dictionary that assigns values of each ascii character's freq
    # Frequency info taken from https://millikeys.sourceforge.net/freqanalysis.html
    # Note: Ignores case
    scoreDict = {' ':0.1874, 'e':0.096, 't':0.0702, 'a':0.0621, 'o':0.0584, 'i':0.0522, 'n':0.0521, 'h':0.0487,
    's':0.0487, 'r':0.0443, 'd': 0.0352, 'l':0.032, 'u':0.0225, 'm':0.0194, 'c':0.0188, 'w':0.0182, 'g':0.0166,
    'f':0.0162, 'y':0.0156, 'p':0.0131, ',':0.0124, '.':0.0121, 'b':0.0119, 'k':0.0074, 'v':0.0071, '"':0.0067, 
    "'":0.0044, '-':0.0026, '?':0.0012, 'x':0.0012, 'j':0.0012, ';':0.0008, '!':0.0008, 'q':0.0007, 'z':0.0007,
    ':':0.0003, '1':0.0002, '_':0.0001, '0':0.0001, ')':0.0001, '*':0.0001, '(':0.0001, '2':0.0001, '`':0.0001,
    '3':0.0001, '9':0.0001, '5':0.0001, '4':0.0001, '8':0.0001, '7':0.0001, '6':0.0001, '/':0.001, '[':0.0001,
    ']':0.0001, '=':0.0001, '>':0.0001, '~':0.0001, '<':0.0001, '#':0.0001, '&':0.0001, '{':0.0001, '}':0.0001,
    '^':0.0001, '|':0.0001, '@':0.0001, '%':0.0001, '$':0.0001}

    # First do freq analysis
    # First perform frequency analysis
    freqDict = {}
    dictSize = 0
    for letter in plaintext.lower():
        freq = freqDict.get(letter)
        valid = scoreDict.get(letter)
        if(valid is None): # Only add if it's a character with a score
            dictSize += 0 # NOP
        else:
            if(freq is None):
                freqDict[letter] = 1
            else:
                freqDict[letter] += 1
            dictSize += 1

    # Now convert to relative frequencies
    for character in freqDict:
        freqDict[character] /= dictSize

    # Now that we have both the frequencies of our plaintext and the frequencies of the English language, let's compare
    # To do so, we'll sum all the differences between the frequencies and divide by the number of characters encountered
    sum = 0
    for freq in freqDict:
        sum += abs((freqDict[freq] - scoreDict[freq])/scoreDict[freq])
    avg_diff = sum / len(freqDict)

    # Smaller deviation means a closer adherence to english language, so we want negative correlation with our avg_diff
    return 1000 / avg_diff

def byteXOR(file):
    infile = open(file, 'r')
    lines = infile.readlines()

    testing = False
    if(testing == True):
        testval = 16
        testlines = []
        for line in lines:
            print("Processing line: " + line + "\n\n")
            testlines.append(ciphersXOR.xor_bytestrings(line.encode(), testval).hex())
            lines = testlines

    # Format: (Key, Plaintext, Score)
    best = (0, "", 0)
    for val in range(256):
        # Analyze each line
        for line in lines:
            # First xor to try to decode
            try:
                plaintext = ciphersXOR.xor_bytestrings(bytes.fromhex(line), val).decode()
                score = scorePlaintext(plaintext)
                if(score > best[2]): # Only add plaintext to dictionary if it at least somewhat resembles English
                    best = (val, plaintext, score)
            except UnicodeError:
                failed = True
    # Line with highest score is most similar to English
    print("Key: {}\nPlaintext:\n{}".format(hex(best[0]), best[1]))
    

def main():
    byteXOR("Lab0.TaskII.B.txt")

if __name__ == '__main__':
    main()
