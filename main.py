import tkinter as tk
from PIL import Image, ImageTk
from PIL import ImageSequence

import os
import random
import sqlite3
import time
import requests


# -------- Database Setup -------- #
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    password TEXT
)
""")
conn.commit()


def recreate_salami_table():
    conn = sqlite3.connect("salami.db")
    c = conn.cursor()

    # Drop the existing table if it exists
    c.execute("DROP TABLE IF EXISTS salami_records")

    # Create a new table with the correct schema
    c.execute('''
        CREATE TABLE salami_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT,
            sender_email TEXT,
            receiver_name TEXT,
            receiver_email TEXT,
            personal_message TEXT,
            salami_amount TEXT,
            selected_envelope TEXT,
            envelope_path TEXT,
            payment_method TEXT,
            phone_number TEXT, 
            iban TEXT,
            cnic TEXT,
            transaction_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

    print("salami_records table recreated successfully.")

# Call the function to recreate the table
recreate_salami_table()


# -------- Setup Window -------- #
root = tk.Tk()
root.title("Welcome to Digital Salami")
root.configure(bg="#9630b0")
root.geometry("700x600")
# -------- Event Frame -------- #
envelope_frame = tk.Frame(root, bg="#9630b0")  
event_frame = tk.Frame(root, bg="#9630b0")
salami_frame = tk.Frame(root, bg="#9630b0") 
confirmation_frame = tk.Frame(root, bg="#9630b0")

selected_gateway = None  # Default
# -------- Load Welcome GIF -------- #
gif_path = os.path.join(os.getcwd(), "welcome.gif")
gif = Image.open(gif_path)

frames = []
try:
    while True:
        frame = gif.copy().resize((680, 400), Image.Resampling.LANCZOS)
        frames.append(ImageTk.PhotoImage(frame))
        gif.seek(len(frames))
except EOFError:
    pass

# -------- Welcome Frame -------- #
welcome_frame = tk.Frame(root, bg="#9630b0")
welcome_frame.pack()


gif_label = tk.Label(welcome_frame, bg="#9630b0")
gif_label.pack(pady=(20, 10))


def update_frame(index=0):
    gif_label.config(image=frames[index])
    root.after(100, update_frame, (index + 1) % len(frames))


update_frame()

def show_register_screen():
      login_frame.pack_forget()
      register_frame.pack(pady=50)

def show_login_screen():
    welcome_frame.pack_forget()
    login_frame.pack(pady=50)

    
 
start_button = tk.Button(
    welcome_frame,
    text="Start",
    font=("Helvetica", 16, "bold"),
    bg="#ff69b4",
    fg="white",
    padx=20, pady=10,
    command=show_login_screen
)
start_button.pack(pady=(10, 30))

# -------- Login Frame -------- #
login_frame = tk.Frame(root, bg="#9630b0")

email_label = tk.Label(login_frame, text="Email:", bg="#9630b0", fg="white", font=("Helvetica", 14))
email_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

email_entry = tk.Entry(login_frame, font=("Helvetica", 14), width=30)
email_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(login_frame, text="Password:", bg="#9630b0", fg="white", font=("Helvetica", 14))
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

password_entry = tk.Entry(login_frame, font=("Helvetica", 14), width=30, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

def validate_user_login():
    email = email_entry.get()
    password = password_entry.get()

    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()

    if user:
        print(f"Login successful for {email}")
        event_selection_screen()  # Move to event selection screen
    else:
        print(" Invalid credentials. Try again.")



login_button = tk.Button(
    login_frame, text="Login", font=("Helvetica", 12, "bold"),
    bg="#ff69b4", fg="white", width=12, command=validate_user_login  # Call the validation function
)


login_button.grid(row=2, column=0, pady=20)

register_button = tk.Button(
    login_frame, text="Register", font=("Helvetica", 12, "bold"),
    bg="#ff69b4", fg="white", width=12,
    command=show_register_screen
)

register_button.grid(row=2, column=1, pady=20)

register_frame = tk.Frame(root, bg="#9630b0")

# Email
reg_email_label = tk.Label(register_frame, text="Email:", bg="#9630b0", fg="white", font=("Helvetica", 14))
reg_email_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
reg_email_entry = tk.Entry(register_frame, font=("Helvetica", 14), width=30)
reg_email_entry.grid(row=0, column=1, padx=10, pady=5)

# First Name
first_name_label = tk.Label(register_frame, text="First Name:", bg="#9630b0", fg="white", font=("Helvetica", 14))
first_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
first_name_entry = tk.Entry(register_frame, font=("Helvetica", 14), width=30)
first_name_entry.grid(row=1, column=1, padx=10, pady=5)

# Last Name
last_name_label = tk.Label(register_frame, text="Last Name:", bg="#9630b0", fg="white", font=("Helvetica", 14))
last_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
last_name_entry = tk.Entry(register_frame, font=("Helvetica", 14), width=30)
last_name_entry.grid(row=2, column=1, padx=10, pady=5)

# Create Password
create_pass_label = tk.Label(register_frame, text="Create Password:", bg="#9630b0", fg="white", font=("Helvetica", 14))
create_pass_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
create_pass_entry = tk.Entry(register_frame, font=("Helvetica", 14), width=30, show="*")
create_pass_entry.grid(row=3, column=1, padx=10, pady=5)
# Verification Code Section
verification_code = str(random.randint(1000, 9999))  # Temporary code

verify_label = tk.Label(register_frame, text="Enter Verification Code:", bg="#9630b0", fg="white", font=("Helvetica", 14))
verify_entry = tk.Entry(register_frame, font=("Helvetica", 14), width=30)

def register_user():
    print("Verification code:", verification_code)  # Show in console
    verify_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    verify_entry.grid(row=4, column=1, padx=10, pady=5)
    verify_button.grid(row=5, column=1, pady=10)

def verify_user():
    entered_code = verify_entry.get()
    if entered_code == verification_code:
        email = reg_email_entry.get()
        first = first_name_entry.get()
        last = last_name_entry.get()
        password = create_pass_entry.get()

        try:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (email, first, last, password))
            conn.commit()
            print(" User verified and registered!")
        except sqlite3.IntegrityError:
            print(" Email already exists. Try logging in.")

        register_frame.pack_forget()
        login_frame.pack(pady=50)
    else:
        print(" Incorrect verification code. Try again.")
register_btn = tk.Button(register_frame, text="Register", font=("Helvetica", 12, "bold"),
                         bg="#ff69b4", fg="white", width=12, command=register_user)
register_btn.grid(row=6, column=0, pady=20)

verify_button = tk.Button(register_frame, text="Verify", font=("Helvetica", 12, "bold"),
                          bg="#ff69b4", fg="white", width=12, command=verify_user)
#  Note: This button is only shown when `register_user()` is called


# event selection 

import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os

# Store references to images to prevent garbage collection
event_images = []

def animate_gif(label, frames, index):
    try:
        label.config(image=frames[index])  # Set image for the current frame
        label.image = frames[index]  # Keep a reference to the image
        next_index = (index + 1) % len(frames)  # Loop the index for animation
        label.after(100, animate_gif, label, frames, next_index)  # Schedule next frame
    except tk.TclError:
        # Label was destroyed, ignore the error and stop the animation
        pass


def event_selection_screen():
    login_frame.pack_forget()  # Hide login frame
    event_frame.pack(pady=20, fill="both", expand=True)  # Show event frame

    for widget in event_frame.winfo_children():
        widget.destroy()

    # Add welcome label
    welcome_label = tk.Label(event_frame, text="Welcome! Choose your event.",
                             font=("Helvetica", 20, "bold"), bg="#9630b0", fg="white")
    welcome_label.pack(pady=10)

    # Create canvas and scrollbar
    canvas = tk.Canvas(event_frame, bg="#9630b0", highlightthickness=0)
    scroll_y = tk.Scrollbar(event_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # Create frame inside canvas
    event_container = tk.Frame(canvas, bg="#9630b0")
    canvas.create_window((0, 0), window=event_container, anchor="nw")

    # Event GIFs
    events = {
        "Mehandi": "mehandi.gif",
        "Baraat": "baraat.gif",
        "Walima": "walima.gif",
        "Engagement": "engagement.gif",
        "Anniversary": "anniversary.gif",
        "Bridal Shower": "bridal_shower.gif"
    }

    # Display in grid (2 columns)
    col_count = 2
    row = col = 0
    for event_name, gif_file in events.items():
        gif_path = os.path.join("C:\\Users\\i c\\Digital Salami MVP\\events", gif_file)
        if os.path.exists(gif_path):
            img = Image.open(gif_path)

            # Resize and store all frames for animation
            frames = [ImageTk.PhotoImage(frame.copy().resize((150, 150), Image.Resampling.LANCZOS))
                      for frame in ImageSequence.Iterator(img)]
            event_images.extend(frames)  # Prevent garbage collection

            # Create card frame
            card = tk.Frame(event_container, bg="#9630b0", highlightthickness=0, bd=0)
            gif_label = tk.Label(card, bg="#9630b0")
            gif_label.pack(pady=(0, 5))
            animate_gif(gif_label, frames, 0)

            tk.Button(card, text=event_name, font=("Helvetica", 14),
                      bg="#ff69b4", fg="white", width=20, height=2,
                      command=lambda e=event_name: select_event(e)).pack()

            card.grid(row=row, column=col, padx=20, pady=20)

            col += 1
            if col == col_count:
                col = 0
                row += 1
        else:
            print(f" {gif_file} not found at {gif_path}")

    # Update scrollregion after rendering
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    event_container.bind("<Configure>", configure_scroll_region)
#event selection
def select_event(event_name):
    print(f"Selected Event: {event_name}")
    envelope_selection_screen() 

def animate_gif(label, frames, index):
    frame = frames[index]
    label.configure(image=frame)
    label.image = frame  # Keep reference
    next_index = (index + 1) % len(frames)
    label.after(100, animate_gif, label, frames, next_index)
    
    # Proceed to envelope selection, etc.

import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import os

envelope_images = []  # Prevent garbage collection

def envelope_selection_screen():
    event_frame.pack_forget()
    envelope_frame.pack(pady=20, fill="both", expand=True)

    for widget in envelope_frame.winfo_children():
        widget.destroy()

    # Title
    tk.Label(envelope_frame, text="Select Your Envelope", font=("Helvetica", 20, "bold"),
             bg="#9630b0", fg="white").pack(pady=10)

    # Canvas + Scrollbar
    canvas = tk.Canvas(envelope_frame, bg="#9630b0", highlightthickness=0)
    scroll_y = tk.Scrollbar(envelope_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # Container Frame
    container = tk.Frame(canvas, bg="#9630b0")
    canvas.create_window((0, 0), window=container, anchor="nw")

    # Load envelopes
    col_count = 3
    row = col = 0
    for i in range(1, 10):
        filename = f"env{i}.png"
        path = os.path.join("C:\\Users\\i c\\Digital Salami MVP\\envelopes", filename)

        if os.path.exists(path):
            img = Image.open(path).resize((150, 150), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            envelope_images.append(img_tk)

            btn = tk.Button(container, image=img_tk, bg="#9630b0", bd=0,
                            command=lambda p=path: show_full_envelope(p))
            btn.grid(row=row, column=col, padx=20, pady=20)

            col += 1
            if col == col_count:
                col = 0
                row += 1
        else:
            print(f" {filename} not found at {path}")

    # Scroll config
    def update_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    container.bind("<Configure>", update_scroll)
def select_gateway_screen():
    # Show the screen for selecting a payment gateway
    print("Payment gateway selection screen")
    show_payment_method_selection(root)

def show_full_envelope(image_path):
    # Clear existing widgets on current frame (if any)
    for widget in envelope_frame.winfo_children():
        widget.destroy()

    try:
        # Load image and resize moderately
        img = Image.open(image_path)
        img = img.resize((200, 100), Image.Resampling.LANCZOS)  # Resize image to fit
        img_tk = ImageTk.PhotoImage(img)

        # Display image on current screen (in envelope_frame)
        label = tk.Label(envelope_frame, image=img_tk, bg="black")
        label.image = img_tk  # Keep reference
        label.pack(pady=20)

        # Envelope Selected message
        msg = tk.Label(envelope_frame, text=" Envelope Selected", font=("Helvetica", 10, "bold"),
                       fg="white", bg="black")
        msg.pack(pady=10)

        # Continue button (to go to the next screen)
        tk.Button(envelope_frame, text="Continue", font=("Helvetica", 16),
                  bg="#ff69b4", fg="white", padx=20, pady=20,
                  command=lambda: show_sender_receiver_details(root, image_path)).pack(pady=20)

    except Exception as e:
        print(f" Error loading image: {e}")

import tkinter as tk
from tkinter import messagebox

# Global dictionary to store transaction data
salami_data = {}

def show_sender_receiver_details(root, selected_envelope_path):
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Header
    tk.Label(root, text="🎁 Sender & Receiver Details", font=("Arial", 18, "bold")).pack(pady=20)

    # Entry field dictionary
    entries = {}

    # Input labels and keys
    fields = [
        ("Sender Name", "sender_name"),
        ("Sender Email", "sender_email"),
        ("Receiver Name", "receiver_name"),
        ("Receiver Email", "receiver_email"),
        ("Salami Amount", "salami_amount"),
        ("Personal Message (Optional)", "personal_message"),
    ]

    # Entry form
    for label_text, key in fields:
        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, anchor="w", width=25).pack(side="left")
        entry = tk.Entry(frame, width=40)
        entry.pack(side="left")
        entries[key] = entry

    # Validation & next screen trigger
    def continue_to_payment():
        for key in entries:
            salami_data[key] = entries[key].get().strip()

        # Basic validation
        required = ["sender_name", "sender_email", "receiver_name", "receiver_email"]
        for field in required:
            if not salami_data[field]:
                messagebox.showerror("Input Error", f"{field.replace('_', ' ').title()} is required.")
                return

        # Save selected envelope image path
        salami_data["selected_envelope"] = selected_envelope_path

        # Proceed to payment method screen
        show_payment_method_selection(root)

    # Button
    tk.Button(
        root,
        text="Continue to Payment",
        bg="#ff69b4",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=10,
        pady=5,
        command=continue_to_payment
    ).pack(pady=30)

def show_payment_method_selection(root):
    # Clear screen
    for widget in root.winfo_children():
        widget.destroy()

    # Heading
    tk.Label(root, text="💰 Select Payment Method", font=("Arial", 18, "bold")).pack(pady=20)

    # Instruction
    tk.Label(root, text="Please choose a payment method:", font=("Arial", 12)).pack(pady=10)

    # Button styles
    button_style = {
        "width": 30,
        "height": 2,
        "font": ("Arial", 12, "bold"),
        "bg": "#ff69b4",
        "fg": "white",
        "padx": 10,
        "pady": 5,
    }

    def select_jazzcash():
        salami_data["payment_method"] = "JazzCash / EasyPaisa"
        show_jazzcash_payment_screen(root)

    def select_stripe():
        salami_data["payment_method"] = "Card (Stripe)"
        show_stripe_payment_screen(root)

    # Buttons
    tk.Button(root, text="🎉 JazzCash / EasyPaisa", command=select_jazzcash, **button_style).pack(pady=15)
    tk.Button(root, text="💳 Card (Stripe)", command=select_stripe, **button_style).pack(pady=15)
def show_jazzcash_payment_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="📱 JazzCash / EasyPaisa Details", font=("Arial", 18, "bold")).pack(pady=20)

    entries = {}
    fields = [
        ("Phone Number (required)", "phone_number"),
        ("IBAN Number (optional)", "iban"),
        ("CNIC (optional)", "cnic"),
        ("MPIN (4-DIGIT)", "mpin"),
    ]

    for label, key in fields:
        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Label(frame, text=label, anchor="w", width=25).pack(side="left")
        entry = tk.Entry(frame, width=40)
        entry.pack(side="left")
        entries[key] = entry

    def continue_to_confirmation():
        # Ensure global dict
        global salami_data
        if 'salami_data' not in globals():
            salami_data = {}

        # Fetch input values
        salami_data["phone_number"] = entries["phone_number"].get().strip()
        salami_data["iban"] = entries["iban"].get().strip()
        salami_data["cnic"] = entries["cnic"].get().strip()
        salami_data["mpin"] = entries["mpin"].get().strip()

        # Basic validation
        if not salami_data["phone_number"]:
            messagebox.showerror("Input Error", "Phone Number is required.")
            return
        if not salami_data["mpin"]:
            messagebox.showerror("Input Error", "MPIN is required.")
            return

        # Continue
        show_confirmation_screen(root)

    # Add continue button
    tk.Button(
        root,
        text="Continue to Confirmation",
        bg="#ff69b4",
        fg="white",
        font=("Arial", 12, "bold"),
        command=continue_to_confirmation
    ).pack(pady=30)


def show_stripe_payment_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="💳 Card Payment (Stripe)", font=("Arial", 18, "bold")).pack(pady=20)

    entries = {}
    fields = [
        ("Card Number", "card_number"),
        ("Expiry Date (MM/YY)", "expiry_date"),
        ("CVV", "cvv"),
        ("Cardholder Name", "cardholder_name"),
        ("Card Type (Debit/Credit/Visa)", "card_type"),
        ("Email", "card_email"),
    ]

    for label, key in fields:
        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Label(frame, text=label, anchor="w", width=30).pack(side="left")
        entry = tk.Entry(frame, width=35)
        entry.pack(side="left")
        entries[key] = entry

    import tkinter as tk

def show_stripe_payment_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="💳 Card Payment (Stripe)", font=("Arial", 18, "bold")).pack(pady=20)

    entries = {}
    fields = [
        ("Card Number", "card_number"),
        ("Expiry Date (MM/YY)", "expiry_date"),
        ("CVV", "cvv"),
        ("Cardholder Name", "cardholder_name"),
        ("Card Type", "card_type"),
        ("Email", "card_email"),
    ]

    card_type_options = ["Debit", "Credit", "Visa"]  # Options for Card Type

    for label, key in fields:
        frame = tk.Frame(root)
        frame.pack(pady=5)

        tk.Label(frame, text=label, anchor="w", width=30).pack(side="left")

        if key == "card_type":
            # Create a dropdown for the Card Type field
            var = tk.StringVar(root)
            var.set(card_type_options[0])  # Set default option to Debit
            card_type_menu = tk.OptionMenu(frame, var, *card_type_options)
            card_type_menu.pack(side="left")
            entries[key] = var  # Store the selected value
        else:
            # Create regular entry fields for the other fields
            entry = tk.Entry(frame, width=35)
            entry.pack(side="left")
            entries[key] = entry

    def continue_to_confirmation():
        # Gather all the input values
        salami_data = {}
        for key in entries:
            if isinstance(entries[key], tk.StringVar):  # For dropdown menu
                salami_data[key] = entries[key].get().strip()
            else:  # For regular text entry fields
                salami_data[key] = entries[key].get().strip()

        # Check if any required field is empty
        required = ["card_number", "expiry_date", "cvv", "cardholder_name", "card_type", "card_email"]
        for field in required:
            if not salami_data[field]:
                tk.messagebox.showerror("Input Error", f"{field.replace('_', ' ').title()} is required.")
                return

        # If everything is valid, proceed to confirmation screen (this function should be implemented)
        show_confirmation_screen(root)

    tk.Button(
        root,
        text="Continue to Confirmation",
        bg="#ff69b4",
        fg="white",
        font=("Arial", 12, "bold"),
        command=continue_to_confirmation
    ).pack(pady=30)

# Make sure to define salami_data and show_confirmation_screen() appropriately in your code.

from datetime import datetime
import random
from PIL import Image, ImageTk

def show_confirmation_screen(root):
    # First clear all widgets from root (except the confirmation frame)
    for widget in root.winfo_children():
        if widget != getattr(root, "confirmation_frame", None):  # Skip confirmation_frame
            widget.destroy()

    # Create confirmation frame if not already created
    if not hasattr(root, "confirmation_frame"):
        confirmation_frame = tk.Frame(root, bg="#9630b0")
        confirmation_frame.pack(fill="both", expand=True)
        root.confirmation_frame = confirmation_frame  # Store reference globally

    # Clear previous widgets if any
    for widget in confirmation_frame.winfo_children():
        widget.destroy()

    tk.Label(
        confirmation_frame,
        text="🧾 Confirm Your Salami Details",
        font=("Arial", 18, "bold"),
        bg="#9630b0",
        fg="white"
    ).pack(pady=20)

    # Generate transaction data
    salami_data["transaction_id"] = f"TXN{random.randint(100000, 999999)}"
    salami_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salami_data["salami_amount"]   # Optional to make dynamic

    summary = f"""
    Sender: {salami_data.get('sender_name', '')}
    Receiver: {salami_data.get('receiver_name', '')}
    Amount: {salami_data['salami_amount']}
    Payment Method: {salami_data.get('payment_method', '')}
    Transaction ID: {salami_data['transaction_id']}
    Date & Time: {salami_data['timestamp']}
    """

    tk.Label(
        confirmation_frame,
        text=summary,
        font=("Arial", 12),
        justify="left",
        bg="#9630b0",
        fg="white"
    ).pack(pady=10)

    # Envelope preview
    if "selected_envelope" in salami_data:
        try:
            img = Image.open(salami_data["selected_envelope"])
            img = img.resize((150, 100))
            img = ImageTk.PhotoImage(img)
            tk.Label(confirmation_frame, image=img, bg="#9630b0").pack()
            confirmation_frame.envelope_preview_img = img  # Keep reference to prevent garbage collection
        except Exception as e:
            tk.Label(confirmation_frame, text=f"(Envelope preview failed: {e})", bg="#9630b0", fg="white").pack()

    def confirm_and_send():
        save_to_database()
        show_receipt_screen(root)

    def go_back():
        show_payment_method_selection(root)

    tk.Button(
        confirmation_frame,
        text="Confirm & Send",
        bg="#32cd32",
        fg="white",
        font=("Arial", 12, "bold"),
        command=confirm_and_send
    ).pack(pady=15)

    tk.Button(
        confirmation_frame,
        text="Back",
        bg="gray",
        fg="white",
        font=("Arial", 11),
        command=go_back
    ).pack(pady=10)


import sqlite3

def save_to_database():
    conn = sqlite3.connect("salami.db")
    c = conn.cursor()

    # Create table if not exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS salami_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT,
            sender_email TEXT,
            receiver_name TEXT,
            receiver_email TEXT,
            personal_message TEXT,
            selected_envelope TEXT,
            envelope_path TEXT,
            payment_method TEXT,
            phone_number TEXT,
            iban TEXT,
            cnic TEXT,
            salami_amount TEXT,
            transaction_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert data
    c.execute("""
        INSERT INTO salami_records (
            sender_name, sender_email, receiver_name, receiver_email, personal_message,
            envelope_path, payment_method, phone_number, iban, cnic,selected_envelope,
            salami_amount, transaction_id 
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        salami_data.get("sender_name"),
        salami_data.get("sender_email"),
        salami_data.get("receiver_name"),
        salami_data.get("receiver_email"),
        salami_data.get("personal_message"),
        salami_data.get("selected_envelope"),
        salami_data.get("envelope_path"),
        salami_data.get("payment_method"),
        salami_data.get("phone_number"),
        salami_data.get("iban"),
        salami_data.get("cnic"),
        salami_data.get("salami_amount"),
        salami_data.get("transaction_id"),
        
    ))

    conn.commit()
    conn.close()
