import ciphersXOR
import converting

def scorePlaintext(plaintext):
    # Scores English plaintext based on how much it "adheres" to a message from the english language
    # It achieves this using frequency analysis by sorting all letters by their frequency
    # The score is generated by taking the 5 most common letters in the English language (e,t,a,i,o) and...
    # ... using their relative position to provide a score...
    # ... so if one of the most common letters is the first in the list it will provide the highest score


    # First perform frequency analysis
    freqDict = {}
    for letter in plaintext:
        freq = freqDict.get(letter)
        if(freq is None):
            freqDict[letter] = 1
        else:
            freqDict[letter] += 1

    # Now sort by frequency
    freqs = sorted(freqDict)
    i = 0
    score = 0
    while(i < len(freqs)):
        c = freqs[i]
        if((i < 5) and ((c == 'e') or (c == 't') or (c == 'a') or (c == 'i') or (c == 'o'))):
            # If current char is one of the most frequent English letters and it's one of the top 5 most frequent
            score += 1
        i += 1
    return score # This reflects how many of the top 5 most frequent English letters are in the top 5 most frequent for the string

def byteXOR(file):
    infile = open(file, 'r')
    lines = infile.readlines()

    val = 0
    while(val < 32):
        bite = val.to_bytes(1, "big")
        print("Processing byte: " + str(val))
        print(bite)
        i = 0
        # Analyze each line
        for line in lines:
            # First xor to try to decode
            plaintext = ciphersXOR.xor_bytestrings(line.encode("ascii"), bite).decode("ascii")
            score = scorePlaintext(plaintext)

            # Testing
            if(i == 0):
                #print(plaintext)
                i += 1

            if(score > 0): # If line's char freq has at least 4 of 5 most common english letters as its most common
                print("Byte: ")
                print(bite)
                print("Plaintext: " + plaintext + "\n\n")
        val += 1

def main():
    byteXOR("Lab0.TaskII.B.txt")

if __name__ == '__main__':
    main()
    