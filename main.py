from collections import Counter
from datetime import datetime


# -----------------------------
# Task 5: Logging Function
# -----------------------------
def write_log(message):
    current_time = datetime.now()

    with open("outputs/log.txt", "a") as file:
        file.write(str(current_time) + " - " + message + "\n")


# -----------------------------
# Task 4: File Analysis Function
# -----------------------------
def analyze_file():

    filename = "datasets/sample1.txt"

    try:
        with open(filename, "r") as file:
            text = file.read()

        characters = len(text)
        words = len(text.split())
        lines = len(text.splitlines())

        unique_characters = len(set(text))

        letters = Counter(text.lower())

        print("\n========== File Analysis ==========")

        print("File Name:", filename)
        print("Characters:", characters)
        print("Words:", words)
        print("Lines:", lines)
        print("Unique Characters:", unique_characters)

        print("\nLetter Frequency:")

        for letter, count in sorted(letters.items()):
            if letter.isalpha():
                print(letter.upper(), ":", count)

        print("===================================")

    except FileNotFoundError:
        print("File not found!")
        print("Please check datasets/sample1.txt")


# -----------------------------
# Task 3: Menu Function
# -----------------------------
def show_menu():

    print("\n========== CryptoLabX ==========")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Attack")
    print("4. Analyze")
    print("5. Exit")
    print("================================")


# -----------------------------
# Main Program
# -----------------------------

write_log("Program Started")


while True:

    show_menu()

    choice = input("Enter your choice: ")


    if choice == "1":

        write_log("Encrypt Selected")

        print("\nEncrypt Module")
        print("Coming Soon...")


    elif choice == "2":

        write_log("Decrypt Selected")

        print("\nDecrypt Module")
        print("Coming Soon...")


    elif choice == "3":

        write_log("Attack Selected")

        print("\nAttack Module")
        print("Coming Soon...")


    elif choice == "4":

        write_log("Analyze Selected")

        analyze_file()


    elif choice == "5":

        write_log("Exit Selected")

        print("\nThank you for using CryptoLabX!")
        break


    else:

        write_log("Invalid Option Selected")

        print("\nInvalid choice. Try again.")
