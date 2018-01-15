#1/usr/bin/env python
"""Tests various fucntions related to reading and writing java properties files

    Note that there is an issue with comments that start
    with # as only one is read per file so I am ignoring it.

"""

import jprops
import os

from collections import OrderedDict


DEFAULTS = OrderedDict()

DEFAULTS.update( {
            'timeout': "0",
            'tail': "False",
            'bucket': 'S3://foo/bar-baz',
})

FILES = [
    'cluster.properties',
    'java.properties',
    'service.properties',
    'utf8.properties',
    'wiki.properties',
]

pwd = os.getcwd()

for pfile in FILES:
    values = OrderedDict()
    # Should autodetect utf8 or latin-1
    with open(pwd + "/tests/" + pfile, mode="r") as f:
        values = jprops.load_properties(f, OrderedDict)
        # This will write out in latin-1 unless utf8 data exists,
        # switching mode to "wb" forces latin-1
        with open(pwd + "/out/" + pfile, mode="w") as w:
            jprops.store_properties(w, values)

        # Append this file to the DEFAULTS dict
        DEFAULTS.update(values)

# use "wb" so that UTF8 is escaped for java as \uffff and encoded as latin-1
with open(pwd + "/out/all.properties", mode="wb") as a:
    jprops.store_properties(a, DEFAULTS)

# force utf8 output
with open(pwd + "/out/all-utf8.properties", mode="w", encoding='utf-8') as a:
    jprops.store_properties(a, DEFAULTS)
