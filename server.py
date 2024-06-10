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
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # 选择一个公开的 e
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

def check(blinding_factor, private_key):
    try:
        a = pow(blinding_factor, -1, private_key)
    except:
        return False
    return True

def signfunc(private_key, blind_m):
    signature = pow(blind_m, private_key[0], private_key[1])
    return signature

# 生成密钥对
public_key, private_key = generate_keypair()
print(f"Public key e = {public_key[0]}, n = {public_key[1]}")



def cast():
    print("option 1: vote")
    print("option 2: exit")
    option = int(input("option = "))
    if(option != 1 and option != 2):
        print("Invalid option")
        return cast()
    return option
def Verify(VotingResult, signature_unblind, public_key):
    e, n = public_key
    return VotingResult == pow(signature_unblind, e, n)
def VerifyVoter(name, id, encm, checkencm):
    return encm == decrypt((name, id), checkencm)


Result = {}
Voted = set()

while(cast() != 2):
    name , id = map(int,input("name, id = ").split())
    encm , ckeckencm = map(int,input("encm ,checkencm = ").split())
    if VerifyVoter(name, id, encm, ckeckencm) == False and id in Voted:
        print("identity verification failed")
        continue
    else:
        print("identity verification success")
        Voted.add(name)
    # print(encm)
    signature = signfunc(private_key, encm)
    print(f"signature = {signature}")
    VotingResult, signature_unblind = map(int,input("VotingResult, signature_unblind = ").split())
    if Verify(VotingResult, signature_unblind, public_key):
        print("Voting success")
        if VotingResult not in Result:
            Result[VotingResult] = 1
        else:
            Result[VotingResult] += 1
    else:
        print("Voting fail")
    print()

for key, value in Result.items():
    print(f"VotingResult:{key} count: {value}")