import lab0_T2B
import ciphersXOR
import converting
import base64

SCORE_THRESHOLD = 5000

def findKey(byteArr):
    # Takes in an array of bytes and tries to find a key that decrypts to something close to English
    # Track the key/plaintext that most adheres to English language
    # Format: (HighScore, Key, Plaintext letters)
    best = (0, 0, "")
    for val in range(256):
            try:
                plaintextLetters = ciphersXOR.xor_bytestrings(byteArr, val).decode()
                score = lab0_T2B.scoreEngPlaintext(plaintextLetters)
                if((score > SCORE_THRESHOLD) and (score > best[0])): # Only add plaintext to dictionary if it at least somewhat resembles English
                    best = (score, val, plaintextLetters)
            except UnicodeError:
                failed = True
    return best

def findKeyLength(ciphertext):
    # Systematically break up ciphertext into n byte arrays by taking every n bytes
    # Take one of the byte arrays, and do single byte XOR to determine if it translates to english text
    # Scoring: A score of 50+ is regarded as close enough to English text...
    # ... This was determined by observing the results of the single-byte XOR from part B
    # Also worth noting: it was given that the key is no longer than 20 bytes
    # Returns: tuple containing the byte that was used to decode the first set of bytes and the size of the key
    for n in range(1,21,1):
        # First build the byte array that holds every n bytes
        byteArr = bytearray()
        cArr = bytearray(ciphertext)
        for i in range(0,len(cArr),n):
            byteArr.append(cArr[i])
        
        # Now do some XORing to see if any yield passable English
        best = findKey(byteArr)
        if(best[0] > 0):
            print("\nKey found! \nByte: {} \nKeySize: {}".format(best[1], n))
            return (best[1], n, best[2])

def fillPlaintext(plaintext, letters, keySize, start):
    for i in range(0, len(letters), 1):
        plaintext[start + (i*keySize)] = letters[i]

def multiByteDecrypt(file):
    infile = open(file, 'r')
    ciphertext = infile.read().rstrip() # Remove newline chars if there
    decoded = base64.b64decode(ciphertext)
    results = findKeyLength(decoded)
    keySize = results[1]
    letters = results[2]
    plaintext = list("\0" * len(ciphertext))
    fillPlaintext(plaintext, letters, keySize, 0)

    # Create byte array to hold each part of the key
    keyArr = bytearray(keySize)
    keyArr.append(results[0])
    cArr = bytearray(decoded)

    # Now find the rest of the parts of the key
    for i in range(1,keySize):
        # First build byte array
        byteArr = bytearray()
        for j in range(i,len(cArr),keySize):
            byteArr.append(cArr[j])
        curr = findKey(byteArr)
        keyArr.append(curr[1])
        fillPlaintext(plaintext, curr[2], keySize, i)

    # Once char array filled for plaintext, convert back to string and print
    keyArr.reverse()
    key = bytes(keyArr[:keySize]).hex()
    print("Key:0x{}\n".format(key))
    print("\nPlaintext:")
    print(''.join(plaintext))

def main():
    multiByteDecrypt("Lab0.TaskII.C.txt")
    #byteXOR("test.txt")

if __name__ == '__main__':
    main()