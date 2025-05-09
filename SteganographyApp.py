from PIL import Image

def numberToBinary(num):
    """Convert a number to an 8-bit binary string."""
    return format(num, '08b')

def binaryToNumber(binaryString):
    """Convert an 8-bit binary string to a number."""
    return int(binaryString, 2)

def encode(img, msg):
    """Encode a message into the image using LSB."""
    pixels = img.load()
    width, height = img.size
    msgLength = len(msg)
    letterSpot = 0
    pixel = 0

    # Store message length in the first pixel
    r, g, b = pixels[0, 0]
    pixels[0, 0] = (msgLength, g, b)

    for i in range(msgLength * 3):
        x = i % width
        y = i // width

        r, g, b = pixels[x, y]
        r_bin = numberToBinary(r)
        g_bin = numberToBinary(g)
        b_bin = numberToBinary(b)

        if pixel % 3 == 0:
            letter_bin = numberToBinary(ord(msg[letterSpot]))
            g_bin = g_bin[:7] + letter_bin[0]
            b_bin = b_bin[:7] + letter_bin[1]
        elif pixel % 3 == 1:
            g_bin = g_bin[:7] + letter_bin[3]
            r_bin = r_bin[:7] + letter_bin[2]
            b_bin = b_bin[:7] + letter_bin[4]
        else:
            r_bin = r_bin[:7] + letter_bin[5]
            g_bin = g_bin[:7] + letter_bin[6]
            b_bin = b_bin[:7] + letter_bin[7]
            letterSpot += 1

        pixels[x, y] = (
            binaryToNumber(r_bin),
            binaryToNumber(g_bin),
            binaryToNumber(b_bin)
        )

        pixel += 1

    img.save("secretImg.png", "PNG")

def decode(img):
    """Decode a message from the image."""
    pixels = img.load()
    width, height = img.size
    msg = ""

    r, g, b = pixels[0, 0]
    msgLength = r
    pixel = 0
    letterBinary = ""
    x = 0
    y = 0

    while len(msg) < msgLength:
        r, g, b = pixels[x, y]
        r_bin = numberToBinary(r)
        g_bin = numberToBinary(g)
        b_bin = numberToBinary(b)

        if pixel % 3 == 0:
            letterBinary = g_bin[7] + b_bin[7]
        elif pixel % 3 == 1:
            letterBinary += r_bin[7] + g_bin[7] + b_bin[7]
        else:
            letterBinary += r_bin[7] + g_bin[7] + b_bin[7]
            msg += chr(binaryToNumber(letterBinary))

        pixel += 1
        x = pixel % width
        y = pixel // width

    return msg

def main():
    choice = input("Do you want to (E)ncode or (D)ecode a message? ").strip().upper()
    filename = input("Enter the name of the PNG image file: ").strip()

    if not filename.lower().endswith('.png'):
        print("Only PNG files are supported.")
        return

    try:
        img = Image.open(filename)
    except FileNotFoundError:
        print("File not found.")
        return

    if choice == 'E':
        msg = input("Enter the message to hide: ")
        encode(img, msg)
        print("Message encoded and saved as secretImg.png.")
    elif choice == 'D':
        message = decode(img)
        print("Decoded message:", message)
    else:
        print("Invalid choice.")

if __name__ == '__main__':
    main()
