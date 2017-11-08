def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        if 64 < ord(plaintext[i]) < 65 + 26:
            shift = (ord(keyword[i % len(keyword)]) - 65)
            if ord(plaintext[i]) > 64 + 26 - shift:
                ciphertext += chr(ord(plaintext[i]) + shift - 26)
            else:
                ciphertext += chr(ord(plaintext[i]) + shift)
        elif 96 < ord(plaintext[i]) < 97 + 26:
            shift = (ord(keyword[i % len(keyword)]) - 97)
            if ord(plaintext[i]) > 96 + 26 - shift:
                ciphertext += chr(ord(plaintext[i]) + shift - 26)
            else:
                ciphertext += chr(ord(plaintext[i]) + shift)
        else:
            ciphertext += i
    return ciphertext


def decrypt_vigenere(plaintext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        if 64 < ord(plaintext[i]) < 65 + 26:
            shift = (ord(keyword[i % len(keyword)]) - 65)
            if ord(plaintext[i]) < 64 + shift:
                ciphertext += chr(ord(plaintext[i]) + 26 - shift)
            else:
                ciphertext += chr(ord(plaintext[i]) - shift)
        elif 96 < ord(plaintext[i]) < 97 + 26:
            shift = (ord(keyword[i % len(keyword)]) - 97)
            if ord(plaintext[i]) < 96 + shift:
                ciphertext += chr(ord(plaintext[i]) + shift - 26)
            else:
                ciphertext += chr(ord(plaintext[i]) + shift)
        else:
            ciphertext += i
    return ciphertext
