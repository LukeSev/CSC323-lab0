import converting

def match_key(plaintext, key):
    # Matches lengths of plaintext/key by either making key larger or making key smaller
    # Returns key
    plainArr = bytearray(plaintext)
    newKey = bytearray(key)
    if(len(plaintext) > len(key)):
        i = 0
        while(len(plainArr) > len(newKey)):
            newKey.append(newKey[i])
            i += 1
    elif(len(plaintext) < len(key)):
        newKey = newKey[:len(plainArr)]
    return bytes(newKey)

def xor_bytestrings(plaintext, key):
    newKey = match_key(plaintext, key)
    return bytes([x ^ y for x, y in zip(plaintext, newKey)])

def main():
    # Basic functionality test
    test_b1 = b'10110011'
    test_b2 = b'01001100'
    out1 = xor_bytestrings(test_b1, test_b2) # Should return all 0s
    out2 = xor_bytestrings(test_b1, test_b1) # Should return all 1s

    print(out1)
    print(out2)

    # Test key length matching
    test_b3 = b'00000000'
    test_b4 = b'111'
    test_b5 = b'00'
    out3 = xor_bytestrings(test_b3, test_b4) # Should return all 1s
    out4 = xor_bytestrings(test_b3, test_b5) # Should return all 0s

    print(out3)
    print(out4)

if __name__ == '__main__':
    main()
