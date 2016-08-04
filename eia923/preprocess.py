import argparse
import mimetypes
import os
import tempfile
import zipfile

from io import BytesIO
from spreadsheetto import open_spreadsheet
from swiftclient.service import SwiftService, SwiftUploadObject

def convert_and_store_cli():
    parser = argparse.ArgumentParser(description='Convert eia-923 XLS files to CSV files and save in cloud object storage')
    parser.add_argument('--container', dest='container', required=True,
                        help='object storage container name')
    parser.add_argument('--prefix', dest='prefix', default='',
                        help='pseudo-directory prefix (${container}/${prefix}/${object})')
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()

    container = args.container
    if args.prefix != '':
        container = "%s/%s" % (container, args.prefix)

    objects = []

    for filename in args.filenames:
        mt = mimetypes.guess_type(filename)[0]
        if mt == 'application/zip':
            zf = zipfile.ZipFile(filename, 'r')
            temp_dir = tempfile.gettempdir()
            for zf_fn in zf.namelist():
                zf.extract(zf_fn, temp_dir)
                filename = os.path.sep.join((temp_dir, zf_fn))
                print(filename)
                for x in convert_to_swiftobjects(filename):
                    objects.append(x)
                os.remove(filename)
        else:
            for x in convert_to_swiftobjects(filename):
                objects.append(x)

    with SwiftService() as swift:
        for result in swift.upload(container, objects):
            if not result['success']:
                print(result)
            else:
                if 'object' in result:
                    print("%s status: %s" % (result['object'], result['success']))
                else:
                    print(result)

def convert_to_swiftobjects(filename):
    objects = []
    try:
        spreadsheet = open_spreadsheet(filename)
        for sheetname, worksheet in spreadsheet.sheet_dict.items():
            objectname = "%s/%s.csv" % (os.path.basename(filename), sheetname)
            objects.append(SwiftUploadObject(BytesIO(bytes(worksheet.to_csv(), 'utf-8')), objectname))
            print("objectname :: %s" % (objectname))
    except Exception as e:
        print("Exception caught: %s" % filename)
        print(e)
    return objects

# eia-923-convert-and-store --container ets-training-cloudenabled --prefix eia-923/mirror/preprocessed 
