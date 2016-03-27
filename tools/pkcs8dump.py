#!/usr/bin/env python
#
# This file is part of pyasn1-modules software.
#
# Copyright (c) 2005-2016, Ilya Etingof <ilya@glas.net>
# License: http://pyasn1.sf.net/license.html
#
# Read  bunch of ASN.1/PEM plain/encrypted private keys in PKCS#8 
# format on stdin, parse each into plain text, then build substrate from it
#
from pyasn1.codec.der import decoder, encoder
from pyasn1_modules import rfc5208, pem
import sys

if len(sys.argv) != 1:
    print("""Usage:
$ cat pkcs8key.pem | %s""" % sys.argv[0])
    sys.exit(-1)

cnt = 0

while True:
    idx, substrate = pem.readPemBlocksFromFile(
        sys.stdin,
        ('-----BEGIN PRIVATE KEY-----', '-----END PRIVATE KEY-----'),
        ('-----BEGIN ENCRYPTED PRIVATE KEY-----', '-----END ENCRYPTED PRIVATE KEY-----')
    )
    if not substrate:
        break

    if idx == 0:
        asn1Spec = rfc5208.PrivateKeyInfo()
    elif idx == 1:
        asn1Spec = rfc5208.EncryptedPrivateKeyInfo()
    else:
        break

    key, rest = decoder.decode(substrate, asn1Spec=asn1Spec)

    if rest:
        substrate = substrate[:-len(rest)]

    print(key.prettyPrint())

    assert encoder.encode(key) == substrate, 'pkcs8 recode fails'

    cnt += 1

print('*** %s PKCS#8 key(s) de/serialized' % cnt)
