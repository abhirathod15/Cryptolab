import string

ENGLISH_FREQUENCIES = {
    'A': 8.167,
    'B': 1.492,
    'C': 2.782,
    'D': 4.253,
    'E': 12.702,
    'F': 2.228,
    'G': 2.015,
    'H': 6.094,
    'I': 6.966,
    'J': 0.153,
    'K': 0.772,
    'L': 4.025,
    'M': 2.406,
    'N': 6.749,
    'O': 7.507,
    'P': 1.929,
    'Q': 0.095,
    'R': 5.987,
    'S': 6.327,
    'T': 9.056,
    'U': 2.758,
    'V': 0.978,
    'W': 2.360,
    'X': 0.150,
    'Y': 1.974,
    'Z': 0.074
}


def decrypt(text, key):
    result = ""

    for ch in text:
        if ch.isupper():
            result += chr((ord(ch) - ord('A') - key) % 26 + ord('A'))
        elif ch.islower():
            result += chr((ord(ch) - ord('a') - key) % 26 + ord('a'))
        else:
            result += ch

    return result


def calculate_chi_square(text):
    letters = [ch.upper() for ch in text if ch.isalpha()]
    total = len(letters)

    if total == 0:
        return float('inf')

    counts = {}

    for letter in string.ascii_uppercase:
        counts[letter] = 0

    for letter in letters:
        counts[letter] += 1

    chi_square = 0

    for letter in string.ascii_uppercase:
        observed = counts[letter]
        expected = (ENGLISH_FREQUENCIES[letter] / 100) * total

        if expected > 0:
            chi_square += ((observed - expected) ** 2) / expected

    return chi_square


def find_key(ciphertext):
    best_key = 0
    best_score = float('inf')
    best_text = ""

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = calculate_chi_square(plaintext)

        if score < best_score:
            best_score = score
            best_key = key
            best_text = plaintext

    return best_key, best_text, best_score


ciphertext = input("Enter ciphertext: ")

key, plaintext, score = find_key(ciphertext)

print("Predicted key:", key)
print("Decrypted text:", plaintext)
print("Chi-Square value:", score)
