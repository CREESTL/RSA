import random

LEFT_BORDER = 10
RIGHT_BORDER = 15

# TODO p and q should be prime - DONE
# TODO e should be co-prime to prod!!! - DONE
# TODO e should be smaller than prod - DONE
# TODO number e should be prime! - DONE


# The maximum size of block of characters from the text
BLOCK_SIZE = None


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
    # Get the smallest of two numbers
    m = min(a, b)
    # The divider of two numbers
    div = None
    # Iterate up to the smallest of the numbers
    for i in range(1, m + 1):
        if (a % i == 0) and (b % i == 0):
            div = i
    if div == 1:
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
# d - co-prime number
# prod - (p-1)*(q-1)
def find_e(d, prod):
    # Options of (e * d)
    options = [(prod * i + 1) for i in range(100)]
    # 'e' values from those options
    es = [int(el / d) for el in options]
    # only prime numbers should be left
    es = list(filter(check_prime, es))
    for e in es:
        if check_co_prime(e, prod) and e < prod:
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
    d = find_co_prime((p-1)*(q-1))
    e = find_e(d, (p-1)*(q-1))
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
