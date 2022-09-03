def get_ase_128(key,str):
    mode = AES.MODE_CBC
    BS = AES.block_size  # aes数据分组长度为128 bit
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    iv = '\0'*16
    cryptor = AES.new(base64.b64decode(key), mode, iv)
    pad_str = pad(str)
    ciphertext = cryptor.encrypt(pad_str)
    return ciphertext
