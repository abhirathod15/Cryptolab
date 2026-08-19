def load_dictionary(filename):
    words = set()

    with open(filename, "r") as file:
        for line in file:
            words.add(line.strip().lower())

    return words


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


def dictionary_score(text, dictionary):
    words = text.lower().split()
    score = 0

    for word in words:
        word = word.strip(".,!?;:")
        if word in dictionary:
            score += 1

    return score


def find_key(ciphertext, dictionary):
    best_key = 0
    best_score = -1
    best_text = ""

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = dictionary_score(plaintext, dictionary)

        if score > best_score:
            best_score = score
            best_key = key
            best_text = plaintext

    return best_key, best_text, best_score


dictionary = load_dictionary(
    "attacks/shift_cipher_attack/dictionary/english_words.txt"
)

ciphertext = input("Enter ciphertext: ")

key, plaintext, score = find_key(ciphertext, dictionary)

print("Predicted key:", key)
print("Decrypted text:", plaintext)
print("Dictionary score:", score)
