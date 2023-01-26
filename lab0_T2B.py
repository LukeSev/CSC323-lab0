import ciphersXOR
import converting

def scorePlaintext(plaintext):
    # Scores English plaintext based on how much it "adheres" to a message from the english language
    # It achieves this using frequency analysis by sorting all letters by their frequency

    # First perform frequency analysis
    freqDict = {}
    for letter in plaintext.lower():
        freq = freqDict.get(letter)
        if(freq is None):
            freqDict[letter] = 1
        else:
            freqDict[letter] += 1

    # Now sort by frequency
    freqs = sorted(freqDict)
    # Create dictionary that assigns values by frequency of letter, so the most common letter, e, gets 26 and the least common letter, q, gets 1
    scoreDict = {'e':26, 'a': 25, 'r':24, 'i':23, 'o':22, 't':21, 'n':20, 's':19, 'l':18, 'c':17, 'u':16, 'd':15, 'p':14, 
    'm':13, 'h':12, 'g':11, 'b':10, 'f':9, 'y':8, 'w':7, 'k':6, 'v':5, 'x':4, 'z':3, 'j':2, 'q':1}

    i = 0
    score = 0
    # Score the top 5 most frequent
    while(i < 5 and i < len(freqs)):
        c = freqs[i]
        curr = scoreDict.get(c)
        if(curr is None):
            # Invalid letter, do nothing
            score += 0
        else:
            score += (scoreDict.get(c) ** 2)
        i += 1
    # Finally, check if it's printable
    if(plaintext.rstrip().isprintable()): # Remove newline char
        score *= 100
    return score

def scoreEngPlaintext(plaintext):
    # If plaintext doesn't contain printable ascii, throw it out

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
    for letter in plaintext.lower():
        freq = freqDict.get(letter)
        flag = scoreDict.get(letter)
        if(flag is not None): # Only add if it's a character with a score
            if(freq is None):
                freqDict[letter] = 1
            else:
                freqDict[letter] += 1

    # Now sort by frequency
    #freqs = sorted(freqDict)

    #print(freqDict)
    # Now that we have both the frequencies of our plaintext and the frequencies of the English language, let's compare
    # To do so, we'll sum all the differences between the frequencies and divide by the number of characters encountered
    sum = 0
    for freq in freqDict:
        sum += abs(freqDict[freq] - scoreDict[freq])
    avg_diff = sum / len(freqDict)

    # Smaller deviation means a closer adherence to english language, so we want reciprocal relationship with our avg_diff
    return 1 / avg_diff


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

    lineScores = {}
    for val in range(256):
        # Analyze each line
        for line in lines:
            # First xor to try to decode
            try:
                plaintext = ciphersXOR.xor_bytestrings(bytes.fromhex(line), val).decode()
                score = scoreEngPlaintext(plaintext)
                if(score > 500): # Only add plaintext to dictionary if it at least somewhat resembles English
                    lineScores[plaintext] = score
            except UnicodeError:
                failed = True
    
    # Once all scores have been generated, print the lines with the highest score
    topLines = sorted(lineScores.items(), key=lambda x:x[1], reverse=True)
    j = 0
    b = 0
    while((j < 5) and (j < len(topLines))):
        currLine = topLines[j] # Will give us tuple with both the line and its score
        print("\n\nSCORE POSITION: " + str(j+1))
        print("SCORE: " + str(currLine[1]))
        print(currLine[0] + "\n\n")
        j += 1

def main():
    byteXOR("Lab0.TaskII.B.txt")
    #byteXOR("test.txt")

if __name__ == '__main__':
    main()
