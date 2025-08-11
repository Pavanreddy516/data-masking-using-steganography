# 🔐 Steganography Web Application – Hide Secret Messages in Images

A secure Flask-based web application that lets users **hide** and **extract** confidential messages within images using **Caesar cipher encryption** and **LSB (Least Significant Bit) steganography**.

---

## 📸 Project Summary

This project combines cryptographic principles and steganographic techniques in a user-friendly web application. It allows users to:
- Register/Login securely using hashed passwords
- Generate JWT tokens for session control
- Encrypt a secret message using Caesar Cipher
- Embed the encrypted message into an image (PNG/JPG)
- Extract and decrypt hidden messages from images using a password

This project is ideal for educational purposes and demonstrates secure data hiding using basic cryptography and image processing.

---

## 🚀 Features

| Feature                     | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| 👥 User Authentication       | Register and login using hashed passwords (Flask Sessions + MongoDB)        |
| 🔐 JWT Token Generation     | Role-based identity token using Flask-JWT-Extended                          |
| 🧠 Caesar Cipher Encryption | Password-based shift encryption for hidden data                             |
| 🖼️ LSB Steganography        | Hide encrypted messages inside image pixels                                 |
| 🧩 Message Extraction       | Extract and decrypt messages with password verification                     |
| 📁 Upload & Save Images     | Store uploaded and encoded images in separate folders                       |
| 🌐 Web Interface            | Built with HTML templates for interaction (Jinja2 templating)               |
| ⚠️ Session Management       | Restricted access to sensitive routes (e.g., `/steganography`)              |

---

## 🧰 Technology Stack

| Layer       | Tech                             |
|-------------|----------------------------------|
| Backend     | Python, Flask                    |
| Frontend    | HTML, Jinja2 (Flask Templates)   |
| Database    | MongoDB Atlas (cloud-hosted)     |
| Auth        | JWT + Flask Sessions             |
| Encryption  | Caesar Cipher                    |
| Steganography | LSB (Least Significant Bit)     |
| Libraries   | Pillow (PIL), PyMongo, Flask-CORS|

---


## 📦 Installation & Setup

### ✅ Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- MongoDB Atlas account (free tier is sufficient)

---

### 🔧 Step-by-Step Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-username/steganography-web-app.git
cd steganography-web-app

2. **Install the dependencies**

```bash
pip install -r requirements.txt
