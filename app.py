from flask import Flask, render_template, request
import base64
import math

app = Flask(__name__)

# -------------------------
# XOR Cipher
# -------------------------
def xor_cipher(text, key):
    key = key % 256  # normalize key
    return ''.join(chr(ord(c) ^ key) for c in text)

# -------------------------
# Caesar Cipher
# -------------------------
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

# -------------------------
# Substitution Cipher (still shift-based, renamed logic)
# -------------------------
def substitution_cipher(text, key):
    # same as Caesar but kept for UI separation
    return caesar_cipher(text, key)

# -------------------------
# Base64 Encode/Decode
# -------------------------
def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    try:
        return base64.b64decode(text).decode()
    except Exception:
        return "Invalid Base64 input"

# -------------------------
# Reverse Cipher
# -------------------------
def reverse_cipher(text):
    return text[::-1]

# -------------------------
# Multiplicative Cipher
# -------------------------
def multiplicative_encrypt(text, key):
    if math.gcd(key, 26) != 1:
        return "Invalid key (must be coprime with 26)"
    
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr(((ord(char) - base) * key) % 26 + base)
        else:
            result += char
    return result

def multiplicative_decrypt(text, key):
    mod_inv = modinv(key, 26)
    
    if mod_inv is None:
        return "Invalid key (no modular inverse exists for mod 26)"
    
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr(((ord(char) - base) * mod_inv) % 26 + base)
        else:
            result += char
    return result

def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/crypto/<method>', methods=['GET', 'POST'])
def crypto(method):
    result = ''
    
    if request.method == 'POST':
        text = request.form.get('text', '')
        key = request.form.get('key', type=int)

        # Validation
        if method not in ['reverse', 'base64'] and (key is None):
            result = "Key is required"
            return render_template(f'{method}.html', result=result)

        if method == 'xor':
            result = xor_cipher(text, key)

        elif method == 'caesar':
            result = caesar_cipher(text, key)

        elif method == 'substitution':
            result = substitution_cipher(text, key)

        elif method == 'base64':
            action = request.form.get('action')
            if action == 'encode':
                result = base64_encode(text)
            else:
                result = base64_decode(text)

        elif method == 'reverse':
            result = reverse_cipher(text)

        elif method == 'multiplicative':
            action = request.form.get('action')
            if action == 'encrypt':
                result = multiplicative_encrypt(text, key)
            else:
                result = multiplicative_decrypt(text, key)

    return render_template(f'{method}.html', result=result)

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
