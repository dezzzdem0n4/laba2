import random


def binary(n):
    b = ''
    while n > 0:
        b = b + str(n % 2)
        n = n // 2
    return b


def quick_pow(a, n):
    x = 1
    b = binary(n)
    for i in range(len(b)):
        x = x * pow(a, int(b[i]) * pow(2, i))
    return x


def quick_pow_mod(a, s, n):
    b = binary(s)
    y = a
    x = pow(a, int(b[0]))
    for i in range(1, len(b)):
        y = (pow(y, 2)) % n
        if int(b[i]):
            x = (x * y) % n
    return x


def miller_rabin(n, a):
    n1 = n - 1
    r = 0
    s = 0
    while (n1 % 2 == 0):
        s += 1
        n1 = int(n1 / 2)
    r = n1
    y = quick_pow_mod(a, r, n)
    if y != 1 and y != n - 1:
        j = 1
        while (j <= s - 1 and y != n - 1):
            y = quick_pow_mod(y, 2, n)
            if y == 1:
                return 0
            j += 1
        if y != n - 1:
            return 0
    return 1


def fr2210(number):
    ch = 0
    j = 0
    for i in range(len(number) - 1, -1, -1):
        ch += number[i] * pow(2, j)
        j += 1
    return ch


def chpr(n):
    primes = []
    flag = True
    with open('primes.txt', 'r', encoding='utf-8') as b:
        for line in b:
            if len(primes) > 10000:
                break
            a = line.split()
            for i in range(len(a)):
                a[i] = int(a[i])
            primes.extend(a)
    for i in range(len(primes)):
        if n <= primes[i]:
            return 1
        if n % primes[i] == 0:
            return 0


def gen_prost(k, t):
    pb = 1 - 1 / (quick_pow(4, t))

    while (True):
        number = []

        for i in range(k):
            t = random.randint(0, 1)
            number.append(t)

        number[0] = 1
        number[-1] = 1

        ch2 = fr2210(number)
        x = chpr(ch2)
        if x == 0:
            continue
        p = ch2

        ctr = 0
        for i in range(t):
            ctr += 1
            a = random.randint(2, p - 2)
            check_rabin = miller_rabin(p, a)
            if check_rabin == 1:
                continue
            if check_rabin == 0:
                break

        if ctr == t:
            return p


def phi(p1, p2):
    return (p1 - 1) * (p2 - 1)


def ext_euclid(x, y):
    a2 = 1
    a1 = 0
    b2 = 0
    b1 = 1
    while (y != 0):
        q = (x // y)
        r = x - q * y
        a = a2 - q * a1
        b = b2 - q * b1
        x = y
        y = r
        a2 = a1
        a1 = a
        b2 = b1
        b1 = b
    m = x
    a = a2
    b = b2
    res = [m, a, b]
    return res


def euclid(x, y):
    if x < y:
        x, y = y, x
    while (y != 0):
        r = x % y
        x = y
        y = r
    return x


def e_options(PHI):
    primes = []
    stop_phi = True
    with open('primes.txt', 'r', encoding='utf-8') as b:
        for line in b:
            if len(primes) > 10000:
                break
            a = line.split()
            for i in range(len(a)):
                a[i] = int(a[i])
                if a[i] > PHI:
                    a[i] = 0
                    stop_phi = False

            primes.extend(a)
            if stop_phi is False:
                break

    my_len = len(primes)
    while (2 in primes or 0 in primes):
        my_len = len(primes)
        for i in range(my_len):
            if primes[i] == 2 or primes[i] == 0:
                del primes[i]
                my_len -= 1
                break

    my_len = len(primes)
    while (True):
        nod_false = True
        my_len = len(primes)
        for i in range(my_len):
            NOD = euclid(PHI, primes[i])
            if NOD != 1:
                del primes[i]
                my_len -= 1
                nod_false = False
                break
        if nod_false is False:
            continue
        else:
            break
    return primes


def creating_secret_and_open_key(k):
    t = 10
    p = gen_prost(k, t)
    q = gen_prost(k, t)
    n = p * q
    while (p == q):
        q = gen_prost(k, t)
    PHI = phi(p, q)
    e_primes = e_options(PHI)
    print("•Значения для параметра e: ", e_primes[0:10])
    while (True):
        e = int(input("•Введите e: "))
        if e not in e_primes:
            print("•Ошибка при вводе 'e'!")
            continue
        else:
            break
    publicExponent = e
    N = n
    PublicKey = [publicExponent, N]
    res = ext_euclid(PHI, e)
    d = res[2]
    if d < 0:
        d += PHI
    privateExponent = d
    prime1 = p
    prime2 = q
    exponent1 = d % (p - 1)
    exponent2 = d % (q - 1)
    coefficient = (q - 1) % p
    SecretKey = [privateExponent, prime1, prime2, exponent1,
                 exponent2, coefficient]
    with open('publicKey4.txt', 'w', encoding='utf-8') as f:
        for i in range(len(PublicKey)):
            line = str(PublicKey[i]) + '\n'
            f.write(line)
    print("•Открытый ключ сохранен!")
    with open('secretKey4.txt', 'w', encoding='utf-8') as f:
        for i in range(len(SecretKey)):
            line = str(SecretKey[i]) + '\n'
            f.write(line)
    print("•Закрытый ключ сохранен!")
    return ([PublicKey, SecretKey])


def message_to_arr():
    message = input("•Введите сообщение: ")
    message_arr = []
    for letter in message:
        message_arr.append(ord(letter))
    return message_arr


def encryption(PublicKey):
    brr = message_to_arr()
    crr = []
    for i in range(len(brr)):
        t = quick_pow_mod(brr[i], PublicKey[0], PublicKey[1])
        crr.append(t)
    print("•Зашифрованное сообщение: ", crr)
    return crr


def decryption(SecretKey, PublicKey, crr):
    drr = []
    for i in range(len(crr)):
        t = quick_pow_mod(crr[i], SecretKey[0], PublicKey[1])
        drr.append(t)
    dec_msg = ''
    for i in range(len(drr)):
        t = chr(drr[i])
        dec_msg = dec_msg + t
    print("•Расшифрованное сообщение: ", dec_msg)
    return dec_msg


arr = creating_secret_and_open_key(10)
PublicKey = arr[0]
SecretKey = arr[1]
crr = encryption(PublicKey)
dec_msg = decryption(SecretKey, PublicKey, crr)
