#!/usr/bin/env python3

import json
import struct
import sys
import zlib

if __name__ == '__main__':
    with open(sys.argv[1]) as fp:
        obj = json.load(fp)
    text = json.dumps(obj, separators=(',', ':')).encode('utf-8')
    data = zlib.compress(text, zlib.Z_BEST_COMPRESSION)

    # To make decompression a little easier, we prepend the compressed data
    # with the size of the uncompressed data as a 24 bits BE unsigned integer.
    assert len(text) < 1 << 24, 'Uncompressed JSON must be < 16 MiB.'
    data = struct.pack('>I', len(text))[1:4] + data

    step = 20
    slices = (data[i:i+step] for i in range(0, len(data), step))
    slices = [','.join(str(c) for c in s) for s in slices]
    text = ',\n'.join(slices)

    with open(sys.argv[2], 'w') as fp:
        fp.write(text)
