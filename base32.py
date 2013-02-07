#!/usr/bin/env python3
'''
base32.py

CLI base32 encoder/decoder.

Created: 7 feb 2013.

@author: Anton Eliasson <devel@antoneliasson.se>
'''
import base64

def main():
    import sys, argparse
    parser = argparse.ArgumentParser(description='Base32 encode or decode FILE, '
                                     'or standard input, to standard output.')
    parser.add_argument('-d', '--decode', action='store_true')
    parser.add_argument('FILE', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    args = parser.parse_args()

if __name__ == '__main__':
    main()
