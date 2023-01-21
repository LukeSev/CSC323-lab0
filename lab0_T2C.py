import lab0_T2B
import ciphersXOR
import converting
import base64

def multiByteDecrypt(file):
    infile = open(file, 'r')
    ciphertext = infile.read().rstrip() # Remove newline chars if there
    encrypted = base64.b64decode(ciphertext)

    # For range, max possible key value will occur if key is size of entire ciphertext
    for val in range(2 ** (8 * len(encrypted))):
        try:
            plaintext = ciphersXOR.xor_bytestrings(encrypted, val).decode()
            score = lab0_T2B.scorePlaintext(plaintext)
            if(score > 500):
                print("\nFound viable decryption")
                print("SCORE: " + str(score))
                print("Decryption: " + plaintext + "\n")
        except UnicodeError:
            failed = True

def main():
    multiByteDecrypt("Lab0.TaskII.C.txt")
    #byteXOR("test.txt")

if __name__ == '__main__':
    main()