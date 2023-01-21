import binascii
import base64


# Conversion (Encode/Decode) functions will be used to make conversion much easier in future projects
def ascii_to_hex(str):
    return str.encode("ascii").hex()

def hex_to_ascii(hexx):
    return bytearray.fromhex(hexx).decode("ascii")

def hex_to_b64(str):
    return base64.b64encode(str.fromhex().encode("ascii")).decode("ascii")

def b64_to_hex(b):
    return base64.b64decode(b.encode("ascii")).decode("ascii").hex()

def main():
    # Tests validity of conversion functions
    test_str = "Hello"
    hexxy = ascii_to_hex(test_str)
    bb = ascii_to_b64(test_str)

    print("Test string: " + test_str)
    print("Hex encoded string: " + hexxy)
    print("Base64 encoded string: " + bb)

    hex_back = hex_to_ascii(hexxy)
    b_back = b64_to_ascii(bb)

    print("Hex converted back: " + hex_back)
    print("Base64 converted back: " + b_back)

if __name__ == '__main__':
    main()