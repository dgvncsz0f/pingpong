# -*- coding: utf-8 -*-

# Copyright (c) 2011, Diego Souza
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#   * Neither the name of the <ORGANIZATION> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import binascii
from pingpong.pycrypto.asn1 import DerObject, DerSequence

# Note: You find this method on RSA.py on newer versions.
#       We are inserting it here in order to support older pycrypto versions.
def exportKey(rsaobj, format='PEM'):
    """Export the RSA key. A string is returned
    with the encoded public or the private half
    under the selected format.

    format:		'DER' (PKCS#1) or 'PEM' (RFC1421)
    """
    der = DerSequence()
    if rsaobj.has_private():
        keyType = "RSA PRIVATE"
        der[:] = [ 0, rsaobj.n, rsaobj.e, rsaobj.d, rsaobj.p, rsaobj.q,
                   rsaobj.d % (rsaobj.p-1), rsaobj.d % (rsaobj.q-1),
                   rsaobj.u ]
    else:
        keyType = "PUBLIC"
        der.append('\x30\x0D\x06\x09\x2A\x86\x48\x86\xF7\x0D\x01\x01\x01\x05\x00')
        bitmap = DerObject('BIT STRING')
        derPK = DerSequence()
        derPK[:] = [ rsaobj.n, rsaobj.e ]
        bitmap.payload = '\x00' + derPK.encode()
        der.append(bitmap.encode())
    if format=='DER':
        return der.encode()
    if format=='PEM':
        pem = "-----BEGIN %s KEY-----\n" % keyType
        binaryKey = der.encode()
        # Each BASE64 line can take up to 64 characters (=48 bytes of data)
        chunks = [ binascii.b2a_base64(binaryKey[i:i+48]) for i in range(0, len(binaryKey), 48) ]
        pem += ''.join(chunks)
        pem += "-----END %s KEY-----" % keyType
        return pem
    return ValueError("")


