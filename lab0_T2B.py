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
        #print("Processing byte: " + str(val))
        # Analyze each line
        for line in lines:
            # First xor to try to decode
            try:
                plaintext = ciphersXOR.xor_bytestrings(bytes.fromhex(line), val).decode()
                #plaintext = ciphersXOR.xor_bytestrings(bytes.fromhex(line), bite).decode()
                score = scorePlaintext(plaintext)
                #print(plaintext)
                lineScores[plaintext] = score
            except UnicodeError:
                failed = True
    
    # Once all scores have been generated, print the lines with the highest score
    topLines = sorted(lineScores.items(), key=lambda x:x[1], reverse=True)
    j = 0
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
