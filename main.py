import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import re
import sqlite3
import random
import string
class AnimatedGIFLabel(tk.Label):
    def __init__(self, master, path, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frames = []
        self.delay = 100

        try:
            gif = Image.open(path)
            while True:
                frame = ImageTk.PhotoImage(gif.copy().resize((150, 150)))
                self.frames.append(frame)
                try:
                    gif.seek(len(self.frames))
                except EOFError:
                    break
            self.delay = gif.info.get('duration', 100)
            self.current = 0
            self.after(self.delay, self.play)
        except Exception as e:
            print(f"❌ Couldn't load animation {path}: {e}")
            self.config(text="GIF Error", fg="white", bg="#9630b0")

    def play(self):
        if self.frames:
            self.config(image=self.frames[self.current])
            self.current = (self.current + 1) % len(self.frames)
            self.after(self.delay, self.play)


# -------- Helper Functions -------- #
def generate_verification_code():
    """Generate a random 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))


def register_user(first, last, email, password):
    """Handle the registration process for new users."""
    conn = sqlite3.connect('users.db')  # Connect to the SQLite database
    cursor = conn.cursor()

    # Check if the email is already registered
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return "email_exists"

    # Generate a verification code and insert the user into the database
    verification_code = generate_verification_code()
    cursor.execute("INSERT INTO users (first_name, last_name, email, password, verified, verification_code) VALUES (?, ?, ?, ?, ?, ?)",
                   (first, last, email, password, 0, verification_code))
    conn.commit()
    conn.close()

    # Print the verification code in console for MVP
    print(f"🔐 Verification code for {email}: {verification_code}")
    return verification_code  # ✅ This line must be indented inside the function




def verify_code(email, input_code):
    """Verify the entered code against the database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT verification_code FROM users WHERE email = ?", (email,))
    db_code = cursor.fetchone()
    conn.close()

    if db_code and db_code[0] == input_code:
        # Update verification status
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET verified = 1 WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        return True
    return False


def login_user(email, password):
    """Handle the login process."""
    conn = sqlite3.connect('users.db')  # Replace with your actual database path
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user is None:
        return "account_not_found"

    stored_password = user[4]  # Assuming password is stored in the 4th column
    if stored_password != password:
        return "wrong_password"

    if not user[4]:  # Verification check
        return "not_verified"

    return user


# -------- Initialize the main window -------- #
root = tk.Tk()
root.title("Welcome to Digital Salami")
root.geometry("500x600")
root.configure(bg="#9630b0")


# -------- FRAME FOR GIF -------- #
gif_frame = tk.Frame(root, bg="#9630b0")
gif_frame.pack(side="top", fill="both", expand=False)

gif_path = os.path.join(os.getcwd(), "welcome.gif")
gif_image = Image.open(gif_path)

frames = []
try:
    while True:
        resized = gif_image.resize((700, 400))
        frame = ImageTk.PhotoImage(resized.copy())
        frames.append(frame)
        gif_image.seek(gif_image.tell() + 1)
except EOFError:
    pass

gif_label = tk.Label(gif_frame, bg="#9630b0")
gif_label.pack()


def update_gif_frame(frame_index=0):
    gif_label.config(image=frames[frame_index])
    root.after(100, update_gif_frame, (frame_index + 1) % len(frames))


update_gif_frame()


# -------- FRAME FOR BUTTON -------- #
button_frame = tk.Frame(root, bg="#9630b0")
button_frame.pack(pady=20)


def start_button_action():
    gif_frame.pack_forget()
    button_frame.pack_forget()
    show_login_register_screen()


start_button = tk.Button(
    button_frame,
    text="Start",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#FF4081",
    padx=30,
    pady=20,
    command=start_button_action
)
start_button.pack(anchor='w', padx=150)


# -------- Login/Registration Screen -------- #
login_register_frame = tk.Frame(root, bg="#9630b0")


def show_login_register_screen():
    login_register_frame.pack(fill="both", expand=True)
    show_login_form()


toggle_frame = tk.Frame(login_register_frame, bg="#9630b0")
toggle_frame.pack(pady=10)


def show_login_form():
    clear_form()
    login_title = tk.Label(form_frame, text="Login", font=("Arial", 18, "bold"), bg="#9630b0", fg="white")
    login_title.pack(pady=10)

    tk.Label(form_frame, text="Email", bg="#9630b0", fg="white").pack()
    email_entry = tk.Entry(form_frame)
    email_entry.pack(pady=5)

    tk.Label(form_frame, text="Password", bg="#9630b0", fg="white").pack()
    password_entry = tk.Entry(form_frame, show="*")
    password_entry.pack(pady=5)

    def handle_login():
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        result = login_user(email, password)

        if result == "account_not_found":
            messagebox.showerror("Error", "Account not found. Please register.")
        elif result == "wrong_password":
            messagebox.showerror("Error", "Wrong password.")
        elif result == "not_verified":
            messagebox.showerror("Error", "Email not verified. Please check your email for the verification code.")
        else:
            messagebox.showinfo("Welcome", f"Hello {result[1]}! Login successful.")
            login_register_frame.pack_forget()
            show_event_selection_screen(result[1])  # Pass user first name or user ID


    tk.Button(
        form_frame,
        text="Login",
        bg="#FF4081",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=5,
        command=handle_login
    ).pack(pady=10)


def show_register_form():
    clear_form()
    register_title = tk.Label(form_frame, text="Register", font=("Arial", 18, "bold"), bg="#9630b0", fg="white")
    register_title.pack(pady=10)

    tk.Label(form_frame, text="First Name", bg="#9630b0", fg="white").pack()
    fname_entry = tk.Entry(form_frame)
    fname_entry.pack(pady=5)

    tk.Label(form_frame, text="Last Name", bg="#9630b0", fg="white").pack()
    lname_entry = tk.Entry(form_frame)
    lname_entry.pack(pady=5)

    tk.Label(form_frame, text="Email", bg="#9630b0", fg="white").pack()
    email_entry = tk.Entry(form_frame)
    email_entry.pack(pady=5)

    tk.Label(form_frame, text="Password", bg="#9630b0", fg="white").pack()
    password_entry = tk.Entry(form_frame, show="*")
    password_entry.pack(pady=5)

    def handle_register():
        first = fname_entry.get()
        last = lname_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if not first or not last or not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Invalid Email", "Enter a valid email address.")
            return
        if len(password) < 6:
            messagebox.showerror("Weak Password", "Password must be at least 6 characters.")
            return

        sent_code = register_user(first, last, email, password)

        if sent_code == "email_exists":
            messagebox.showerror("Error", "This email is already registered.")
            return

        show_verification_form(email, sent_code)


    tk.Button(
        form_frame,
        text="Register",
        bg="#FF4081",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=5,
        command=handle_register
    ).pack(pady=10)


def show_verification_form(email, sent_code):
    clear_form()
    tk.Label(form_frame, text="Email Verification", font=("Arial", 18, "bold"), bg="#9630b0", fg="white").pack(pady=10)

    tk.Label(form_frame, text="Enter the 6-digit code sent to your email", bg="#9630b0", fg="white").pack()
    code_entry = tk.Entry(form_frame)
    code_entry.pack(pady=5)

    def verify():
        input_code = code_entry.get()
        if verify_code(email, input_code):
            messagebox.showinfo("Success", "Your email has been verified! You can now log in.")
            show_login_form()
        else:
            messagebox.showerror("Error", "Invalid verification code. Please try again.")

    tk.Button(
        form_frame,
        text="Verify",
        bg="#FF4081",
        fg="white",
        font=("Arial", 12, "bold"),
        command=verify
    ).pack(pady=10)


# Buttons to switch between login and register
login_btn = tk.Button(toggle_frame, text="Login", command=show_login_form, bg="#FF4081", fg="white", padx=20, pady=5)
register_btn = tk.Button(toggle_frame, text="Register", command=show_register_form, bg="#FF4081", fg="white", padx=20, pady=5)

login_btn.grid(row=0, column=0, padx=10)
register_btn.grid(row=0, column=1, padx=10)


# Form Frame
form_frame = tk.Frame(login_register_frame, bg="#9630b0")
form_frame.pack(pady=10)


def clear_form():
    for widget in form_frame.winfo_children():
        widget.destroy()


import tkinter as tk
from tkinter import messagebox
import os

# Assuming AnimatedGIFLabel is defined somewhere else in your code
# from your_gif_module import AnimatedGIFLabel

import tkinter as tk
from tkinter import messagebox
import os

# Assuming AnimatedGIFLabel is defined somewhere else in your code
# from your_gif_module import AnimatedGIFLabel

def show_event_selection_screen(user_name):
    clear_form()  # Optional: Clear previous form if needed

    event_frame = tk.Frame(root, bg="#9630b0")
    event_frame.pack(fill="both", expand=True)

    # Use grid for the frame to help with centering
    event_frame.grid_rowconfigure(0, weight=0)  # Row for the label
    event_frame.grid_rowconfigure(1, weight=1)  # Row for the grid of events
    event_frame.grid_columnconfigure(0, weight=1)  # Center the column

    # Welcome label
    tk.Label(event_frame, text=f"Welcome, {user_name}!\nChoose your event:",
             font=("Arial", 20, "bold"), bg="#9630b0", fg="white").grid(row=0, column=0, pady=20)

    # Scrollable canvas
    canvas = tk.Canvas(event_frame, bg="#9630b0", highlightthickness=0)
    scrollbar = tk.Scrollbar(event_frame, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=scrollbar.set)

    scroll_frame = tk.Frame(canvas, bg="#9630b0")
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.grid(row=1, column=0, sticky="nsew")  # Make canvas fill the space
    scrollbar.grid(row=2, column=0, sticky="ew")  # Place the scrollbar below the canvas

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scroll_frame.bind("<Configure>", on_configure)

    events = [
        ("Mehandi", "mehandi.gif"),
        ("Barat", "baraat.gif"),
        ("Walima", "Walimaa.gif"),
        ("Engagement", "engagement.gif"),
        ("Bridal Shower", "bridal_shower.gif"),
        ("Anniversary", "anniversary.gif")
    ]

    for idx, (event_name, gif_file) in enumerate(events):
        col = idx % 3
        row = idx // 3

        box = tk.Frame(scroll_frame, bg="#9630b0", padx=10, pady=10)
        box.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

        gif_path = os.path.join("C:/Users/i c/Digital Salami MVP", gif_file)

        if os.path.exists(gif_path):
            gif_label = AnimatedGIFLabel(box, gif_path, bg="#9630b0")
            gif_label.pack()
        else:
            print(f"❌ File not found: {gif_path}")
            tk.Label(box, text="GIF Not Found", bg="#9630b0", fg="white").pack()

        tk.Button(
            box,
            text=event_name,
            bg="#FF4081",
            fg="white",
            font=("Arial", 12, "bold"),
            command=lambda name=event_name: messagebox.showinfo("Event Selected", f"You chose: {name}")
        ).pack(pady=5)

root.mainloop()

