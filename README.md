
---
## 🎬 Welcome Animation

![Welcome Screen](welcome.gif)

# Digital Salami MVP (Minimum Viable Product)

## Overview

**Digital Salami** is an innovative desktop application built with Python's **Tkinter** library, providing a unique way to send personalized digital salami (envelopes) for various events. The MVP of this project focuses on user registration, login authentication, dynamic event selection, customizable envelope preview, and integrated payment systems (via **Stripe** and mock gateways).

The project integrates a **Flask backend** with **JWT authentication**, secure user login, and seamless payment integration for a complete end-to-end user experience.

---

## Features

### 1. **User Authentication**

* **Secure Registration**: Users can create accounts by providing a username and password.
* **JWT-Based Login**: After registration, users can securely log in to the app, generating a JWT token to access protected features.
* **Password Hashing**: Passwords are hashed and stored securely to ensure user data safety.

### 2. **Event and Envelope Selection**

* **Event-Based Salami**: Choose from a variety of pre-defined events such as **Mehandi**, **Baraat**, **Walima**, **Bridal Shower**, and **Anniversary**.
* **Envelope Customization**: Browse through a collection of digital envelope GIFs, select a preferred design, and preview it in full-screen mode.

### 3. **Personalized Sender/Receiver Details**

* Users can provide both sender and receiver information, making each salami unique and personalized.
* The details are stored temporarily for the transaction process and are used to customize the envelope further.

### 4. **Payment Integration**

* **Stripe Integration**: The system is integrated with **Stripe** to facilitate real payment processing. Test payments are simulated using Stripe's **test cards**.
* **Mock Payment Gateways**: For demo purposes, mock payment gateways are available for testing, giving the app a polished feel even without real transactions.
* **Payment Confirmation**: After the transaction, users receive a payment receipt, with the option to download it or receive an email confirmation.

### 5. **User Interface**

* A clean, intuitive, and modern user interface developed with **Tkinter** ensures a seamless experience for users.
* Simple navigation flow from the **Start Screen** to **Login**, **Event Selection**, **Envelope Selection**, and **Payment Method Selection**.

---

## Requirements

### Backend (Flask)

* Python 3.x
* Flask
* Flask-JWT-Extended
* Stripe
* Werkzeug (for password hashing)
* dotenv (to manage environment variables)

### Frontend (Tkinter)

* Tkinter (for GUI)
* Requests (for backend API calls)

---

## Project Setup

### Step 1: Clone the Repository

Clone the project repository to your local system.

```bash
git clone <repository_url>
cd <project_directory>
```

### Step 2: Install Backend Dependencies

Inside the **backend** directory, install the required dependencies.

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

1. Create a `.env` file in the **root directory** and add the following:

   ```bash
   JWT_SECRET_KEY=your_jwt_secret_key
   STRIPE_API_KEY=your_stripe_api_key
   ```

2. Replace `your_jwt_secret_key` with a secure key you generate for JWT authentication.

3. Replace `your_stripe_api_key` with your **Stripe test/live secret key** (you can generate this from your Stripe Dashboard).

---

## Running the Application

### Backend (Flask)

To run the backend server, navigate to the **backend** folder and execute the following command:

```bash
cd backend
python app.py
```

The backend API will be hosted at `http://127.0.0.1:5000` by default.

### Frontend (Tkinter)

To run the Tkinter GUI, navigate to the **frontend** folder and execute:

```bash
cd frontend
python main.py
```

The **Tkinter GUI** will open, and you can start interacting with the Digital Salami application.

---

## API Endpoints

### 1. **/register** \[POST]

**Description**: Register a new user account.

**Request Body**:

```json
{
  "username": "new_user",
  "password": "secure_password"
}
```

**Response**:

```json
{
  "message": "User registered successfully!"
}
```

---

### 2. **/login** \[POST]

**Description**: Log in and receive a JWT token for authentication.

**Request Body**:

```json
{
  "username": "existing_user",
  "password": "user_password"
}
```

**Response**:

```json
{
  "access_token": "jwt_token_here"
}
```

---

### 3. **/protected** \[GET]

**Description**: Access a protected route (requires JWT authentication).

**Request Header**:

```bash
Authorization: Bearer jwt_token_here
```

**Response**:

```json
{
  "message": "This is a protected route!"
}
```

---

### 4. **/charge\_card** \[POST]

**Description**: Process a payment using Stripe (test cards only).

**Request Body**:

```json
{
  "amount": 1000,
  "card": {
    "number": "4242424242424242",
    "exp_month": 12,
    "exp_year": 2025,
    "cvc": "123"
  }
}
```

**Response**:

```json
{
  "message": "Payment successful!",
  "charge_id": "charge_id_here"
}
```

---

### 5. **/create-payment-intent** \[POST]

**Description**: Create a payment intent with Stripe (requires JWT).

**Request Body**:

```json
{
  "amount": 5000,
  "currency": "usd"
}
```

**Response**:

```json
{
  "clientSecret": "stripe_client_secret_here"
}
```

---

## Frontend User Flow

### 1. **Start Screen**

* The app begins with a welcoming screen displaying an animated GIF that transitions into the login or registration page.

### 2. **Login/Registration**

* Users can log in with an existing account or register a new one. Registration requires a username and password. After successful login, users will receive a JWT token.

### 3. **Event Selection**

* Users choose an event from predefined options such as **Mehandi**, **Baraat**, **Walima**, **Bridal Shower**, or **Anniversary**.

### 4. **Envelope Customization**

* Users browse through available envelopes (GIFs), preview their chosen envelope in full-screen mode, and confirm their selection.

### 5. **Sender/Receiver Details**

* Users provide details for the sender and receiver. These details personalize the envelope, making the transaction unique.

### 6. **Payment**

* Users can choose to make a payment using real or mock payment gateways. Stripe's integration ensures secure transactions, and users receive a receipt after successful payment.

---

## Future Features

### 1. **Additional Payment Gateways**

* Integrate **EasyPaisa**, **JazzCash**, and **PayPal** to provide more local and international payment options.

### 2. **Email Notifications**

* **Email receipts** for transactions, enhancing the user experience and providing proof of payment.

### 3. **Mobile Application**

* Transition to a **mobile app** for Android/iOS to expand the reach and accessibility of the platform.

### 4. **Admin Panel**

* **Admin dashboard** to manage user accounts, view transaction logs, and monitor payment statuses.

---


---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details 