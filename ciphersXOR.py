import converting

def match_key(plaintext, key):
    # Matches lengths of plaintext/key by either making key larger or making key smaller
    # Returns key
    plainArr = bytearray(plaintext)
    hexkey = hex(key)[2:]
    if(len(hexkey) % 2 == 1):
        hexkey = '0' + hexkey # Pad with 0 to make compatible with fromhex
    newKey = bytearray.fromhex(hexkey)
    if(len(plainArr) > len(newKey)):
        i = 0
        while(len(plainArr) > len(newKey)):
            newKey.append(newKey[i])
            i += 1
    elif(len(plainArr) < len(newKey)):
        newKey = newKey[:len(plainArr)]
    return bytes(newKey)

def xor_bytestrings(plaintext, key):
    newKey = match_key(plaintext, key)
    return bytes([x ^ y for x, y in zip(plaintext, newKey)])

def main():

    #test = "basic"
    #test = "complex"
    test = "typetest"

    if(test == "basic"):
        # Basic functionality test
        test_b1 = b'10110011'
        test_b2 = b'01001100'
        out1 = xor_bytestrings(test_b1, test_b2) # Should return all 0s
        out2 = xor_bytestrings(test_b1, test_b1) # Should return all 1s

        # Test key length matching
        test_b3 = bytes.fromhex("ff")
        test_b4 = bytes.fromhex("00")
        test_b5 = bytes.fromhex("ff")
        out3 = xor_bytestrings(test_b3, test_b4) # Should return all 1s
        out4 = xor_bytestrings(test_b3, test_b5) # Should return all 0s

        print(out3)
        print(out4)

    elif(test == "complex"):
        # We want to take a word, xor it and encode as hex string, then try to decode in reverse
        key = 16 # Single byte key
        plaintext = "Hello, this is a test"
        print("Plaintext before encryption: " + plaintext)

        # Now XOR
        heXORed = xor_bytestrings(plaintext.encode("ascii"), bytes(key)).hex()
        print("XORed and hexxed: " + heXORed)

        # Now convert back again
        ciphertext = bytes.fromhex(heXORed)
        plaintext_surely = xor_bytestrings(ciphertext, bytes(key)).decode("ascii")
        print("Decrypted: " + plaintext_surely)

    elif(test == "typetest"):
        key = 287
        hexkey = hex(key)
        print(hexkey)
        print(hexkey[2:])
        print(type(hex(key)))



if __name__ == '__main__':
    main()
