#!/usr/bin/env python3
'''
4get

The successor to the original 4chandl script.

Created: 1 feb 2013.

@author: Anton Eliasson <devel@antoneliasson.se>

'''

import logging
try:
    import httplib2
    httplib2.debuglevel = 1
    hlib = httplib2.Http('.cache')
except ImportError:
    print('''This application requires the Python library httplib2. Search your Linux distribution's
packages or download the source here: http://code.google.com/p/httplib2/''')
    import sys
    sys.exit(1)

def split_url(url):
    from urllib.parse import urlparse

    p = urlparse(url)
    path = p.path.split('/')
    scheme = p.scheme
    board = path[1]
    threadnumber = path[3]

    return (scheme, board, threadnumber)

def get_posts(scheme, board, threadnumber):
    import json
    url = '{0}://api.4chan.org/{1}/res/{2}.json'.format(scheme, board, threadnumber)
    response, content = hlib.request(url)
    _ = json.loads(content.decode())
    posts = _['posts']
    return posts

def get_file_urls(scheme, board, posts):
    from base64 import b64decode
    files = []
    for post in posts:
        if 'tim' in post:
            tim = post['tim']
            ext = post['ext']
            url = '{0}://images.4chan.org/{1}/src/{2}{3}'.format(scheme, board, tim, ext)
            filename = post['filename']
            md5 = b64decode(post['md5'])
            file = {'url' : url, 'filename' : filename, 'ext' : ext, 'md5' : md5}
            files.append(file)
    return files

def download_file(directory, url, filename, ext):
    response, content = hlib.request(url)
    if response.status != 200:
        print('URL {0} with original filename {1} failed to download with status {2}'.format(url, filename, response.status))
    for attempt in range(10):
        try:
            if attempt > 0:
                fname = 'filename-{}'.format(attempt)
            else:
                fname = filename
            file = open(directory + fname + ext, 'xb')
            break
        except FileExistsError:
            continue
    else:
        print('{} kunde inte sparas'.format(filename))
    
    file.write(content)
    return filename

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Downloads images from 4chan')
    parser.add_argument('thread')
    parser.add_argument('directory')

    args = parser.parse_args()
    thread_url = args.thread
    directory = args.directory
    # säkerställ att: directory inte existerar | directory är en katalog & (directory är tom | -f används), annars sys.exit
    scheme, board, threadnumber = split_url(thread_url)

    posts = get_posts(scheme, board, threadnumber)
    files = get_file_urls(scheme, board, posts)

    for file in files:
        filename = download_file(directory, file['url'], file['filename'], file['ext'])
#        check_file(directory, filename, file['md5'])

if __name__ == '__main__':
    main()
