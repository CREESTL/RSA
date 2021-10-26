import random
from time import time

# Borders containing 'p' and 'q' values
# The more numbers are between these borders - the slower the program works!
# 1 and 100 is OK for English
# 1 and 500 is OK for English and Russian
LEFT_BORDER = 1
RIGHT_BORDER = 500


# Function gets the greatest common divisor of two numbers using Euclid's algorithm
def gcd(a, b) -> int:
    while b != 0:
        a, b = b, a % b
    return a


# Function finds the multiplicative inverse of the number
def rev_mod(d, phi) -> int:
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
    # Generate two random numbers in the borders
    p = random.randint(LEFT_BORDER, RIGHT_BORDER)
    q = random.randint(LEFT_BORDER, RIGHT_BORDER)
    # Than change them until both are prime
    while not check_prime(p):
        p -= 1
    while not check_prime(q):
        q += 1
    # These numbers should not be the same!
    if p == q:
        return generate_p_q()
    return p, q


# Function checks if a number is prime
def check_prime(num) -> bool:
    div = None
    # Find all dividers of the number
    for i in range(1, num):
        if num % i == 0:
            div = i
    # If the only divider is '1' - the number is prime
    if div == 1:
        return True
    else:
        return False


# Function checks if two numbers are co-primes
def check_co_prime(a, b) -> bool:
    # They are co-primes only if their GCD is 1
    if gcd(a, b) == 1:
        return True
    else:
        return False


# Function finds a co-prime number for another given number
def find_co_prime(num) -> int:
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
def encode(text, key) -> str:
    e, n = key
    res = [ord(char) ** e % n for char in text]
    res = to_text(res)
    return res


# Function decodes encoded text
def decode(text, key) -> str:
    d, n = key
    res = [ord(char) ** d % n for char in text]
    res = to_text(res)
    return res


if __name__ == "__main__":
    # Getting a raw user input
    raw_text = input("Enter text to encode: ")
    # Start measuring time
    start = time()
    # Generating integers to work with
    p, q = generate_p_q()
    # Each character is converted to number using ord(). No number converted this way must be bigger than 'n'!!!!
    # The bigger 'p' and 'q' are (set LEFT_BORDER and RIGHT_BORDER wider) - the more characters the program will work
    # with correctly. It's better if 'p' * 'q' is bigger than 2000
    # If 'n' is too small - the program will crash even on Latin characters sometimes...
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
    # Printing the results
    try:
        print(f"Encoded text is: {encoded_text}")
    except UnicodeEncodeError:
        # Not each time 'to_text()' works correctly because the encoded numbers might be too big
        print("Encoded text can't be printed in Unicode symbols, sorry.")
    print(f"Decoded text is: {decoded_text}")
    # Stop measuring time
    end = time()
    time_dif = end - start
    print(f"The program took {time_dif} seconds to finish.")