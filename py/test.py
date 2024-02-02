#!/usr/bin/env python3

from base import *

import pickle

print(len(CONTEXT))
f = open('test','wb')
f.write(pickle.dumps(CONTEXT))
