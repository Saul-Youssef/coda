#
#   Basic definitions
#
from base import *
import Number
#
#    pass is the identity.  null returns empty data independent of B.
#
CONTEXT.add(DEF(da('pass'),lambda domain,A,B:B))
CONTEXT.add(DEF(da('null'),lambda domain,A,B:data()))

