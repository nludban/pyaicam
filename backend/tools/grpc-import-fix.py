#!/usr/bin/env python

import sys

# camera2_pb2_grpc.py:
# - import camera2_pb2 as camera2__pb2
# + from . import camera2_pb2 as camera2__pb2

n_flag = False

for path in sys.argv[1:]:
    if path == '-n':
        n_flag = True
        continue
    imp = path.split('/')[-1].split('.')[0]
    if imp.endswith('_grpc'):
        imp = imp[:-5]
    alt = imp.replace('_pb2', '__pb2')  # Probably just one.
    old = f'\nimport {imp} as {alt}\n'
    new = f'\nfrom . import {imp} as {alt}\n'
    src = open(path).read()
    if src.count(old) != 1:
        raise ValueError(f'Expected 1x "{old.strip()}", got {src.count(old)}x.')
    if not n_flag:
        open(path, 'w').write(src.replace(old, new))
    print(path, '(skipping)' if n_flag else '(updated)')

#--#
