def encrypt(text, key):
    result = ""

    for ch in text:
        if ch.isupper():
            result += chr((ord(ch) - ord('A') + key) % 26 + ord('A'))
        elif ch.islower():
            result += chr((ord(ch) - ord('a') + key) % 26 + ord('a'))
        else:
            result += ch

    return result


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


print("Shift Cipher")

choice = input("Enter E for Encryption or D for Decryption: ").upper()
text = input("Enter text: ")
key = int(input("Enter key (0-25): "))

if choice == "E":
    print("Encrypted text:", encrypt(text, key))
elif choice == "D":
    print("Decrypted text:", decrypt(text, key))
else:
    print("Invalid choice")
