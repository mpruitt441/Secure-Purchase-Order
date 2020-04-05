from Crypto.PublicKey import RSA

def generate():
    key = RSA.generate(2048)

    f = open('key.pem', 'wb')
    f.write(key.exportKey('PEM'))
    f.close()

def publicExport(filename, forwho):
    f = open(filename, 'r')
    pubkey = RSA.importKey(f.read()).publickey().exportKey('PEM')
    fnew = open(forwho + filename, 'wb')
    fnew.write(pubkey)
    f.close()
    fnew.close()
