#!/usr/bin/env python2
# Swaps the tags artist and album artist in an MP4 file.
#
# Created 2013-03-13

import mutagen
import mutagen.flac
import mutagen.easymp4
import sys

# constants
ARTIST = '\xa9ART'
ALBUM_ARTIST = 'aART'
PART_OF_COMPILATION = 'cpil'

def usage():
    return '''Usage: albumartist_fixer.py <mp4 file>'''

def main():
    # This breaks pprint (among other things, probably). RegisterTextKey is supposed
    # to be used for mapping a tag name (arg 1) to a list (of strings, arg 2). Here I
    # map a tag name directly to a boolean (cpil). Since pprint expects all attributes
    # to be iterable, it will fail on the 'compilation' attribute.
    #
    # The correct way to solve this would be to invent
    # classmethod mutagen.easymp4.RegisterBoolKey(key, atomid)
    # which would wrap the boolean in a list. I am going to avoid pprint instead.
    mutagen.easymp4.EasyMP4Tags.RegisterTextKey('compilation', 'cpil')

    if len(sys.argv) != 2:
        # wrong number of arguments
        print(usage())
        sys.exit(1)

    filename = sys.argv[1]
    try:
        # only MP4 and FLAC are tested, but others may work
        audiofile = mutagen.File(filename, options=[mutagen.easymp4.EasyMP4, mutagen.flac.FLAC],
                                 easy=True)
    except IOError as ioe:
        print(ioe)
        sys.exit(ioe.errno)
    if audiofile is None:
        print('No handler available for file {}'.format(filename))
        sys.exit(1)
    else:
        print('{} identified as {}'.format(filename, audiofile.mime[0]))

    if 'artist' in audiofile and 'albumartist' in audiofile:
        if len(audiofile['artist']) == 1 and len(audiofile['albumartist']) == 1:
            # swap tags
            audiofile['artist'], audiofile['albumartist'] = audiofile['albumartist'], audiofile['artist']
            # maybe mark track as part of a compilation
            if 'audio/mp4' in audiofile.mime:
                print("{} is part of a compilation album (MP4 specific)".format(filename))
                audiofile['compilation'] = True
            audiofile.save()
            print("Tags successfully swapped. New values:")
            print("Artist: " + audiofile['artist'][0])
            print("Album artist: " + audiofile['albumartist'][0])
        else:
            # untested :3
            print('Too many or too few tags in file:')
            from pprint import pprint
            pprint(audiofile.items())
            print('Bailing out.')
            sys.exit(1)
    else:
        if 'artist' in audiofile:
            message = 'did not contain an ALBUMARTIST tag.'
        elif 'albumartist' in audiofile:
            message = 'did not contain an ARTIST tag.'
        else:
            message = 'did not contain an ARTIST and ALBUMARTIST tag.'
        print("Failed. '" + filename + "' " + message)
        sys.exit(3)

if __name__ == '__main__':
    main()
