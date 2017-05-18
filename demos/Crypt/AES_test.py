#AES_test.py
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import base64
import os

BLOCK_SIZE = 32

PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

key = os.urandom(BLOCK_SIZE)

cipher = AES.new(key)

# encode a string
encoded = EncodeAES(cipher, 'password')
print 'Encrypted string:', encoded

# decode the encoded string
decoded = DecodeAES(cipher, encoded)
print 'Decrypted string:', decoded