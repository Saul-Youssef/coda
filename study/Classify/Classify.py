#
#    These are some classes for data searching and classification
#

#   Classify atoms

from base import *

at = data()|data()

#
#    Some test Data
#
EVEN = [data()]
while len(EVEN)<10: EVEN.append(EVEN[-1]+data(at,at))
ODD = [data(at)]
while len(ODD)<10: ODD.append(ODD[-1]+data(at,at))

Even = Data(EVEN)
Odd  = Data(ODD)
Atoms = Even+Odd
