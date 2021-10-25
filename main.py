import random

# Borders containing 'p' and 'q' values (don't make them too widely spread)
LEFT_BORDER = 10
RIGHT_BORDER = 15


# Function gets the greatest common divisor of two numbers using Euclid's algorithm
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Standard Euclid's algorithm can be extended to find, given a and b, integers 'x' and 'y' such that 'ax + by = d',
# where 'd' is the greatest common divisor of 'a' and 'b'
def ext_gcd(a, b):
    if a == 0:
        gcd = b
        # 'x' from description
        c1 = 0
        # 'y' from description
        c2 = 1
        return gcd, c1, c2
    else:
        gcd, c1, c2 = ext_gcd(b % a, a)
        return gcd, c2 - (b // a) * c1, c1


# Function find the multiplicative inverse of the number
# Let's call some mul.inv. 'b'
# It is mul.inv for 'a' modulo 'c' if:
# a * b % c = 1
# Function is used to calculate 'd' value for 'e' value in RSA
def mul_inv(num, mod):
    g, x, _ = ext_gcd(num, mod)
    if g == 1:
        return x % mod


# Function generates two prime numbers
def generate_p_q():
    p = random.randint(LEFT_BORDER, RIGHT_BORDER)
    q = random.randint(LEFT_BORDER, RIGHT_BORDER)
    while not check_prime(p):
        p -= 1
    while not check_prime(q):
        q += 1
    # These numbers should not be the same!
    if p == q:
        return generate_p_q()
    return p, q


# Function checks if a number is prime
def check_prime(num):
    div = None
    for i in range(1, num):
        if num % i == 0:
            div = i
    if div == 1:
        return True
    else:
        return False


# Function checks if two numbers are co-primes
def check_co_prime(a, b):
    # They are co-primes only if their GCD is 1
    if gcd(a, b) == 1:
        return True
    else:
        return False


# Function finds a co-prime number for another given number
def find_co_prime(num):
    options = list()
    for i in range(num):
        if check_co_prime(i, num):
            options.append(i)
    # Choose one of the numbers from the list
    res = random.choice(options)
    return res


# Function finds an 'e' value of RSA
def find_e(d, phi):
    # 'e' is a multiplicative inverse of d modulo phi
    e = mul_inv(d, phi)
    return e


# Function converts array of integers into text
def to_text(nums) -> str:
    text = ''
    for num in nums:
        text += chr(num)
    return text


# Function encodes a raw text
def encode(text, key):
    e, n = key
    res = [ord(char) ** e % n for char in text]
    res = to_text(res)
    return res


# Function decodes encoded text
def decode(text, key):
    d, n = key
    res = [ord(char) ** d % n for char in text]
    res = to_text(res)
    return res


if __name__ == "__main__":
    # Getting a raw user input
    raw_text = input("Enter text to encode (UTF-8 characters only!): ")
    # Generating integers to work with
    p, q = generate_p_q()
    n = p * q
    phi = (p-1) * (q-1)
    d = find_co_prime(phi)
    e = find_e(d, phi)
    # Forming public and private keys
    public_key = (e, n)
    private_key = (d, n)
    # Encoding / Decoding the text
    encoded_text = encode(raw_text, public_key)
    decoded_text = decode(encoded_text, private_key)
    print(f"Encoded text is: {encoded_text}")
    print(f"Decoded text is: {decoded_text}")
