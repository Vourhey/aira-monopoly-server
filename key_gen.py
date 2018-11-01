from ecdsa import SigningKey, SECP256k1
import sha3

def __generate_raw():
    keccak = sha3.keccak_256()

    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak.update(pub)
    return keccak.hexdigest()

def new_address():
    address = __generate_raw()[24:]
    return '0x' + address

def new_tx():
    return '0x' + __generate_raw()
