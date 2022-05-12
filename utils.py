import hashlib

def md5_password(password):
    pwdBytes = password.encode(encoding='UTF-8', errors='strict')
    h = hashlib.md5()
    h.update(pwdBytes)
    return h.hexdigest()



    