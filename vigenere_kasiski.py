import re
from collections import Counter, defaultdict

# English letter frequencies
ENGLISH_FREQ = [
    0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020,
    0.061, 0.070, 0.0015, 0.0077, 0.040, 0.024, 0.067,
    0.075, 0.019, 0.00095, 0.060, 0.063, 0.091, 0.028,
    0.0098, 0.024, 0.0015, 0.020, 0.00074
]


# 1. PREPROCESS CIPHERTEXT
def clean_ciphertext(ciphertext):
    return re.sub(r'[^A-Z]', '', ciphertext.upper())


# 2. FIND REPEATED PATTERNS
def find_repeated_patterns(ciphertext, min_length=3, max_length=5):
    patterns = defaultdict(list)

    for length in range(min_length, max_length + 1):
        for i in range(len(ciphertext) - length + 1):
            pattern = ciphertext[i:i + length]
            patterns[pattern].append(i)

    return {
        pattern: positions
        for pattern, positions in patterns.items()
        if len(positions) > 1
    }


# 3. CALCULATE DISTANCES
def calculate_distances(repeated_patterns):
    distances = []

    for pattern, positions in repeated_patterns.items():
        for i in range(len(positions) - 1):
            distance = positions[i + 1] - positions[i]
            distances.append((pattern, distance))

    return distances


# 4. FIND FACTORS
def find_factors(distances, max_key_length=20):
    factor_count = Counter()

    for pattern, distance in distances:
        for factor in range(2, max_key_length + 1):
            if distance % factor == 0:
                factor_count[factor] += 1

    return factor_count


# 5. INDEX OF COINCIDENCE
def calculate_ic(group):
    n = len(group)

    if n <= 1:
        return 0

    counts = Counter(group)

    numerator = sum(
        count * (count - 1)
        for count in counts.values()
    )

    denominator = n * (n - 1)

    return numerator / denominator


# 6. KASISKI ANALYSIS
def kasiski_analysis(ciphertext):

    repeated = find_repeated_patterns(ciphertext)

    distances = calculate_distances(repeated)

    factor_count = find_factors(distances)

    print("\n========== KASISKI ANALYSIS ==========")

    print("\nRepeated patterns:")

    for pattern, positions in sorted(repeated.items()):
        print(pattern, "-> positions", positions)

    print("\nDistances:")

    for pattern, distance in distances:
        print(
            f"Pattern = {pattern:5s} Distance = {distance}"
        )

    print("\nFactor frequency:")

    for factor, count in factor_count.most_common():
        print(
            f"Key length {factor:2d} -> {count} occurrences"
        )

    candidates = [
        factor
        for factor, count in factor_count.most_common(10)
    ]

    return candidates


# 7. SPLIT CIPHERTEXT INTO GROUPS
def split_into_groups(ciphertext, key_length):

    groups = []

    for i in range(key_length):
        groups.append(ciphertext[i::key_length])

    return groups


# 8. FREQUENCY ANALYSIS
def frequency_analysis(group):

    counts = Counter(group)

    frequencies = {}

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        frequencies[letter] = counts[letter]

    return frequencies


# 9. FIND SHIFT USING CHI-SQUARE
def find_shift(group):

    n = len(group)

    best_shift = 0
    best_score = float("inf")

    for shift in range(26):

        observed = [0] * 26

        for char in group:

            value = (
                ord(char) - ord('A') - shift
            ) % 26

            observed[value] += 1

        chi_square = 0

        for i in range(26):

            expected = n * ENGLISH_FREQ[i]

            if expected > 0:

                chi_square += (
                    (observed[i] - expected) ** 2
                ) / expected

        if chi_square < best_score:

            best_score = chi_square
            best_shift = shift

    return best_shift, best_score


# 10. FIND PROBABLE KEY
def find_key(groups):

    key = ""

    print("\n========== SHIFT ANALYSIS ==========")

    for i, group in enumerate(groups):

        shift, score = find_shift(group)

        letter = chr(ord('A') + shift)

        print(
            f"Group {i + 1:2d}: "
            f"Shift = {shift:2d}, "
            f"Key letter = {letter}, "
            f"Chi-square = {score:.2f}"
        )

        key += letter

    return key


# 11. VIGENERE DECRYPTION
def vigenere_decrypt(ciphertext, key):

    plaintext = ""

    for i, char in enumerate(ciphertext):

        cipher_value = ord(char) - ord('A')

        key_value = (
            ord(key[i % len(key)]) - ord('A')
        )

        plain_value = (
            cipher_value - key_value
        ) % 26

        plaintext += chr(
            ord('A') + plain_value
        )

    return plaintext


# 12. VIGENERE ENCRYPTION
def vigenere_encrypt(plaintext, key):

    ciphertext = ""

    for i, char in enumerate(plaintext):

        plain_value = ord(char) - ord('A')

        key_value = (
            ord(key[i % len(key)]) - ord('A')
        )

        cipher_value = (
            plain_value + key_value
        ) % 26

        ciphertext += chr(
            ord('A') + cipher_value
        )

    return ciphertext


