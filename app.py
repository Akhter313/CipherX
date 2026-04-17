from flask import Flask, render_template, request, abort
import base64
import math

app = Flask(__name__)


# -------------------------
# Core cipher helpers
# -------------------------
def xor_cipher(text, key):
    key = key % 256
    return ''.join(chr(ord(c) ^ key) for c in text)


def caesar_cipher(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def rot13_cipher(text):
    return caesar_cipher(text, 13)


def substitution_cipher(text, key):
    # Kept as a shift-based substitution variant for compatibility with the UI.
    return caesar_cipher(text, key)


def shift_cipher(text, key, action):
    shift = -key if action == 'decrypt' else key
    return caesar_cipher(text, shift)


def base64_encode(text):
    return base64.b64encode(text.encode()).decode()


def base64_decode(text):
    try:
        return base64.b64decode(text).decode()
    except Exception:
        return "Invalid Base64 input"


def reverse_cipher(text):
    return text[::-1]


def binary_encode(text):
    return ' '.join(format(ord(c), '08b') for c in text)


def binary_decode(text):
    try:
        parts = text.split()
        if not parts:
            return "Invalid binary input"

        chars = []
        for part in parts:
            if len(part) != 8 or any(ch not in "01" for ch in part):
                return "Invalid binary input"
            chars.append(chr(int(part, 2)))

        return ''.join(chars)
    except Exception:
        return "Invalid binary input"


def hex_encode(text):
    return text.encode().hex()


def hex_decode(text):
    try:
        return bytes.fromhex(text).decode()
    except Exception:
        return "Invalid hex input"


def caesar_bruteforce(text):
    lines = []
    for shift in range(26):
        lines.append(f"Shift {shift}: {caesar_cipher(text, shift)}")
    return "\n".join(lines)


# -------------------------
# Multiplicative cipher
# -------------------------
def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def multiplicative_encrypt(text, key):
    if math.gcd(key, 26) != 1:
        return "Invalid key (must be coprime with 26)"

    result = []
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result.append(chr(((ord(char) - base) * key) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def multiplicative_decrypt(text, key):
    mod_inv = modinv(key, 26)

    if mod_inv is None:
        return "Invalid key (no modular inverse exists for mod 26)"

    result = []
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result.append(chr(((ord(char) - base) * mod_inv) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    return render_template('base.html')


@app.route('/crypto/<method>', methods=['GET', 'POST'])
def crypto(method):
    supported_methods = {
        'xor', 'caesar', 'rot13', 'substitution',
        'base64', 'reverse', 'multiplicative',
        'binary', 'hex', 'bruteforce'
    }

    if method not in supported_methods:
        abort(404)

    result = ''

    if request.method == 'POST':
        text = request.form.get('text', '')
        key = request.form.get('key', type=int)
        action = request.form.get('action', '')

        if method == 'xor':
            result = "Key is required" if key is None else xor_cipher(text, key)

        elif method == 'caesar':
            result = "Key is required" if key is None else shift_cipher(text, key, action)

        elif method == 'rot13':
            result = rot13_cipher(text)

        elif method == 'substitution':
            result = "Key is required" if key is None else shift_cipher(text, key, action)

        elif method == 'base64':
            result = base64_encode(text) if action == 'encode' else base64_decode(text)

        elif method == 'reverse':
            result = reverse_cipher(text)

        elif method == 'multiplicative':
            if key is None:
                result = "Key is required"
            else:
                result = multiplicative_encrypt(text, key) if action == 'encrypt' else multiplicative_decrypt(text, key)

        elif method == 'binary':
            result = binary_encode(text) if action == 'encode' else binary_decode(text)

        elif method == 'hex':
            result = hex_encode(text) if action == 'encode' else hex_decode(text)

        elif method == 'bruteforce':
            result = caesar_bruteforce(text)

    return render_template('crypto.html', result=result, method=method)


if __name__ == "__main__":
    app.run(debug=True)