from reportlab.pdfgen import canvas
from tkinter import filedialog

def show_receipt_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="📃 Your Salami Receipt", font=("Arial", 18, "bold")).pack(pady=20)

    receipt_text = f"""
Transaction ID: {salami_data['transaction_id']}
Sender: {salami_data['sender_name']} ({salami_data['sender_email']})
Receiver: {salami_data['receiver_name']} ({salami_data['receiver_email']})
Amount: {salami_data['salami_amount']}
Payment Method: {salami_data['payment_method']}
Date & Time: {salami_data['timestamp']}
"""

    tk.Label(root, text=receipt_text, font=("Arial", 12), justify="left").pack(pady=10)

    # Envelope preview
    if "selected_envelope" in salami_data:
        try:
            img = Image.open(salami_data["selected_envelope"])
            img = img.resize((150, 100))
            img = ImageTk.PhotoImage(img)
            tk.Label(root, image=img).pack()
            root.receipt_img = img
        except:
            tk.Label(root, text="(Envelope preview failed)").pack()

    # Success message
    tk.Label(root, text="✅ Your salami has been sent!", font=("Arial", 12, "bold"), fg="green").pack(pady=20)

    # --- PDF Download ---
    def download_pdf():
        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not filepath:
            return

        c = canvas.Canvas(filepath)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 800, "Digital Salami Receipt")
        c.setFont("Helvetica", 12)
        c.drawString(100, 770, f"Transaction ID: {salami_data['transaction_id']}")
        c.drawString(100, 750, f"Sender: {salami_data['sender_name']} ({salami_data['sender_email']})")
        c.drawString(100, 730, f"Receiver: {salami_data['receiver_name']} ({salami_data['receiver_email']})")
        c.drawString(100, 710, f"Amount: {salami_data['salami_amount']}")
        c.drawString(100, 690, f"Payment Method: {salami_data['payment_method']}")
        c.drawString(100, 670, f"Date & Time: {salami_data['timestamp']}")
        c.drawString(100, 650, f"Message: {salami_data.get('personal_message', '')}")
        c.save()
        messagebox.showinfo("Saved", "PDF receipt has been saved successfully.")

    # --- Email Placeholder ---
    def send_email_placeholder():
        messagebox.showinfo("Email Sent", f"Mock email sent to {salami_data['receiver_email']} 🎉")

    # Buttons
    btn_frame = tk.Frame(root, bg="#9630b0")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="📥 Download PDF Receipt", command=download_pdf, bg="#4682B4", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=10)
    tk.Button(btn_frame, text="📩 Send to Email", command=send_email_placeholder, bg="#32cd32", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=10)
root.mainloop()