# 13. VERIFICATION
def verify(original_ciphertext, plaintext, key):

    encrypted = vigenere_encrypt(
        plaintext,
        key
    )

    print("\n========== VERIFICATION ==========")

    if encrypted == original_ciphertext:

        print("Re-encrypted ciphertext matches original.")
        print("Verification SUCCESSFUL!")

    else:

        print("Re-encrypted ciphertext does NOT match.")
        print("Verification FAILED!")


# DISPLAY FREQUENCY TABLES
def display_frequency_tables(groups):

    print("\n========== FREQUENCY TABLES ==========")

    for i, group in enumerate(groups):

        frequencies = frequency_analysis(group)

        print(
            f"\nGroup {i + 1} "
            f"(length = {len(group)}):"
        )

        print(
            " ".join(
                f"{letter}:{frequencies[letter]}"
                for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            )
        )

        print(
            f"IC = {calculate_ic(group):.4f}"
        )


# MAIN ANALYSIS
def analyze(ciphertext):

    # Preprocess
    ciphertext = clean_ciphertext(ciphertext)

    print("\n======================================")
    print("VIGENERE CIPHER CRYPTANALYSIS")
    print("======================================")

    print(
        "\nClean ciphertext length:",
        len(ciphertext)
    )

    # Kasiski examination
    candidates = kasiski_analysis(ciphertext)

    print(
        "\nKasiski candidate key lengths:",
        candidates
    )

    # IC analysis
    print("\n========== IC ANALYSIS ==========")

    ic_results = []

    for key_length in candidates:

        groups = split_into_groups(
            ciphertext,
            key_length
        )

        average_ic = sum(
            calculate_ic(group)
            for group in groups
        ) / len(groups)

        ic_results.append(
            (key_length, average_ic)
        )

        print(
            f"Key length {key_length:2d} "
            f"-> Average IC = {average_ic:.4f}"
        )

    # Estimate key length
    if ic_results:

        estimated_key_length = max(
            ic_results,
            key=lambda x: x[1]
        )[0]

    else:

        estimated_key_length = candidates[0]

    print(
        "\nEstimated key length:",
        estimated_key_length
    )

    # Divide ciphertext into groups
    groups = split_into_groups(
        ciphertext,
        estimated_key_length
    )

    print(
        "\nCiphertext divided into",
        estimated_key_length,
        "groups."
    )

    # Frequency analysis
    display_frequency_tables(groups)

    # Find key
    key = find_key(groups)

    print("\n========== RECOVERED KEY ==========")
    print("Key:", key)

    # Decrypt
    plaintext = vigenere_decrypt(
        ciphertext,
        key
    )

    print("\n========== RECOVERED PLAINTEXT ==========")
    print(plaintext)

    # Verify
    verify(
        ciphertext,
        plaintext,
        key
    )


# =========================================================
# CIPHERTEXT 2 - EVEN GROUP NUMBER
# =========================================================

CIPHERTEXT_2 = """
QRBAI UWYOK ILBRZ XTUWL EGXSN VDXWR XMHXY FCGMW
WWSME LSXUZ
MKMFS BNZIF YEIEG RFZRX WKUFA XQEDX DTTHY NTBRJ
LHTAI KOCZX
QHBND ZIGZG PXARJ EDYSJ NUMKI FLBTN HWISW NVLFM
EGXAI AAWSL
FMHXR SGRIG HEQTU MLGLV BRSIL AEZSG XCMHT OWHFM
LWMRK HPRFB
ELWGF RUGPB HNBEM KBNVW HHUEA KILBN BMLHK XUGML
YQKHP RFBEL
EJYNV WSIJB GAXGO TPMXR TXFKI WUALB RGWIE GHWHG
AMEWW LTAEL
NUMRE UWTBL SDPRL YVRET LEEDF ROBEQ UXTHX ZYOZB
XLKAC KSOHN
VWXKS MAEPH IYQMM FSECH RFYPB BSQTX TPIWH GPXQD
FWTAI KNNBX

SIYKE TXTLV BTMQA LAGHG OTPMX RTXTH XSFYG WMVKH
LOIVU ALMLD
LTSYV WYNVW MQVXP XRVYA BLXDL XSMLW SUIOI IMELI
SOYEB HPHNR
WTVUI AKEYG WIETG WWBVM VDUMA EPAUA KXWHK MAUPA
MUKHQ PWKCX
EFXGW WSDDE OMLWL NKMWD FWTAM FAFEA MFZBN WIHYA
LXRWK MAMIK
GNGHJ UAZHM HGUAL YSULA ELYHJ BZMSI LAILH WWYIK
EWAHN PMLBN
NBVPJ XLBEF WRWGX KWIRH XWWGQ HRRXW IOMFY CZHZL
VXNVI OYZCM
YDDEY IPWXT MMSHS VHHXZ YEWNV OAOEL SMLSW KXXFX
STRVI HZLEF
JXDAS FIE
"""


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    print("\n======================================")
    print("EVEN GROUP - CIPHERTEXT 2")
    print("======================================")

    analyze(CIPHERTEXT_2)
