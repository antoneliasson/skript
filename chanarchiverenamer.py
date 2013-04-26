#!/usr/bin/env python3
'''
TODO: documentation!

Created on 4 April 2013.

@author: Anton Eliasson <devel@antoneliasson.se>
'''

import logging
import os

from lxml.html import parse

def get_filename_mappings(root):
    mappings = []
    filetexts = root.xpath('//span[@class="fileText"]')
    for filetext in filetexts:
        src = filetext[0].text
        dst = filetext[1].attrib['title']
        mapping = (src, dst)
        logging.debug('Found mapping: %s', mapping)
        mappings.append(mapping)
    return mappings

def safe_rename(src, dst):
    ''' os.rename() is subject to race conditions. This solution should be race-free. '''
    try:
        os.link(src, dst)
    except FileNotFoundError:
        logging.warning('File %s that should have been renamed to %s does not exist', src, dst)
        # skip
        return
    except FileExistsError:
        # destination file already exists, make up a new filename
        nbr = os.path.splitext(src)[0]
        name = os.path.splitext(dst)[0]
        ext = os.path.splitext(dst)[1]
        new_dst = '{}-{}{}'.format(name, nbr, ext)
        logging.warning('%s already exists; renaming to %s instead', dst, new_dst)
        os.link(src, new_dst)
        # die if that didn't work
    os.unlink(src)

def rename_all(filename_mappings):
    for mapping in filename_mappings:
        safe_rename(mapping[0], mapping[1])

def get_thumbnails(root):
    thumbs = []
    filethumbs = root.xpath('//a[@class="fileThumb"]')
    for filethumb in filethumbs:
        img = filethumb[0]
        path = img.attrib['src']
        fname = path.split('/').pop()
        logging.debug('Found thumbnail: %s', fname)
        thumbs.append(fname)
    return thumbs

def cleanup(root):
    thumbnails = get_thumbnails(root)
    for f in thumbnails:
        logging.debug('Removing thumbnail: %s', f)
        try:
            os.remove(f)
        except FileNotFoundError:
            logging.warning('Thumbnail %s that should have been deleted does not exist', f)

def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    
    tree = parse('index.html')
    root = tree.getroot()
    
    filename_mappings = get_filename_mappings(root)
    rename_all(filename_mappings)

    cleanup(root)
    
    logging.info('Done. You get to clean up the CSS and JS files manually.')
    # TODO: remove <op's file>_{75,150}.jpg
    
if __name__ == '__main__':
    main()

