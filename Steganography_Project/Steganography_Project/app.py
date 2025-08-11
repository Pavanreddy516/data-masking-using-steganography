from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, decode_token
from pymongo import MongoClient
from flask_cors import CORS
from PIL import Image
import os
import hashlib
from datetime import timedelta

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)  # Token expires in 5 minutes
jwt = JWTManager(app)

# MongoDB Configuration
MONGO_URL = "mongodb+srv://Ayyanagouda:7022@cluster0.bttrl.mongodb.net/taskm"
client = MongoClient(MONGO_URL)
db = client['taskm']
users_collection = db['users']

# Flask Session Configuration
app.secret_key = 'your_secret_key'

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if users_collection.find_one({'email': email}):
            return jsonify({'message': 'User already exists. Please login instead.'}), 409

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({'email': email, 'password': hashed_password})
        return jsonify({'message': 'Registration successful! Please login.'}), 201

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Check if the email and password match the default user
    if email == "user@gmail.com" and password == "1234":
        session['user_email'] = email
        flash('Login successful! Welcome to your dashboard.', 'success')
        return redirect(url_for('role_input'))

    user = users_collection.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        session['user_email'] = email
        flash('Login successful!', 'success')
        return redirect(url_for('role_input'))

    flash('Invalid email or password. Please try again.', 'error')
    return redirect(url_for('index'))

@app.route('/role_input', methods=['GET', 'POST'])
def role_input():
    if 'user_email' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        role = request.form.get('role')
        token = create_access_token(identity=session['user_email'])
        return redirect(url_for('view_token', token=token))

    return render_template('role_input.html')

@app.route('/view_token', methods=['GET'])
def view_token():
    token = request.args.get('token', '')
    if not token:
        flash('No token provided.', 'error')
        return redirect(url_for('role_input'))

    return render_template('view_token.html', token=token)

@app.route('/steganography', methods=['GET'])
def steganography():
    if 'user_email' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('index'))

    return render_template('steganography.html')

# Updated to include redirection to steganography after viewing the token
@app.route('/redirect_to_steganography', methods=['POST'])
def redirect_to_steganography():
    token = request.form.get('token', None)
    if not token:
        flash('No token provided.', 'error')
        return redirect(url_for('view_token'))

    try:
        decoded = decode_token(token)
        if decoded:
            return redirect(url_for('steganography'))
    except Exception as e:
        flash('Invalid or expired token. Please try again.', 'error')
        return redirect(url_for('role_input'))


# Caesar Cipher Functions (Used for Steganography)
def caesar_cipher_encrypt(text, shift):
    encrypted_text = ''
    for char in text:
        if char.isalpha():  # For alphabetic characters
            shift_amount = shift % 26
            new_char = chr(((ord(char.lower()) - ord('a') + shift_amount) % 26) + ord('a'))
            if char.isupper():
                new_char = new_char.upper()
            encrypted_text += new_char
        elif char.isdigit():  # For numeric characters
            shift_amount = shift % 10
            new_char = chr(((ord(char) - ord('0') + shift_amount) % 10) + ord('0'))
            encrypted_text += new_char
        else:
            encrypted_text += char  # Non-alphanumeric characters remain unchanged
    return encrypted_text

def caesar_cipher_decrypt(text, shift):
    decrypted_text = ''
    for char in text:
        if char.isalpha():  # For alphabetic characters
            shift_amount = shift % 26
            new_char = chr(((ord(char.lower()) - ord('a') - shift_amount) % 26) + ord('a'))
            if char.isupper():
                new_char = new_char.upper()
            decrypted_text += new_char
        elif char.isdigit():  # For numeric characters
            shift_amount = shift % 10
            new_char = chr(((ord(char) - ord('0') - shift_amount) % 10) + ord('0'))
            decrypted_text += new_char
        else:
            decrypted_text += char  # Non-alphanumeric characters remain unchanged
    return decrypted_text


def generate_shift_from_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return int(hashed_password, 16) % 26

def embed_data(image_path, data, output_path, password):
    shift = generate_shift_from_password(password)
    encrypted_data = caesar_cipher_encrypt(data, shift) + chr(0)  # Null character as a delimiter
    binary_data = ''.join(format(ord(char), '08b') for char in encrypted_data)
    
    # Open the image and ensure it is in a mode that supports pixel manipulation
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    data_index = 0

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if data_index < len(binary_data):
                r, g, b = pixels[i, j]
                r = (r & ~1) | int(binary_data[data_index])
                data_index += 1
                if data_index < len(binary_data):
                    g = (g & ~1) | int(binary_data[data_index])
                    data_index += 1
                if data_index < len(binary_data):
                    b = (b & ~1) | int(binary_data[data_index])
                    data_index += 1
                pixels[i, j] = (r, g, b)

    # Save the image in the same format (lossless if possible)
    img.save(output_path, format="PNG" if image_path.lower().endswith('.png') else "PNG")

# Extract Data Function with Support for PNG and JPG
def extract_data(image_path, password):
    shift = generate_shift_from_password(password)
    img = Image.open(image_path).convert("RGB")
    binary_data = ""
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    chars = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    message = ""
    for char in chars:
        if chr(int(char, 2)) == chr(0):  # Null character indicates end of message
            break
        message += chr(int(char, 2))

    return caesar_cipher_decrypt(message, shift)

@app.route('/embed', methods=['POST'])
def embed():
    try:
        image = request.files['image']
        data = request.form['data']
        password = request.form['password']

        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        temp_image_path = os.path.join(upload_folder, image.filename)
        image.save(temp_image_path)

        output_path = os.path.join("encoded", f"embedded_{image.filename}")
        os.makedirs("encoded", exist_ok=True)
        embed_data(temp_image_path, data, output_path, password)

        return jsonify({"message": "Data embedded successfully!", "output_path": output_path}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route('/extract', methods=['POST'])
def extract():
    try:
        # Check if required fields are provided
        if 'image' not in request.files or 'password' not in request.form:
            return jsonify({"message": "Missing required fields"}), 400

        # Retrieve uploaded image and password
        image = request.files['image']
        password = request.form['password']

        # Save uploaded image temporarily
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        temp_image_path = os.path.join(upload_folder, image.filename)
        image.save(temp_image_path)

        # Extract data from the image
        extracted_data = extract_data(temp_image_path, password)

        if extracted_data:  # Ensure data was successfully extracted
            return jsonify({
                "message": extracted_data,
                "data": extracted_data
            }), 200
        else:
            return jsonify({"message": "No valid data found or incorrect password!"}), 400

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True)