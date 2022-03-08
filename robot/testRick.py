import base64
from io import BytesIO

from PIL import Image

import sys


def sizeof_fmt(num, suffix='B'):
    ''' by Fred Cirera,  https://stackoverflow.com/a/1094933/1870254, modified'''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


im = Image.open('rick-astley-rickrolling.jpg')
im = im.resize((128, 128))

im_file = BytesIO()
im.save(im_file, format="JPEG")
im_bytes = im_file.getvalue()  # i
im_b64 = str(base64.b64encode(im_bytes))

for name, size in sorted(((name, sys.getsizeof(value)) for name, value in locals().items()),
                         key=lambda x: -x[1])[:10]:
    print("{:>30}: {:>8}".format(name, sizeof_fmt(size)))
