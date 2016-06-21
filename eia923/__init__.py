#!/usr/bin/env python3

import argparse
import os
import urllib.request

from http.server import HTTPServer, SimpleHTTPRequestHandler

def download_file(file_url, file_path):
    if os.path.exists(file_path):
        print("%s previously retrieved" % file_path)
    else:
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        print("downloading %s" % file_url)
        urllib.request.urlretrieve(file_url, file_path)

def download_eia906_archives(mirror, destination):
    for year in range(1970, 2001):
        file_name = 'f759%du.xls' % year
        file_path = os.path.sep.join((destination, file_name))
        file_url = "%s%s" % (mirror, file_name)
        download_file(file_url, file_path)

def download_eia923_archives(mirror, destination):
    names = ['f923_%d.zip' % year for year in range(2008, 2015)]
    for n in ['f906920_%d.zip' % year for year in range(2001, 2008)]:
        names.append(n)

    for file_name in names:
        file_path = os.path.sep.join((destination, file_name))
        file_url = "%s%s" % (mirror, file_name)
        download_file(file_url, file_path)

def mirror():
    parser = argparse.ArgumentParser(description='Download eia-923 archives')
    parser.add_argument('--source', dest='source',
                        default='http://www.eia.gov/electricity/data/eia923/xls/',
                        help="default is http://www.eia.gov/electricity/data/eia923/xls/")
    parser.add_argument('--destination', dest='destination',
                        default=os.curdir)
    parser.add_argument('--server', dest='server',
                        default=None,
                        help="host:port to serve, default is none")
    
    args = parser.parse_args()
    download_eia923_archives(args.source,
                             args.destination)
    download_eia906_archives("%sutility/" % args.source,
                             os.path.sep.join((args.destination, "utility")))

    if args.server != None:
        os.chdir(args.destination)
        host, port = args.server.split(':')
        port = int(port)
        httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
        print("Serving data at %s:%d" % (host, port))
        httpd.serve_forever()

if __name__ == '__main__':
    mirror()
