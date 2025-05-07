from flask import Flask, render_template, request, url_for
import base64

app = Flask(__name__)

# XOR Cipher
def xor_cipher(text, key):
    return ''.join(chr(ord(c) ^ key) for c in text)

# Caesar Cipher
def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_amount + shift) % 26 + shift_amount)
        else:
            result += char
    return result

# Substitution Cipher
def substitution_cipher(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            shift = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result

# Base64 Encode/Decode
def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    return base64.b64decode(text).decode()

# Reverse Cipher
def reverse_cipher(text):
    return text[::-1]

# Multiplicative Cipher
def multiplicative_encrypt(text, key):
    return ''.join(chr(((ord(char) - 97) * key) % 26 + 97) if char.isalpha() else char for char in text.lower())

def multiplicative_decrypt(text, key):
    mod_inv = modinv(key, 26)
    return ''.join(chr(((ord(char) - 97) * mod_inv) % 26 + 97) if char.isalpha() else char for char in text.lower())

def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/crypto/<method>', methods=['GET', 'POST'])
def crypto(method):
    result = ''
    if request.method == 'POST':
        text = request.form['text']
        key = request.form.get('key', 0, type=int)

        if method == 'xor':
            result = xor_cipher(text, key)
        elif method == 'caesar':
            result = caesar_cipher(text, key)
        elif method == 'substitution':
            result = substitution_cipher(text, key)
        elif method == 'base64':
            action = request.form['action']
            result = base64_encode(text) if action == 'encode' else base64_decode(text)
        elif method == 'reverse':
            result = reverse_cipher(text)
        elif method == 'multiplicative':
            action = request.form['action']
            result = (multiplicative_encrypt(text, key) if action == 'encrypt'
                      else multiplicative_decrypt(text, key))

    return render_template(f'{method}.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
