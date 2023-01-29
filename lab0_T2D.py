import lab0_T2B
import lab0_T2C
import ciphersXOR
import converting
import base64

SCORE_THRESHOLD = 300

def shiftLetters(letters, amt):
    # Given string of chars, shift all chars by specified amount of chars
    shiftedLetters = []
    for letter in letters:
        # For each letter, convert to int, increment by given amt, then convert back to char and add to shifted
        newLetterVal = ord(letter)+amt
        # Check if uppercase or lowercase
        if(letter.isupper()):
            if(newLetterVal > 90):
                # If shifted letter goes past end of uppercase alphabet, make it wrap around
                newLetterVal -= 26
        else:
            if(newLetterVal > 122):
                # If shifted letter goes past end of lowercase alphabet, make it wrap around
                newLetterVal -= 26
        shiftedLetters.append(chr(newLetterVal))
    return ''.join(shiftedLetters)

def findCharKey(letters):
    # Takes in char string and tries to find a shift amount that yields a passable score
    # Output format: (Score, Ascii Char shift amt, plaintext letters)
    best = (0, '', "")
    for amt in range(26):
        plaintextChars = shiftLetters(letters, amt)
        score = lab0_T2B.scorePlaintext(plaintextChars.lower())
        if(score > best[0]):
            best = (score, chr(97+amt), plaintextChars)
    return best

def findCharKeyLength(ciphertext, start):
    # Similar method as used in part C except with shifting letters instead of XORing bytes
    # Once again assuming length of key won't be over 20 chars
    # Returns tuple in format (Key Length, Key Char, Shifted Letters, score)
    for n in range(start,21,1):
        # First build string of every n letters of ciphertext
        letters = []
        for i in range(0,len(ciphertext), n):
            letters.append(ciphertext[i])

        # Now see if any letters 
        key = findCharKey(''.join(letters))
        if(key[0] > SCORE_THRESHOLD):
            return (n, key[1], key[2], key[0])
    return (0, '', "", 0)

def doVigenereStuff(ciphertext, keyInfo):
    # Takes ciphertext and keyInfo with a specific keySize, and then does rest of Vigenere Cipher
    # Returns tuple in format: (key, plaintext)
    keySize = keyInfo[0]
    # Build the key and plaintext as each Caesar Cipher is completed
    plaintext = list("\0" * len(ciphertext))
    lab0_T2C.fillPlaintext(plaintext, keyInfo[2], keySize, 0)
    key = []
    key.append(keyInfo[1])

    # Now perform the rest of the Caesar Ciphers
    for i in range(1,keySize):
        letters = []
        for j in range(i, len(ciphertext), keySize):
            letters.append(ciphertext[j])
        best = findCharKey(''.join(letters))
        key.append(best[1])
        lab0_T2C.fillPlaintext(plaintext, best[2], keySize, i)
    return (''.join(key), ''.join(plaintext))

def itWasntActuallyVigenere(filename):
    infile = open(filename, 'r')
    ciphertext = infile.read().rstrip() # Remove newline chars if there
    start = 1
    best = ("", "", 0)
    while(start < 21):
        keyInfo = findCharKeyLength(ciphertext, start)
        results = doVigenereStuff(ciphertext, keyInfo)
        if(keyInfo[0] > 0):
            score = lab0_T2B.scorePlaintext(results[1])
            if(score > best[2]):
                best = (results[0], results[1], score)
            start = keyInfo[0]+1
        else:
            break

    # Once done, print plaintext and key
    print("Key:\n{}\n\nPlaintext:\n{}\n".format(best[0], best[1]))

def main():
    itWasntActuallyVigenere("Lab0.TaskII.D.txt")

if __name__ == '__main__':
    main()