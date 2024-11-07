# La función recibe name y password
# Si el usuario ya existe, debe retornar "User already registered"
# Si el usuario no existe, debe registrarlo y retornar "User successfully registered"
def registerUser(name, password):
    try:
        # Se abre el archivo en modo lectura para verificar si el usuario ya está registrado.
        with open('users_register.txt', 'r') as file:
            for line in file:
                if name in line:  # Se busca el nombre en el archivo.
                    #Si se encuentra el nombre, significa que ya se ha registrado
                    return "User already registered" 

    except FileNotFoundError:
        # Si el archivo no existe, se crea el archivo a continuación.
        pass

    # Si el usuario no está registrado, se agrega al archivo.
    with open('users_register.txt', 'a') as file:
        file.write(name + " " + password + "\n")  # Se registra el usuario y la contraseña.
        return "User successfully registered" 


# Función que abre o cierra una sesión
# Abre/cierra una sesión del usuario dependiendo del valor de flag 
# lo hace si el nombre de usuario y la contraseña son correctos
# Si la sesión se pudo abrir/cerrar debe retornar "Session was successfully opened/closed" de lo contrario
# debe retornar "error"
def openCloseSession(name, password, flag): 
    try:
        # Se abre el archivo en modo lectura
        with open('users_register.txt', 'r') as file:
            for line in file:
                # Se divide la línea en nombre y contraseña
                registered_name, registered_password = line.split()  
                
                # Se validan las credenciales
                if registered_name == name:
                    if registered_password == password:
                        if flag == True:  # Abrir sesión
                            # Agregar el nombre al archivo de sesiones
                            with open('sessions.txt', 'a') as session_file:
                                # Agregar el usuario a las sesiones abiertas
                                session_file.write(name + "\n")  
                            return "Session was successfully opened"
                        elif flag == False:  # Cerrar sesión
                            # Remover el nombre del archivo de sesiones
                            try:
                                with open('sessions.txt', 'r') as session_file:
                                    sessions = [line.strip() for line in session_file]

                                if name in sessions:
                                    # Quitar el usuario de la lista de sesiones abiertas
                                    sessions.remove(name)  

                                    with open('sessions.txt', 'w') as session_file:
                                        for session in sessions:
                                            #Se guardan las sesiones que siguen abiertas
                                            session_file.write(session + "\n")  

                                    return "Session was successfully closed"
                                else:
                                    return "error"  # El usuario no tiene sesión abierta
                            except FileNotFoundError:
                                return "error"  # El archivo de sesiones no existe

                    else:
                        return "error"  # Contraseña incorrecta

        return "error"  # Usuario no encontrado

    except FileNotFoundError:
        return "error"  # El archivo no existe


# Función que actualiza el puntaje
def updateScore(name, password, score):
    try:
        # Verificar si el usuario está registrado y la contraseña es correcta
        with open('users_register.txt', 'r') as file:
            for line in file:
                registered_name, registered_password = line.split()
                
                if registered_name == name and registered_password == password:
                    # Comprobar si el usuario tiene sesión abierta
                    try:
                        with open('sessions.txt', 'r') as session_file:
                            if name not in session_file.read().splitlines():
                                return "error"  # El usuario no tiene sesión abierta
                    except FileNotFoundError:
                        return "error"  # No hay sesiones

                    # Leer y actualizar el puntaje
                    try:
                        with open('scores.txt', 'r') as score_file:
                            scores = score_file.readlines()
                    except FileNotFoundError:
                        scores = []  # No hay puntajes registrados

                    # Actualizar el puntaje o agregar el usuario si no existe
                    updated = False
                    for i in range(len(scores)):
                        user, current_score = scores[i].strip().split()
                        if user == name:
                            new_score = int(current_score) + int(score)
                            scores[i] = f"{user} {new_score}\n"  # Actualizar el puntaje
                            updated = True
                            break
                    
                    if not updated:
                        scores.append(f"{name} {score}\n")  # Agregar nuevo puntaje

                    # Guardar los puntajes actualizados
                    with open('scores.txt', 'w') as score_file:
                        score_file.writelines(scores)

                    return "Score was successfully updated"

        return "error"  # Usuario no encontrado o contraseña incorrecta

    except FileNotFoundError:
        return "error"  # El archivo de usuarios no existe


