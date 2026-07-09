# Break-the-login

## Overview

**Break-the-login** is an academic project developed for the _Secure Software Application Development_ course at the Faculty of Mathematics and Computer Science, University of Bucharest.

The goal of the project is to demonstrate how authentication systems are attacked in practice and how they can be secured against real-world threats.

The project contains two versions of the same application:

- **v1 (Vulnerable)** – intentionally insecure implementation used to demonstrate common authentication vulnerabilities.
- **v2 (Secured)** – improved implementation where the identified vulnerabilities are mitigated using secure development practices.

## Implemented Features

- User registration
- User authentication (login/logout)
- Session management using cookies
- Password reset functionality
- Role-based user model

## Demonstrated Vulnerabilities

The vulnerable version includes examples of:

- Weak password policies
- Plain-text password storage
- Brute-force attacks due to missing rate limiting
- User enumeration
- Insecure session management
- Predictable and reusable password reset tokens

The secured version addresses these issues using:

- Password hashing
- Rate limiting
- Generic authentication error messages
- Secure cookie attributes
- Cryptographically secure session identifiers
- One-time password reset tokens

## Technologies Used

- Python
- Flask
- SQLite

## Running the Project

Clone the repository:

```bash
git clone https://github.com/<username>/Break-the-login.git
cd Break-the-login
```

Install the dependencies:

```bash
pip install flask werkzeug
```

Initialize the database:

```bash
sqlite3 authx.db < schema.sql
```

Start the application:

```bash
python app.py
```

The application will be available at:

```text
http://localhost:5000
```

## Educational Purpose

This project was developed strictly for educational purposes in a controlled laboratory environment to study authentication vulnerabilities and secure software development practices.
