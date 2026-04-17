# CipherX


<img width="1920" height="994" alt="Screenshot From 2026-04-17 16-57-40" src="https://github.com/user-attachments/assets/44e6d845-d069-4b68-b3ea-78924a1af28a" />
<br>
<img width="1920" height="991" alt="Screenshot From 2026-04-17 16-59-19" src="https://github.com/user-attachments/assets/5e9d871d-0fed-4201-9d86-da109375f5a5" />


## Overview

CipherX is a Flask based web app I built as a cybersecurity student to practice classical cryptography concepts in a simple, hands-on way. It brings common cipher and encoding methods into one place, so text can be encrypted, decrypted, encoded, decoded, or tested without switching between different tools.

## Features

- Caesar, Substitution, XOR, and Multiplicative cipher tools
- Base64, Binary, and Hex encoding/decoding
- ROT13 and Reverse text utilities
- Caesar brute force output for all 26 shifts
- Responsive interface with a readable result area
- Simple structure for understanding how each algorithm works

## Tech Stack

- Python
- Flask
- HTML
- CSS

## Project Structure

```text
CipherX/
|-- app.py
|-- requirements.txt
|-- static/
|   `-- css/
|       `-- style.css
|-- templates/
|   |-- base.html
|   `-- crypto.html
`-- README.md
```

## Getting Started

Clone the repository and open the project folder:

```bash
git clone <your-repo-url>
cd CipherX
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python3 app.py
```

Open the local server:

```text
http://127.0.0.1:5000
```

## How It Works

The home page lists the available tools. After selecting a tool, enter the text, choose the action if the tool has one, and provide a numeric key for keyed ciphers.

The actions depend on the method:

- Caesar, Substitution, XOR, and Multiplicative use `Encrypt` and `Decrypt`.
- Base64, Binary, and Hex use `Encode` and `Decode`.
- ROT13 and Reverse only need one action because running them again returns the original text.
- Brute force lists all 26 Caesar shifts for the entered text.

## Learning Focus

This project is mainly for understanding the basics behind classical ciphers, key based transformations, encoding formats, and brute force testing. It is useful for practicing how plaintext changes under different methods and how weak classical ciphers can be reversed.


## Author

Kamal Akhter
