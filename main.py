import random

# Borders containing 'p' and 'q' values (don't make them too widely spread)
LEFT_BORDER = 10
RIGHT_BORDER = 15

# TODO now works wrong with Russian because in this case ord(char) > n
# TODO bring blocks back ! Make it works with any language from UTF-8


# Function gets the greatest common divisor of two numbers using Euclid's algorithm
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Function finds the multiplicative inverse of the number
def rev_mod(d, phi):
    i = 1
    num = phi * i + 1
    e = num / d
    # Equation is: e * d % phi = 1
    # So each iteration we get one of possible values of e * d, then divide it by d and check if result is integer
    while not e.is_integer():
        i += 1
        num = phi * i + 1
        e = num / d
    return int(e)


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


# Function converts array of integers into text
def to_text(nums) -> str:
    text = ''
    for num in nums:
        text += chr(num)
    return text


# Function encodes a raw text
def encode(text, key):
    e, n = key
    for char in text:
        if ord(char) > n:
            print(f'!!! char is {char} ord is {ord(char)} n is {n}')
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
    e = rev_mod(d, phi)
    # Forming public and private keys
    public_key = (e, n)
    private_key = (d, n)
    # Encoding / Decoding the text
    encoded_text = encode(raw_text, public_key)
    decoded_text = decode(encoded_text, private_key)
    print(f"Encoded text is: {encoded_text}")
    print(f"Decoded text is: {decoded_text}")
