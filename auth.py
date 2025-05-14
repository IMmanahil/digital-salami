import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT UNIQUE,
                        password TEXT,
                        verification_code TEXT)''')
    conn.commit()
    conn.close()

# Generate a 6-digit verification code
def generate_verification_code():
    return str(random.randint(100000, 999999))

# Send verification email
def send_verification_email(user_email, verification_code):
    sender_email = os.getenv("SENDER_EMAIL")  # Change this
    sender_password = os.getenv("SENDER_PASSWORD")  # Use an app password (not real one)

    receiver_email = user_email
    subject = "Digital Salami - Email Verification Code"
    body = f"Your verification code is: {verification_code}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"Verification email sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Register user and send verification code
def register_user(first_name, last_name, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    verification_code = generate_verification_code()
    send_verification_email(email, verification_code)
    print(f"[DEBUG] Sent verification code: {verification_code}")

    try:
        hashed_password = generate_password_hash(password)
        cursor.execute('''INSERT INTO users (first_name, last_name, email, password, verification_code)
                          VALUES (?, ?, ?, ?, ?)''',
                       (first_name, last_name, email, hashed_password, verification_code))
        conn.commit()
    except sqlite3.IntegrityError:
        print("User already exists.")
        conn.close()
        return "user_exists"

    conn.close()
    return verification_code  # Let GUI handle user input of this code

# Verify code after user inputs it
def verify_code(email, input_code):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('SELECT verification_code FROM users WHERE email = ?', (email,))
        stored_code = cursor.fetchone()

        if stored_code:
            if stored_code[0] == input_code:
                cursor.execute('UPDATE users SET verification_code = ? WHERE email = ?', ('verified', email))
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                return False
        else:
            conn.close()
            return False
    except Exception as e:
        print(f"Error verifying code: {e}")
        return False

# Login user
def login_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, password, verification_code FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return "account_not_found"
    elif not check_password_hash(result[1], password):
        return "wrong_password"
    elif result[2] != "verified":
        return "not_verified"
    else:
        return ("success", result[0])  # Return success and user's first name

# Tkinter Registration Screen
def register_screen():
    def register():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        email = entry_email.get()
        password = entry_password.get()

        # Call the register_user function
        verification_code = register_user(first_name, last_name, email, password)
        if verification_code == "user_exists":
            messagebox.showerror("Error", "User already exists.")
        else:
            messagebox.showinfo("Info", "Registration successful! Please check your email for verification code.")

    register_window = tk.Toplevel()
    register_window.title("Register")

    tk.Label(register_window, text="First Name").pack()
    entry_first_name = tk.Entry(register_window)
    entry_first_name.pack()

    tk.Label(register_window, text="Last Name").pack()
    entry_last_name = tk.Entry(register_window)
    entry_last_name.pack()

    tk.Label(register_window, text="Email").pack()
    entry_email = tk.Entry(register_window)
    entry_email.pack()

    tk.Label(register_window, text="Password").pack()
    entry_password = tk.Entry(register_window, show="*")
    entry_password.pack()

    tk.Button(register_window, text="Register", command=register).pack()

# Tkinter Login Screen
def login_screen():
    def login():
        email = entry_email.get()
        password = entry_password.get()

        # Call the login_user function
        result = login_user(email, password)

        if result == "account_not_found":
            messagebox.showerror("Error", "Account not found.")
        elif result == "wrong_password":
            messagebox.showerror("Error", "Incorrect password.")
        elif result == "not_verified":
            messagebox.showerror("Error", "Account not verified. Please check your email.")
        else:
            messagebox.showinfo("Info", f"Login successful! Welcome {result[1]}.")

    login_window = tk.Toplevel()
    login_window.title("Login")

    tk.Label(login_window, text="Email").pack()
    entry_email = tk.Entry(login_window)
    entry_email.pack()

    tk.Label(login_window, text="Password").pack()
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack()

    tk.Button(login_window, text="Login", command=login).pack()

# Main Screen for the App
def main_screen():
    window = tk.Tk()
    window.title("Digital Salami")

    tk.Label(window, text="Welcome to Digital Salami!").pack()

    tk.Button(window, text="Register", command=register_screen).pack()
    tk.Button(window, text="Login", command=login_screen).pack()

    window.mainloop()

# Start the application
if __name__ == "__main__":
    init_db()
    main_screen()
