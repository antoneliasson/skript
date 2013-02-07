#!/usr/bin/env python3
'''
base32.py

CLI base32 encoder/decoder.

Too slow to be usable on big (>1MB) files, apparently.

Created: 7 feb 2013.

@author: Anton Eliasson <devel@antoneliasson.se>
'''
import base64

def encode(file):
    '''
    Reads file and returns it base32 encoded as a bytes object.
    '''
    data = file.read()
    return base64.b32encode(data)

def decode(file):
    '''
    Reads file, strips all whitespace and base32 decodes it. The result is returned
    as a bytes object.
    '''
    data = file.read().decode('ascii')
    data = data.strip().replace(' ', '').replace('\n', '').replace('\t', '')
    return base64.b32decode(data, casefold=True)

def wrap_text(text, width):
    '''
    Inserts a newline into the string text at every width character (but not at
    the end of the string). The result is returned as a new string.
    '''
    import textwrap
    # break_on_hyphens makes textwrap really slow with unbreakable lines, disable it
    return '\n'.join(textwrap.wrap(text, width=width, break_on_hyphens = False))

def main():
    import sys, argparse

    # make stdin binary
    sys.stdin = sys.stdin.detach()

    parser = argparse.ArgumentParser(description='Base32 encode or decode FILE, '
                                     'or standard input, to standard output.',
                                     epilog='With no FILE, or when FILE is -, read standard input.')
    parser.add_argument('-d', '--decode', action='store_true', help='decode data')
    parser.add_argument('FILE', nargs='?', type=argparse.FileType('rb'), default=sys.stdin)
    parser.add_argument('-w', '--wrap', default=76, help='wrap encoded lines after COLS character (default 76).')

    args = parser.parse_args()

    file = args.FILE
    textwidth = int(args.wrap)

    if args.decode:
        print(decode(file).decode('ascii'), end='')
    else:
        text = encode(file).decode('ascii')
        print(wrap_text(text, textwidth))

if __name__ == '__main__':
    main()
