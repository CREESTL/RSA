import random

LEFT_BORDER = 10
RIGHT_BORDER = 15


# The maximum size of block of characters from the text
BLOCK_SIZE = None


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


# Function gets the greatest common divisor of two numbers
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Function generates two large numbers
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
    if gcd(a, b) == 1:
        return True
    else:
        return False


# Function finds a co-prime number for another given number
def find_co_prime(num):
    # All co-prime numbers
    options = list()
    for i in range(num):
        if check_co_prime(i, num):
            options.append(i)
    # Choose one of the numbers
    res = random.choice(options)
    return res


# Function finds an 'e' value of RSA
def find_e(d, phi):
    e = multiplicative_inverse(d, phi)
    return e


# Function splits text to blocks of characters of fixed size
def to_blocks(text) -> [[str]]:
    blocks = [text[k:k + BLOCK_SIZE] for k in range(0, len(text), BLOCK_SIZE)]
    blocks = list(map(list, blocks))
    return blocks


# Function concatenates blocks to text
def to_text(blocks) -> str:
    text = ''
    for block in blocks:
        for num in block:
            text += chr(num)
    return text


# Function encodes a single block of characters
def encode_block(block, key):
    e, n = key
    encoded_block = list()
    for char in block:
        encoded_char = (ord(char) ** e) % n
        encoded_block.append(int(encoded_char))
    return encoded_block


# Function decodes a single block of characters
def decode_block(block, key):
    d, n = key
    decoded_block = list()
    for char in block:
        decoded_char = (ord(char) ** d) % n
        decoded_block.append(int(decoded_char))
    return decoded_block


def encode(text, key):
    # First text should be separated to blocks of fixed size
    blocks = to_blocks(text)
    encoded_blocks = list()
    for block in blocks:
        encoded_blocks.append(encode_block(block, key))
    # Concatenate block to a single string back again
    res = to_text(encoded_blocks)
    return res


def decode(text, key):
    # First text should be separated to blocks of fixed size
    blocks = to_blocks(text)
    decoded_blocks = list()
    for block in blocks:
        decoded_blocks.append(decode_block(block, key))
    # Concatenate block to a single string back again
    res = to_text(decoded_blocks)
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
    # Fix the block size
    BLOCK_SIZE = n
    # Encoding / Decoding the text
    encoded_text = encode(raw_text, public_key)
    decoded_text = decode(encoded_text, private_key)
    print(f"Encoded text is: {encoded_text}")
    print(f"Decoded text is: {decoded_text}")
