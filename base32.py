#!/usr/bin/env python3
'''
base32.py

CLI base32 encoder/decoder.

Created: 7 feb 2013.

@author: Anton Eliasson <devel@antoneliasson.se>
'''
import base64

def encode(file):
    data = file.read()
    return base64.b32encode(data)

def decode(file):
    data = file.read()
    data = data.strip().replace(' ', '').replace('\n', '')
    return base64.b32decode(data, casefold=True)

def main():
    import sys, argparse

    # make stdin binary
    sys.stdin = sys.stdin.detach()

    parser = argparse.ArgumentParser(description='Base32 encode or decode FILE, '
                                     'or standard input, to standard output.', epilog='With no FILE, or when FILE is -, read standard input.')
    parser.add_argument('-d', '--decode', action='store_true', help='decode data')
    parser.add_argument('FILE', nargs='?', type=argparse.FileType('rb'), default=sys.stdin)

    args = parser.parse_args()

    file = args.FILE

    if args.decode:
        print(decode(file).decode('ascii'))
    else:
        result = encode(file).decode('ascii')
        for line in result.split(sep='', maxsplit=76):
            print(line)

if __name__ == '__main__':
    main()