# Función que lee el puntaje
# Retorna el puntaje del usuario si el nombre de usuario y la contraseña 
# son correctos y si el usuario se encuentra con sesión abierta
# Si se pudo leer el puntaje debe retornar el puntaje, de lo contrario
# debe retornar "error"
def getScore(name, password):
    try:
        # Verificar si el usuario está registrado y la contraseña es correcta
        with open('users_register.txt', 'r') as file:
            for line in file:
                registered_name, registered_password = line.split()
                
                if registered_name == name and registered_password == password:
                    # Comprobar si el usuario tiene sesión abierta
                    try:
                        with open('sessions.txt', 'r') as session_file:
                            if name not in session_file.read().splitlines():
                                return "error"  # El usuario no tiene sesión abierta
                    except FileNotFoundError:
                        return "error"  # No hay sesiones

                    # Leer el puntaje
                    try:
                        with open('scores.txt', 'r') as score_file:
                            for line in score_file:
                                user, current_score = line.strip().split()
                                if user == name:
                                    return current_score  # Retornar el puntaje
                    except FileNotFoundError:
                        return "error"  # No hay puntajes registrados

        return "error"  # Usuario no encontrado o contraseña incorrecta

    except FileNotFoundError:
        return "error"  # El archivo de usuarios no existe


# Función que lee la lista de usuarios conectados
# retorna una lista con los usuarios conectados, solo debe devolver nombre y puntaje
# si el nombre de usuario y la contraseña son correctos y si el usuario se encuentra con sesión abierta
# de lo contrario debe retornar "error"
def usersList(name, password):
    try:
        # Verificar si el usuario está registrado y la contraseña es correcta
        with open('users_register.txt', 'r') as file:
            for line in file:
                registered_name, registered_password = line.split()
                
                if registered_name == name and registered_password == password:
                    # Comprobar si el usuario tiene sesión abierta
                    try:
                        with open('sessions.txt', 'r') as session_file:
                            connected_users = session_file.read().splitlines()
                            if name not in connected_users:
                                return "error"  # El usuario no tiene sesión abierta
                    except FileNotFoundError:
                        return "error"  # No hay sesiones registradas

                    # Leer la lista de puntajes solo de usuarios conectados
                    try:
                        with open('scores.txt', 'r') as score_file:
                            list_sessions = []
                            for line in score_file:
                                username, current_score = line.strip().split()
                                if username in connected_users:  # Verificar si el usuario está conectado
                                    list_sessions.append((username, current_score))  # Guardar nombre y puntaje
                                # Retornar la lista de usuarios conectados y sus puntajes
                                return  list_sessions
                            else:
                                return "error"  # No hay puntajes para usuarios conectados

                    except FileNotFoundError:
                        return "error"  # El archivo no existe
                    
        return "error"  # Usuario no encontrado o contraseña incorrecta

    except FileNotFoundError:
        return "error"  # El archivo de usuarios no existe

# Función que genera una pregunta en una categoría cat
# retorna la pregunta si el nombre de usuario y la contraseña son correctos y si el usuario se encuentra con sesión abierta
# de lo contrario debe retornar "error"
from random import choice
def question(name, password, cat):
    try:
        # Verificar si el usuario está registrado y la contraseña es correcta
        with open('users_register.txt', 'r') as file:
            for line in file:
                registered_name, registered_password = line.split()

                if registered_name == name and registered_password == password:
                    # Comprobar si el usuario tiene sesión abierta
                    try:
                        with open('sessions.txt', 'r') as session_file:
                            if name not in session_file.read().splitlines():
                                return "error de usuario"  # El usuario no tiene sesión abierta
                    except FileNotFoundError:
                        return "error 1"  # No hay sesiones

                    # Leer las preguntas de la categoría especificada
                    try:
                        with open(f'questions_{cat}.txt', 'r') as question_file:
                            questions = question_file.readlines()
                            if not questions:
                                return "error 2"  # No hay preguntas en esta categoría

                            # Elegir una pregunta aleatoria
                            question_line = choice(questions).strip()
                            return  f"{(question_line)}" # Retornar la pregunta seleccionada

                    except FileNotFoundError:
                        return "error 3"  # No existe el archivo de questions

        return "error 4"  # Usuario no encontrado o contraseña incorrecta

    except FileNotFoundError:
        return "error 5"  # El archivo de usuarios no existe
