from optparse import OptionParser
import sys
import os


def init_opts():
    parser = OptionParser()
    parser.add_option("-t", "--type", action="store_true",
                      dest="type", default=False,
                      help="Type in the message rather than use a file")
    parser.add_option("-f", "--file", action="store_true",
                      dest="file", default=False,
                      help="Use a file rather than type in the message")
    parser.add_option("-e", "--encrypt", action="store_true",
                      dest="encrypt", default=False,
                      help="Encrypt the message")
    parser.add_option("-d", "--decrypt", action="store_true",
                      dest="decrypt", default=False,
                      help="Decrypt the message")
    parser.add_option("-s", "--shift", action="store",
                      dest="shift", default=0, type='int',
                      help="Th number to shift the letters by")
    options, args = parser.parse_args()
    return options, args


def letter_mode_decrypt(num_shifted, encrypted_char, accept_symbol=True):
    """The letter mode allows users to enter encrypted and space only. The function
    operates within the range of A-Z. Return space or encrypted_char upper cases letter.

    num_shifted:       the number to shift the character by
    encrypted_char:    the letter mode encrypted_char letter to be decrypted
    accept_symbol:     whether or not to allow for symbols as input; if so, return the
                       symbol itself
    num_to_shift:      the number to shift the encrypted character by to get the decrypted character
    """

    # If the given character is SPACE, just return the space
    if encrypted_char == " ":
        return " "

    # Convert characters to ASCII numbers
    encrypted_char_num = ord(encrypted_char.upper())

    # If the given character is neither a letter nor space,
    # replace the symbol with a space if ignore_symbol is
    # true; otherwise, raise the error
    if encrypted_char_num < 65 or encrypted_char_num > 90:
        if accept_symbol is True:
            return encrypted_char
        else:
            msg = """The input continas "%s", which is not a letter.""" % plain_char
            raise Exception(msg)

    # Keep the number to shift the letter by within 0 - 26
    while num_shifted > 26:
        num_shifted -= 26

    # Calculate how many numbers to shift to get the decrypted letter
    num_to_shift = 26 - num_shifted

    # If the number to shift would shift the character out of "Z", ASCII 90, then
    # add 6 to the number to shift to use the lower case letters (range 97 - 122)
    if num_to_shift + encrypted_char_num > 90:
        num_to_shift += 6

    # store the decrypted character
    decrypted_char = chr(encrypted_char_num + num_to_shift)

    # return the character and make sure it's in upper case
    return decrypted_char.upper()


def letter_mode_encrypt(num_shifted, plain_char, accept_symbol=True):
    """The letter mode allows users to enter letters and space only. The function
    operates within the range of A-Z. Return space or encrypted upper cases letter.

    num_shifted:   the number to shift the character by
    plain_char:    the original letter to be encrypted
    accept_symbol: whether or not to allow for symbols as input; if so, return the
                   symbol itself
    """

    # If the given character is SPACE, just return the space
    if plain_char == " ":
        return " "

    # Convert characters to ASCII numbers
    plain_char_num = ord(plain_char.upper())

    # If the given character is neither a letter nor space,
    # replace the symbol with a space if ignore_symbol is
    # true; otherwise, raise the error
    if plain_char_num < 65 or plain_char_num > 90:
        if accept_symbol is True:
            return plain_char
        else:
            msg = """The input continas "%s", which is not a letter.""" % plain_char
            raise Exception(msg)

    # Keep the number to shift the letter by within 0 - 26
    while num_shifted > 26:
        num_shifted -= 26

    # If the number to shift would shift the character out of "Z", ASCII 90, then
    # add 6 to the number to shift to use the lower case letters (range 97 - 122)
    if num_shifted + plain_char_num > 90:
        num_shifted += 6

    # store the encrypted character
    encrypted_char = chr(plain_char_num + num_shifted)

    # return the character and make sure it's in upper case
    return encrypted_char.upper()


def main():
    print("************** Welcome to Caesar cipher program **************")
    options, args = init_opts()
    message = ""
    result = ""

    if options.type and not options.file:
        message = input("Please enter the message to encrypt: ")
    elif options.file and not options.type:
        file_path = input("Please enter the path to the text file to encrypt")
        if not os.access(file_path, os.R_OK):
            print("Unable to read the file at %s" % file_path)
            sys.exit()
        else:
            with open(file_path) as f:
                message = f.read()
    else:
        print('Please choose between entering a message or use a file')
        sys.exit()

    print("Message reading complete.")

    if options.encrypt and not options.decrypt:
        for character in message:
            encrypted_letter = letter_mode_encrypt(options.shift, character)
            result += encrypted_letter
    elif options.decrypt and not options.encrypt:
        for character in message:
            decrypted_letter = letter_mode_decrypt(options.shift, character)
            result += decrypted_letter
    else:
        print('Please choose between encryption or decryption')
        sys.exit()

    print("Results generated. Outputting to the text file in the program directory.")

    file = open("results.txt", 'w')
    file.write(result)
    file.close()

    print("Results saved. Available in the text file now.")


if __name__ == "__main__":
    main()
