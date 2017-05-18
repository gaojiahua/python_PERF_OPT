# Python 密码学

> 使用的Pycrypto
>
> pip  install  pycrypto

## 1. AES
###AES简介

　　美国国家标准技术研究所在2001年发布了高级加密标准（AES）。AES是一个对称分组密码算法，旨在取代DES成为广泛使用的标准。

　　根据使用的密码长度，AES最常见的有3种方案，用以适应不同的场景要求，分别是AES-128、AES-192和AES-256。本文主要对AES-128进行介绍，另外两种的思路基本一样，只是轮数会适当增加。

### 流程

![](pics\aes.png)
　AES加密过程涉及到4种操作：字节替代（SubBytes）、行移位（ShiftRows）、列混淆（MixColumns）和轮密钥加（AddRoundKey）。解密过程分别为对应的逆操作。由于每一步操作都是可逆的，按照相反的顺序进行解密即可恢复明文。加解密中每轮的密钥分别由初始密钥扩展得到。算法中16字节的明文、密文和轮密钥都以一个4x4的矩阵表示。
![](pics\aes_box.png)
![](pics\aes_shiftrows.png)
![](pics\comn_enc.png)

![](pics\key_iter.png)

### 代码示例

```Python
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

secret = os.urandom(BLOCK_SIZE)

cipher = AES.new(secret)
# encode a string
encoded = EncodeAES(cipher, 'password')
print 'Encrypted string:', encoded

# decode the encoded string
decoded = DecodeAES(cipher, encoded)
print 'Decrypted string:', decoded
```


## 2. RSA
```Python
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
 
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
 
# ghost的秘钥对的生成
private_pem = rsa.exportKey()
with open('master-private.pem', 'w') as f:
  f.write(private_pem)
 
public_pem = rsa.publickey().exportKey()
with open('master-public.pem', 'w') as f:
  f.write(public_pem)
```