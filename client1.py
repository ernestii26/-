import random
import math

#-----------------RSA-----------------
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = egcd(b % a, a)
    return g, y - (b // a) * x, x


def generate_keypair():
    p = 61  # 选择两个素数 p 和 q
    q = 89
    n = p * q
    phi = (p - 1) * (q - 1)

    e = int(1e9 + 7)  # 选择一个公开的 e
    d = modinv(e, phi)  # 计算 d，使得 ed ≡ 1 (mod phi)

    return (e, n), (d, n)


def encrypt(public_key, plaintext):
    e, n = public_key
    ciphertext = pow(plaintext, e, n)
    return ciphertext


def decrypt(private_key, ciphertext):
    d, n = private_key
    plaintext = pow(ciphertext, d, n)
    return plaintext
#-----------------RSA-----------------
# e, n = map(int,input().split())
# public_key = (e, n)
public_key = (65537, 3233)
e, n = public_key
def check(blinding_factor, n):
    try:
        a = pow(blinding_factor, -1, n)
    except:
        return False
    return True

def blinding(public_key, m):
    blinding_factor = random.randint(1, 1000)
    while(check(blinding_factor, public_key[1]) == False):
        blinding_factor = random.randint(1, 1000)
    blind_m = m * pow(blinding_factor, public_key[0]) % public_key[1]
    return (blinding_factor, blind_m)

def unblinding(signature, blinding_factor, public_key):
    return signature * pow(blinding_factor, -1, public_key[1]) % public_key[1]

digital_signature_public_key, digital_signature_private_key = generate_keypair()
print(f"name = {digital_signature_private_key[0]}, id = {digital_signature_private_key[1]}")


m = int(input("who to vote: ")) #
blinding_factor, encm = blinding(public_key, m)
checkencm = encrypt(digital_signature_public_key, encm)
print(f"encm = {encm}, checkencm = {checkencm}")
signature = int(input("signature = "))
unblinding = unblinding(signature, blinding_factor, public_key)
print(pow(unblinding, e, n))
# encm = decrypt(digital_signature_private_key, encm)
# print(encm)
print(f"VotingResult:{m} signature_unblind: {unblinding}")