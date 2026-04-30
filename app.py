import sqlite3
import uuid
from flask import Flask, request, jsonify, make_response, render_template_string, redirect, url_for

app = Flask(__name__)

sessions = {}
reset_tokens = {}

def get_db_connection():
    conn = sqlite3.connect('authx.db')
    conn.row_factory = sqlite3.Row
    return conn


BASE_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>AuthX - System v1 (Vulnerable)</title>
    <style>
        body { font-family: sans-serif; margin: 40px; line-height: 1.6; }
        nav { margin-bottom: 20px; background: #eee; padding: 10px; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <nav>
        <strong>AuthX</strong> | 
        <a href="/">Home</a> | <a href="/register">Register</a> | 
        <a href="/login">Login</a> | <a href="/forgot-password">Forgot Password</a>
    </nav>
    {% block content %}{% endblock %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(BASE_LAYOUT + "<p>Acces restrictionat angajatilor.</p>")

@app.route('/register', methods=['GET'])
def register_page():
    return render_template_string(BASE_LAYOUT + """
    <h2>Creare Cont Nou</h2>
    <form method="POST" action="/api/register">
        Email: <input type="email" name="email" required><br><br>
        Parola: <input type="password" name="password" required><br><br>
        <button type="submit">inregistrare</button>
    </form>
    """)

@app.route('/login', methods=['GET'])
def login_page():
    return render_template_string(BASE_LAYOUT + """
    <h2>Autentificare</h2>
    <form method="POST" action="/api/login">
        Email: <input type="email" name="email" required><br><br>
        Parola: <input type="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
    """)

@app.route('/dashboard')
def dashboard():
    session_id = request.cookies.get('session_id')
    if session_id in sessions:
        user_id = sessions[session_id]
        return render_template_string(BASE_LAYOUT + f"""
            <h1>Dashboard Utilizator</h1>
            <p>Sunteti autentificat cu succes! ID Utilizator: {user_id}</p>
            <p>Acesta este un sistem vulnerabil</p>
            <a href='/logout'>Deconectare</a>
        """)
    return redirect(url_for('login_page'))

@app.route('/forgot-password', methods=['GET'])
def forgot_page():
    return render_template_string(BASE_LAYOUT + """
    <h2>Recuperare Parola</h2>
    <p>Introduceti email-ul pentru a genera un token de resetare.</p>
    <form method="POST" action="/api/forgot-password">
        Email: <input type="email" name="email" required><br><br>
        <button type="submit">Obtine Token</button>
    </form>
    """)

@app.route('/reset-password', methods=['GET'])
def reset_password_page():
    return render_template_string(BASE_LAYOUT + """
    <h2>Setare Parola Noua</h2>
    <form method="POST" action="/api/reset-password">
        Token: <input type="text" name="token" required><br><br>
        Noua Parola: <input type="password" name="password" required><br><br>
        <button type="submit">Actualizeaza Parola</button>
    </form>
    """)


@app.route('/api/register', methods=['POST'])
def register():
    email = request.form.get('email') or request.json.get('email')
    password = request.form.get('password') or request.json.get('password')

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, password))
        conn.commit()
        return "Cont creat! <a href='/login'>Login aici</a>"
    except sqlite3.IntegrityError:
        return "Eroare: Email deja existent.", 400
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    email = request.form.get('email') or request.json.get('email')
    password = request.form.get('password') or request.json.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if not user:
        return "EROARE: Utilizatorul nu a fost gasit in baza de date", 404
    
    if user['password_hash'] == password:
        session_id = str(uuid.uuid4())
        sessions[session_id] = user['id']
        
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('session_id', session_id)
        return resp
    else:
        return "EROARE: Parola introdusa este incorecta", 401

@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id in sessions:
        del sessions[session_id]
    resp = make_response(redirect(url_for('login_page')))
    resp.set_cookie('session_id', '', expires=0)
    return resp

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form.get('email') or request.json.get('email')
    token = f"reset-token-{email}"
    reset_tokens[token] = email
    return f"Token generat: <strong>{token}</strong> (in mod normal trimis pe mail)<br>Accesati <a href='/reset-password'>pagina de resetare</a> pentru a finaliza."

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    token = request.form.get('token') or request.json.get('token')
    new_password = request.form.get('password') or request.json.get('password')
    
    if token in reset_tokens:
        email = reset_tokens[token]
        conn = get_db_connection()
        conn.execute('UPDATE users SET password_hash = ? WHERE email = ?', (new_password, email))
        conn.commit()
        conn.close()
        return "Parola a fost schimbata (Token-ul a ramas valid pentru reutilizare"
    
    return "Token invalid!", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)