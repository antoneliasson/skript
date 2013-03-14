#!/usr/bin/env python2
# Swaps the tags artist and album artist in an MP4 file.
#
# Created 2013-03-13

import mutagen.mp4
import sys

# constants
ARTIST = '\xa9ART'
ALBUM_ARTIST = 'aART'
PART_OF_COMPILATION = 'cpil'

def usage():
    return '''Usage: albumartist_fixer.py <mp4 file>'''

def main():
    if len(sys.argv) != 2:
        # wrong number of arguments
        print(usage())
        sys.exit(1)

    filename = sys.argv[1]
    try:
        audiofile = mutagen.mp4.MP4(filename)
    except mutagen.mp4.MP4StreamInfoError:
        print("'{}' does not look like a MP4 file.".format(filename))
        sys.exit(2)
    except IOError as ioe:
        print(ioe)
        sys.exit(ioe.errno)
        
    if ARTIST in audiofile and ALBUM_ARTIST in audiofile:
        if len(audiofile[ARTIST]) == 1 and len(audiofile[ALBUM_ARTIST]) == 1:
            # swap tags
            audiofile[ARTIST], audiofile[ALBUM_ARTIST] = audiofile[ALBUM_ARTIST], audiofile[ARTIST]
            # mark track as part of a compilation
            audiofile[PART_OF_COMPILATION] = True
            audiofile.save()
            print("Tags successfully swapped in '{}'. New values:".format(filename))
            print("Artist: " + audiofile[ARTIST][0])
            print("Album artist: " + audiofile[ALBUM_ARTIST][0])
        else:
            # untested :3
            print('Too many or too few tags in file:')
            print(audiofile.pprint())
            print('Bailing out.')
            sys.exit(4)
    else:
        if ARTIST in audiofile:
            message = 'did not contain an ALBUM_ARTIST tag.'
        elif ALBUM_ARTIST in audiofile:
            message = 'did not contain an ARTIST tag.'
        else:
            message = 'did not contain an ARTIST and ALBUM_ARTIST tag.'
        print("Failed. '" + filename + "' " + message)
        sys.exit(3)

if __name__ == '__main__':
    main()
