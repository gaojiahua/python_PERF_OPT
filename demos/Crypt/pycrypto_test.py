# -*- coding: utf-8 -*-
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64 
# 伪随机数生成器
random_generator = Random.new().read
# rsa算法生成实例
rsa = RSA.generate(1024, random_generator)
 
# master的秘钥对的生成
private_pem = rsa.exportKey()
 
with open('master-private.pem', 'w') as f:
  f.write(private_pem)
 
public_pem = rsa.publickey().exportKey()
with open('master-public.pem', 'w') as f:
  f.write(public_pem)
 
message = 'hello ghost, this is a plain text'
with open('master-public.pem') as f:
	key = f.read()
	rsakey = RSA.importKey(key)
	cipher = Cipher_pkcs1_v1_5.new(rsakey)
	cipher_text = base64.b64encode(cipher.encrypt(message))
	print cipher_text
 
with open('master-private.pem') as f:
	key = f.read()
	rsakey = RSA.importKey(key)
	cipher = Cipher_pkcs1_v1_5.new(rsakey)
	text = cipher.decrypt(base64.b64decode(cipher_text), random_generator)
	print text