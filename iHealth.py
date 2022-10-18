#Programa que corre la aplicación de iHealth
#Grupo 4:
#Juan Miguel González-Campo Asturias 21077
#Paulo Raul Sánchez González 21401
#Pedro Javier Marroquín Abrego 21801

import os
import urllib.parse as up
from datetime import date
from datetime import datetime
from re import I
import sys
from tkinter import Menu
import psycopg2 as pg2
import getpass


#Conexión a la base de datos, utilizamos ElephantSQL para tener la base de datos en nube
up.uses_netloc.append("postgres")
url = up.urlparse("postgres://evsboafc:VOcaeA4yK8m4T9F-Ml7qf7-yWJ6UzFpx@babar.db.elephantsql.com/evsboafc")
conn = pg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port )


#Conectar base de datos
cur = conn.cursor()



#-----------------------FUNCIONES DE PROGRAMA-----------------------#

"""Main del programa

:return: None
"""
def main():
    #Conexion a la base de datos
    print("¡Bienvenido a iHealth!")
    print("""¿Que desea?
    1. Iniciar Sesion
    2. Registrarse
    3. Salir
    """)
    opc = input()

    if opc == "1":
        SignIn()
        return
    elif opc == "2":
        Register()
        return
    else:
        sys.exit()



"""Función para hace LOG IN

:return: usrID, el ID del usuario que se logueo.
"""
def SignIn():
    print("INICIAR SESION")
    print("\n1. Continuar\n2. Regresar a Inicio")
    opc = input("Ingrese su eleccion: ")
    if opc == "1":
        usr = input("Ingrese su usuario: ")
        usr = usr.lower()
        pas = getpass.getpass("Ingrese su contrasena (sensible a casos): ")

        cur.execute("SELECT idusuario FROM Usuario WHERE username = %s AND userpassword = %s", (usr, pas))

        if cur.rowcount == 1:
            usrID = cur.fetchone()[0]
            print("Bienvenido " + usr)
            #Se obtiene la clasificacion del usuario
            cur.execute("SELECT clasificacion FROM Usuario WHERE idusuario = %s", (int(usrID),))
            clasif = cur.fetchone()[0]

            #Se envia al usuario al menu correspondiente
            if clasif:
                MenuAdmin()
                return
            else:
                MenuCliente(usrID)
                return
        else:
            print("\nUsuario o contrasena incorrectos")
            SignIn()
            return

    elif opc == "2":
        main()
        return
    else:
        print("No ha marcado una opcion valida\n")
        SignIn()
        return


"""Menu para REGISTRAR un nuevo usuario

:return: None
"""
def Register():
    print("REGISTRAR UN NUEVO USUARIO")
    print("\n1. Continuar\n2. Regresar a Inicio")
    opc = input("Ingrese su eleccion: ")
    if opc == "1":
        print("\n")
        #Primero se genera el nuevo ID, viendo el antiguo ID más alto
        cur.execute("SELECT idUsuario FROM Usuario ORDER BY idUsuario DESC LIMIT 1")
        newID = cur.fetchone()[0] + 1

        email = input("Ingrese su email: ")
        email = email.lower()
        #Verifica que este email no este registrado
        cur.execute("SELECT * FROM Usuario WHERE email = %s", (email,))
        if cur.rowcount == 1:
            print("Ya existe una cuenta asociada a este email")
            Register()
            return
        #Se piden los datos del nuevo usuario
        usr = input("Ingrese su usuario: ")
        usr = usr.lower()
        #verifica que este nombre de usuario no haya sido registrado
        cur.execute("SELECT * FROM Usuario WHERE username = %s", (usr,))
        if cur.rowcount == 1:
            print("Este usuario ya existe")
            Register()
            return

        pswd = getpass.getpass("Ingrese su password (sensible a casos): ")
        pswd2 = getpass.getpass("Confirme su password (sensible a casos): ")
        #Verifica que las contraseñas sean iguales
        if pswd != pswd2:
            print("Las contrasenas no coinciden")
            Register()
            return

        #Se inserta ID generado, datos de usuario, clasificacion de usuario
        cur.execute("INSERT INTO Usuario (idusuario, username, userpassword, email, activo, clasificacion, fechainicio) VALUES (%s, %s, %s, %s, '0','0',CURRENT_DATE)", (newID, usr, pswd, email))
        conn.commit()
        print("Usuario registrado con exito")
        main()
        return
    elif opc == "2":
        main()
        return
    else:
        print("No ha marcado una opcion valida\n")
        Register()
        return



#--------------------------------- MENU CLIENTES ---------------------------------#
""" Menu que miran los clientes

:raram usrID: ID del usuario

:return: None
"""
def MenuCliente(usrID):
    print("\n\nMENU CLIENTE")
    cur.execute("SELECT * FROM Usuario WHERE idusuario = %s", (usrID,))
    infoUsr = cur.fetchone()
    nombre = infoUsr[5]

    #Revisa si el usuario tiene un plan activo
    if infoUsr[4] == False:
        print("Su cuenta no se encuentra activa, si desea activarla debe contratar un plan")
        print("¿Desea contratar un plan?\n1. Si\n2. No")
        op = input()
        if op == "1":
            activarCuenta(usrID)
            return
        else:
            main()
            return
    #Revisa si el usuario es nuevo
    if nombre is None:
        ingresoDatosCliente(usrID)
        return

    print("¿Que desea hacer?\n1. Registro diario\n2. Ver estadísticas de peso y calorias\n3. Ver y agregar sesiones\n4. Ver sesiones programadas e historicas\n5. Cerrar sesion\n6. Cerrar programa")
    op1 = input()
    if op1 == "1":
        cur.execute("SELECT fecha FROM registro WHERE idusuario = %s AND fecha = CURRENT_DATE", (usrID,))
        if cur.rowcount == 1:
            print("Ya ha realizado su registro diario")
            MenuCliente(usrID)
            return
        peso, calorias = registroDiario()
        cur.execute("INSERT INTO Registro (idusuario, calorias, pesoactual, fecha) VALUES (%s, %s, %s, CURRENT_DATE)", (usrID, calorias, peso))
        conn.commit()
        MenuCliente(usrID)
        return
    if op1 == "2":
        estadisticas(usrID)
        MenuCliente(usrID)
        return
    if op1 == "3":
        agregarSesion(usrID)
        return
    if op1 == "4":
        verSesiones(usrID)
        return
    if op1 == "5":
        main()
        return
    if op1 == "6":
        exit()
    else:
        print("No ha marcado una opcion valida")
        MenuCliente(usrID)
        return

"""Menu para ver las sesiones del usuario

:param usrID: ID del usuario

:return: None
"""
def verSesiones(usrID):
    print("1. Ver sesiones programadas")
    print("2. Ver sesiones historicas ")
    print("3. Regresar a menu principal")
    op2=input()
    if op2=="1":
        print("Sus sesiones programadas son las siguientes:")
        cur.execute("SELECT sesion.idsesion, inst.nombre as nombre, inst.apellido as apellido, cat.nombre as categoria, fecha, hora, duracion FROM sesion LEFT JOIN usuariosesion as usr ON sesion.idsesion = usr.idsesion LEFT JOIN instructor as inst ON sesion.idinstructor = inst.idinstructor LEFT JOIN categoria as cat ON sesion.idcategoria = cat.idcategoria WHERE usr.idusuario = %s AND fecha >= CURRENT_DATE ORDER BY fecha ASC, hora ASC",(usrID,))
        sesiones = cur.fetchall()
        if (len(sesiones) == 0):
            print("No tiene sesiones programadas")
            verSesiones(usrID)
            return
        for i in range (0,len(sesiones)):
            print(i+1, ".",  "Instructor: ", sesiones[i][1], sesiones[i][2], ", Categoria:", sesiones[i][3], ", Fecha:", sesiones[i][4], ", Hora:", sesiones[i][5], ", Duracion (mins):", sesiones[i][6])
        MenuCliente(usrID)
        return
    if op2=="2":
        print("Sus sesiones historicas son las siguientes: ")
        cur.execute("SELECT sesion.idsesion, inst.nombre as nombre, inst.apellido as apellido, cat.nombre as categoria, fecha, hora, duracion FROM sesion LEFT JOIN usuariosesion as usr ON sesion.idsesion = usr.idsesion LEFT JOIN instructor as inst ON sesion.idinstructor = inst.idinstructor LEFT JOIN categoria as cat ON sesion.idcategoria = cat.idcategoria WHERE usr.idusuario = %s AND fecha < CURRENT_DATE ORDER BY fecha DESC, hora DESC",(usrID,))
        sesiones = cur.fetchall()
        if (len(sesiones) == 0):
            print("No tiene sesiones pasadas")
            verSesiones(usrID)
            return
        for i in range (0,len(sesiones)):
            print(i+1, ".",  "Instructor: ", sesiones[i][1], sesiones[i][2], ", Categoria:", sesiones[i][3], ", Fecha:", sesiones[i][4], ", Hora:", sesiones[i][5], ", Duracion (mins):", sesiones[i][6])
        MenuCliente(usrID)
        return
    if op2=="3":
        MenuCliente(usrID)
    else:
        print("No ha marcado una opcion valida")
        verSesiones(usrID)
        return



"""Estadísticas de los registros diarios del usuario

:param usrID: ID del usuario

:return: None

"""
def estadisticas(usrID):

    print("Estadisticas de todos los tiempos: ")
    cur.execute("SELECT max(pesoactual), min(pesoactual), avg(pesoactual) FROM registro WHERE idusuario = %s", (usrID,))
    maxPeso, minPeso, avgPeso = cur.fetchone()
    print("\nPeso:\nPeso máximo: ", maxPeso)
    print("Peso mínimo: ", minPeso)
    print("Peso promedio: ", round(avgPeso, 2))

    cur.execute("SELECT max(calorias), min(calorias), avg(calorias) FROM registro WHERE idusuario = %s", (usrID,))
    maxCal, minCal, avgCal = cur.fetchone()
    print("\nCalorias:\nCalorías máximas: ", maxCal)
    print("Calorías mínimas: ", minCal)
    print("Calorías promedio: ", round(avgCal, 2))

    print("\nEstadisticas de los últimos 7 días: ")
    cur.execute("SELECT max(pesoactual), min(pesoactual), avg(pesoactual) FROM registro WHERE idusuario = %s AND fecha >= (now() - interval '7 days')", (usrID,))
    maxPeso, minPeso, avgPeso = cur.fetchone()
    print("\nPeso:\nPeso máximo: ", maxPeso)
    print("Peso mínimo: ", minPeso)
    print("Peso promedio: ", round(avgPeso, 2))

    cur.execute("SELECT max(calorias), min(calorias), avg(calorias) FROM registro WHERE idusuario = %s AND fecha >= (now() - interval '7 days')", (usrID,))
    maxCal, minCal, avgCal = cur.fetchone()
    print("\nCalorias:\nCalorías máximas: ", maxCal)
    print("Calorías mínimas: ", minCal)
    print("Calorías promedio: ", round(avgCal, 2))



"""Funcion para agregar sesiones a su calendario

:param usrID: ID del usuario

:return: None
"""
def agregarSesion(usrID):
    print("¿Cómo desea buscar la sesion?\n1. fecha \n2. hora\n3. duracion\n4. categoria\n5. instructor\n6. regresar")
    op = input()
    if op == "1":
        fecha = input("Ingrese la fecha de la sesion (YYYY-MM-DD): ")
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            print("No ha ingresado una fecha valida")
            agregarSesion(usrID)
            return
        if fecha < date.today():
            print("La fecha ingresada es anterior a la fecha actual")
            agregarSesion(usrID)
            return
        cur.execute("SELECT idsesion, inst.nombre as nombre, inst.apellido as apellido, cat.nombre as categoria, fecha, hora, duracion FROM sesion LEFT JOIN categoria as cat on sesion.idcategoria = cat.idcategoria LEFT JOIN instructor as inst on sesion.idinstructor = inst.idinstructor WHERE fecha = %s ORDER BY hora asc", (fecha,))
        sesiones = cur.fetchall()

        if (len(sesiones) == 0):
            print("No hay sesiones para esa fecha")
            agregarSesion(usrID)
            return
        print("Sesiones: ")
        for i in range (0,len(sesiones)):
            print(i+1, ".",  "Instructor: ", sesiones[i][1], sesiones[i][2], ", Categoria:", sesiones[i][3], ", Fecha:", sesiones[i][4], ", Hora:", sesiones[i][5], ", Duracion (mins):", sesiones[i][6])
        seleccion = input("Ingrese el numero de la sesion que desea agregar: ")
        if seleccion.isnumeric():
            seleccion = int(seleccion) -1
            if seleccion < 0 or seleccion > len(sesiones)-1:
                print("No ha ingresado una sesion valida")
                agregarSesion(usrID)
                return
        else:
            print("No ha ingresado un numero valido")
            agregarSesion(usrID)
            return
        sesion = sesiones[seleccion]
        cur.execute("SELECT * FROM usuariosesion WHERE idusuario = %s AND idsesion = %s", (usrID, sesion[0]))
        if (cur.fetchone() != None):
            print("Ya esta inscrito en esa sesion")
            agregarSesion(usrID)
            return
        cur.execute("INSERT INTO usuariosesion (idusuario, idsesion) VALUES (%s, %s)", (usrID, sesion[0]))
        print("Sesion agregada con exito")
        conn.commit()
        MenuCliente(usrID)
        return

    if op == "2":
        hora = input("Ingrese la hora de la sesion (ingrese solo la hora exacta e.g. ""19"" o ""7""): ")
        hora = hora+":00:00"
        cur.execute("SELECT idsesion, inst.nombre as nombre, inst.apellido as apellido, cat.nombre as categoria, fecha, hora, duracion FROM sesion LEFT JOIN categoria as cat on sesion.idcategoria = cat.idcategoria LEFT JOIN instructor as inst on sesion.idinstructor = inst.idinstructor WHERE hora = %s AND fecha >= CURRENT_DATE ORDER BY fecha, hora asc", (hora,))
        sesiones = cur.fetchall()
        if (len(sesiones) == 0):
            print("No hay sesiones para esa hora")
            agregarSesion(usrID)
            return
        print("Sesiones: ")
        for i in range (0,len(sesiones)):
            print(i+1, ".",  "Instructor: ", sesiones[i][1], sesiones[i][2], ", Categoria:", sesiones[i][3], ", Fecha:", sesiones[i][4], ", Hora:", sesiones[i][5], ", Duracion (mins):", sesiones[i][6])
        seleccion = input("Ingrese el numero de la sesion que desea agregar: ")
        if seleccion.isnumeric():
            seleccion = int(seleccion) -1
            if seleccion < 0 or seleccion > len(sesiones)-1:
                print("No ha ingresado una sesion valida")
                agregarSesion(usrID)
                return
        else:
            print("No ha ingresado un numero valido")
            agregarSesion(usrID)
            return
        sesion = sesiones[seleccion]
        cur.execute("SELECT * FROM usuariosesion WHERE idusuario = %s AND idsesion = %s", (usrID, sesion[0]))
        if (cur.fetchone() != None):
            print("Ya esta inscrito en esa sesion")
            agregarSesion(usrID)
            return
        cur.execute("INSERT INTO usuariosesion (idusuario, idsesion) VALUES (%s, %s)", (usrID, sesion[0]))
        print("Sesion agregada con exito")
        conn.commit()
        MenuCliente(usrID)
        return

    if op == "3":
        duracion = input("Haga su selección: 1. Sesiones de 30 minutos 2. Sesiones de 1 hora): ")
        if duracion == "1":
            duracion = 30
        elif duracion == "2":
            duracion = 60
        cur.execute("SELECT idsesion, inst.nombre as nombre, inst.apellido as apellido, cat.nombre as categoria, fecha, hora, duracion FROM sesion LEFT JOIN categoria as cat on sesion.idcategoria = cat.idcategoria LEFT JOIN instructor as inst on sesion.idinstructor = inst.idinstructor WHERE duracion = %s AND fecha >= CURRENT_DATE ORDER BY fecha asc, hora asc", (duracion,))
        sesiones = cur.fetchall()
        if (len(sesiones) == 0):
            print("No hay sesiones con esa duracion")
            agregarSesion(usrID)
            return
        print("Sesiones: ")
        for i in range (0,len(sesiones)):
            print(i+1, ".",  "Instructor: ", sesiones[i][1], sesiones[i][2], ", Categoria:", sesiones[i][3], ", Fecha:", sesiones[i][4], ", Hora:", sesiones[i][5], ", Duracion (mins):", sesiones[i][6])
        seleccion = input("Ingrese el numero de la sesion que desea agregar: ")
        if seleccion.isnumeric():
            seleccion = int(seleccion) -1
            if seleccion < 0 or seleccion > len(sesiones)-1:
                print("No ha ingresado una sesion valida")
                agregarSesion(usrID)
                return
        else:
            print("No ha ingresado un numero valido")
            agregarSesion(usrID)
            return
        sesion = sesiones[seleccion]
        cur.execute("SELECT * FROM usuariosesion WHERE idusuario = %s AND idsesion = %s", (usrID, sesion[0]))
        if (cur.fetchone() != None):
            print("Ya esta inscrito en esa sesion")
            agregarSesion(usrID)
            return
        cur.execute("INSERT INTO usuariosesion (idusuario, idsesion) VALUES (%s, %s)", (usrID, sesion[0]))
        print("Sesion agregada con exito")
        conn.commit()
        MenuCliente(usrID)
        return
    if op == "4":
        print("¿Que categoria desea buscar?")
        cur.execute("SELECT * FROM categoria ORDER BY idcategoria asc")
        categorias = cur.fetchall()
        for i in range (0,len(categorias)-1):
            print(i+1, ".",  categorias[i][1])
        categoria = input("Ingrese el numero de la categoria que desea buscar: ")
        if categoria.isnumeric():
            categoria = int(categoria)-1
            if categoria < 0 or categoria > len(categorias)-1:
                print("No ha ingresado una categoria valida")
                agregarSesion(usrID)
                return
        else:
            print("No ha ingresado una categoria valida")
            agregarSesion(usrID)
            return
        cat = categorias[categoria][0]
        cur.execute("SELECT idsesion, inst.nombre, inst.apellido, (SELECT nombre FROM categoria WHERE idcategoria = %s) as Categoria, fecha, hora, duracion FROM sesion NATURAL JOIN instructor as inst WHERE fecha >= CURRENT_DATE AND idcategoria = %s ORDER BY fecha asc, hora asc", (cat,cat))
        sesiones = cur.fetchall()
        if (len(sesiones) == 0):
            print("No hay sesiones con esa categoria")
            agregarSesion(usrID)
            return
        print("Sesiones: ")
        for i in range (0,len(sesiones)):
            print(i+1, ".",  "Instructor: ", sesiones[i][1], sesiones[i][2], ", Categoria:", sesiones[i][3], ", Fecha:", sesiones[i][4], ", Hora:", sesiones[i][5], ", Duracion (mins):", sesiones[i][6])
        seleccion = input("Ingrese el numero de la sesion que desea agregar: ")
        if seleccion.isnumeric():
            seleccion = int(seleccion) -1
            if seleccion < 0 or seleccion > len(sesiones)-1:
                print("No ha ingresado una sesion valida")
                agregarSesion(usrID)
                return
        else:
            print("No ha ingresado un numero valido")
            agregarSesion(usrID)
            return
        sesion = sesiones[seleccion]
        cur.execute("SELECT * FROM usuariosesion WHERE idusuario = %s AND idsesion = %s", (usrID, sesion[0]))
        if (cur.fetchone() != None):
            print("Ya esta inscrito en esa sesion")
            agregarSesion(usrID)
            return
        cur.execute("INSERT INTO usuariosesion (idusuario, idsesion) VALUES (%s, %s)", (usrID, sesion[0]))
        print("Sesion agregada con exito")
        conn.commit()
        MenuCliente(usrID)
        return
    if op == "5":
        print("¿Con que instructor desea trabajar?")
        cur.execute("SELECT * FROM instructor ORDER BY idinstructor asc")
        instructores = cur.fetchall()
        for i in range (0,len(instructores)):
            print(i+1, ".",  instructores[i][1], instructores[i][2])
        instructor = input("Ingrese el numero del instructor con el que quiere trabajar: ")
        if instructor.isnumeric():
            instructor = int(instructor)-1
            if instructor < 0 or instructor > len(instructores)-1:
                print("No ha ingresado una numero valido")
                agregarSesion(usrID)
                return
        else:
            print("No ha ingresado un instructor valido")
            agregarSesion(usrID)
            return

        inst = instructores[instructor][0]
        cur.execute("SELECT idinstructor, activo FROM instructor WHERE idinstructor = %s", (inst,))
        instCheck = cur.fetchone()
        if instCheck[1] == False:
            print("Lo sentimos este instructor no esta disponible")
            agregarSesion(usrID)
            return
        cur.execute("SELECT idsesion, (SELECT nombre FROM instructor WHERE idinstructor = %s) as nombre, (SELECT apellido FROM instructor WHERE idinstructor = %s) as apellido, cat.nombre as Categoria, fecha, hora, duracion FROM sesion NATURAL JOIN categoria as cat WHERE fecha >= CURRENT_DATE AND idinstructor = %s ORDER BY fecha asc, hora asc", (inst,inst,inst))
        sesiones = cur.fetchall()
        if len(sesiones) == 0:
            print("No hay sesiones con ese instructor")
            agregarSesion(usrID)
            return
        for i in range (0,len(sesiones)):
            print(i+1, ".",  "Instructor: ", sesiones[i][1], sesiones[i][2], ", Categoria:", sesiones[i][3], ", Fecha:", sesiones[i][4], ", Hora:", sesiones[i][5], ", Duracion (mins):", sesiones[i][6])
        seleccion = input("Ingrese el numero de la sesion que desea agregar: ")
        if seleccion.isnumeric():
            seleccion = int(seleccion) -1
            if seleccion < 0 or seleccion > len(sesiones)-1:
                print("No ha ingresado una sesion valida")
                agregarSesion(usrID)
                return
        else:
            print("No ha ingresado un numero valido")
            agregarSesion(usrID)
            return
        sesion = sesiones[seleccion]
        cur.execute("SELECT * FROM usuariosesion WHERE idusuario = %s AND idsesion = %s", (usrID, sesion[0]))
        if (cur.fetchone() != None):
            print("Ya esta inscrito en esa sesion")
            agregarSesion(usrID)
            return
        cur.execute("INSERT INTO usuariosesion (idusuario, idsesion) VALUES (%s, %s)", (usrID, sesion[0]))
        print("Sesion agregada con exito")
        conn.commit()
        MenuCliente(usrID)
        return
    if op == "6":
        MenuCliente(usrID)
        return

"""Cuando es el primer log in del usuario, se le pide que ingrese sus datos para su perfil

:param usrID: ID del usuario que se esta registrando

:return: None
"""
def ingresoDatosCliente(usrID):
    print("Por favor complete su perfil: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    nacAnio = input("Anio de nacimiento: ")
    nacMes = input("Mes de nacimiento: ")
    nacDia = input("Dia de nacimiento: ")
    estatura = input("Estatura (en CM, sin decimales): ")
    direccion = input("Direccion: ")

    #concatenar fecha de nacimiento
    fechaNac = nacAnio + "-" + nacMes + "-" + nacDia

    #Se actualiza la informacion del usuario en postgres
    cur.execute("UPDATE Usuario SET nombre = %s, apellido = %s, fechanacimiento = %s, altura = %s, direccion = %s WHERE idusuario = %s", (nombre, apellido, fechaNac, estatura, direccion, usrID))
    conn.commit()

    print("\nPerfil actualizado con exito")
    MenuCliente(usrID)
    return


"""Cuando es el primer log in del usuario, se le pide que contrate un plan

:param usrID: ID del usuario que se esta registrando

:return: None
"""
def activarCuenta(usrID):
    print("Contratar un plan")

    print("¿Que plan desea contratar?\n1. Plan Oro Q250.00 (al mes): Acceso a nuestro servicio, incluye prestamo de un smartwatch, sesiones 24/7.\n2. Plan Diamante Q500.00 (al mes): Incluye todo lo del plan Oro y adicional 1 consulta con un nutricionista al mes!\nIncluye además el Smartwatch de regalo luego de un contrato mínimo de 12 meses.\n3. No deseo contratar un plan")

    op = input()
    if op == "1":
        print("Plan Oro seleccionado")
        print("¿Desea contratar este plan?\n1. Si\n2. No")
        op2 = input()
        if op2 == "1":
            print("Los numeros de su tarjeta (sin espacios): ")
            tarjeta = input()
            if len(tarjeta) != 16:
                print("El numero de tarjeta no es valido")
                activarCuenta()
                return
            print("Nombre en Tarjeta (incluido apellido): ")
            nombre = input()

            cur.execute("INSERT INTO infopago (idusuario, numtajeta, nombretarjeta) VALUES (%s, %s, %s)", (usrID, tarjeta, nombre))
            conn.commit()
            print("Informacion de pago registrada con exito")
            print("¿Desea realizar el pago por Q250.00 ahora?\n1. Si\n2. No")
            op3 = input()
            if op3 == "1":
                print("Pago realizado con exito")
                cur.execute("UPDATE Usuario SET activo = '1', suscripcion = 1 WHERE idusuario = %s", (usrID,))
                conn.commit()
                print("Su cuenta se encuentra activa")
                MenuCliente(usrID)
                return
            if op3 == "2":
                print("Sentimos que no haya podido realizar el pago ahora, su cuenta se encuentra inactiva")
                cur.execute("UPDATE Usuario SET activo = '0', suscripcion = NULL WHERE idusuario = %s", (usrID,))
                MenuCliente(usrID)
                return
            else:
                print("No ha marcado una opcion valida")
                activarCuenta(usrID)
                return
        else:
            activarCuenta(usrID)
            return
    elif op == "2":
        print("Plan Diamante seleccionado")
        print("¿Desea contratar este plan?\n1. Si\n2. No")
        op2 = input()
        if op2 == "1":
            print("Los numeros de su tarjeta (sin espacios): ")
            tarjeta = input()
            if len(tarjeta) != 16:
                print("El numero de tarjeta no es valido")
                activarCuenta()
                return
            print("Nombre en Tarjeta (incluido apellido): ")
            nombre = input()

            cur.execute("INSERT INTO infopago (idusuario, numtajeta, nombretarjeta) VALUES (%s, %s, %s)", (usrID, tarjeta, nombre))
            conn.commit()
            print("Informacion de pago registrada con exito")
            print("¿Desea realizar el pago por Q500.00 ahora?\n1. Si\n2. No")
            op3 = input()
            if op3 == "1":
                print("Pago realizado con exito")
                cur.execute("UPDATE Usuario SET activo = '1', suscripcion = 2 WHERE idusuario = %s", (usrID,))
                conn.commit()
                print("Su cuenta se encuentra activa")
                MenuCliente(usrID)
                return
            if op3 == "2":
                print("Sentimos que no haya podido realizar el pago ahora, su cuenta se encuentra inactiva")
                cur.execute("UPDATE Usuario SET activo = '0' WHERE idusuario = %s", (usrID,))
                conn.commit()
                MenuCliente(usrID)
                return
            else:
                print("No ha marcado una opcion valida")
                activarCuenta(usrID)
                return
        else:
            activarCuenta(usrID)
            return
    elif op == "3":
        print("Su cuenta se mantendra inactiva")
        MenuCliente(usrID)
        return
    else:
        print("No ha marcado una opcion valida")
        activarCuenta(usrID)
        return

def registroDiario():
    print("Registro diario")
    calorias = int(input("Calorias estimadas (ingrese un número entero): "))
    peso = int(input("Peso en LBS (ingrese un número entero): "))

    return peso, calorias







# --------------------------------- MENU ADMINS --------------------------------- #
""" Menu de administrador

:param usrID: ID del usuario que se esta registrando

:return: None
"""
def MenuAdmin():
    print("\n\nMENU ADMINISTRADOR")
    print("¿Que desea hacer?")
    print("1. Agregar, modificar, dar de baja a un instructor\n2. Agregar, modificar o dar de baja una sesion\n3. Modificar o dar de baja a un usuario\n4. Ver estadisticas\n5. Crear nuevo usuario de administrador\n6. Salir")
    op = input()
    if op == "1":
        print("¿Que desea hacer?\n1. Agregar instructor\n2. Modificar, reactivar o dar de baja instructor\n3. Regresar")
        op2 = input()
        if op2 == "1":
            agregarInstructor()
            return
        elif op2 == "2":
            modificarInstructor()
            return
        elif op2 == "3":
            MenuAdmin()
            return
        else:
            print("No ha marcado una opcion valida")
            MenuAdmin()
            return
    elif op == "2":
        print("¿Que desea hacer?\n1. Agregar sesion\n2. Modificar sesion\n3. Dar de baja sesion")
        op2 = input()
        if op2 == "1":
            nuevaSesion()
            return
        elif op2 == "2":
            modificarSesion()
            return
        elif op2 == "3":
            eliminarSesion()
            return
        else:
            print("No ha marcado una opcion valida")
            MenuAdmin()
            return
    elif op == "3":
        print("¿Que desea hacer?\n1. Modificar usuario\n2. Dar de baja usuario")
        op2 = input()
        if op2 == "1":
            modificarUsuario()
            return
        elif op2 == "2":
            bajaUsuario()
            return
        else:
            print("No ha marcado una opcion valida")
            MenuAdmin()
            return
    elif op == "4":
        reportes()
        return
    elif op == "5":
        crearAdmin()
        return
    elif op == "6":
        print("Saliendo...")
        exit()
    else:
        print("No ha marcado una opcion valida")
        MenuAdmin()
        return

def agregarInstructor():
    print("Desea agregar un instructor?\n1. Si\n2. No, regresar a menu de administradores")
    op = input()
    if op == "1":
        print("Ingrese los datos del instructor nuevo: ")
    elif op == "2":
        MenuAdmin()
        return
    else:
        print("No ha marcado una opcion valida")
        agregarInstructor()
        return
    cur.execute("SELECT idinstructor FROM Instructor ORDER BY idinstructor DESC LIMIT 1")
    id = cur.fetchone()[0]+1
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    cur.execute("INSERT INTO instructor (idinstructor, nombre, apellido, activo, fechainicio) VALUES (%s, %s, %s, '1', CURRENT_DATE)", (id, nombre, apellido))
    conn.commit()
    print("Instructor agregado con exito")
    MenuAdmin()

    return

def modificarInstructor():
    print("Desea modificar un instructor 1. Si 2. No, regresar a menu de administradores")
    op1 = input()
    if op1 == "2":
        MenuAdmin()
        return
    elif op1 == "1":
        print("Instructores: ")
    else:
        print("No ha marcado una opcion valida")
        modificarInstructor()
        return
    cur.execute("SELECT * FROM instructor ORDER BY idinstructor ASC")
    instructores = cur.fetchall()
    for i in range (0,len(instructores)):
            print("ID:",instructores[i][0], ",Nombre: " ,instructores[i][1], ",Apellido:", instructores[i][2], ",Activo:", instructores[i][3], ",Fecha de inicio:", instructores[i][4], ",Fecha final:", instructores[i][5])
    instructor = input("Ingrese el ID del instructor que desea modificar: ")
    if instructor.isnumeric():
        instructor = int(instructor)
        if instructor < 1 or instructor > len(instructores):
            print("No ha ingresado una ID valido")
            modificarInstructor()
            return
    instNum = instructor-1
    print("Que desea modificar del instructor?")
    print("1. Nombre\n2. Apellido\n3. Dar de baja o reactivar\n4. Regresar")
    op = input()
    if op == "1":
        nombre = input("Ingrese el nuevo nombre: ")
        cur.execute("UPDATE instructor SET nombre = %s WHERE idinstructor = %s", (nombre, instructor))
        conn.commit()
        print("Nombre modificado con exito")
        MenuAdmin()
        return
    elif op == "2":
        apellido = input("Ingrese el nuevo apellido: ")
        cur.execute("UPDATE instructor SET apellido = %s WHERE idinstructor = %s", (apellido, instructor))
        conn.commit()
        print("Apellido modificado con exito")
        MenuAdmin()
        return
    elif op == "3":
        print("¿Desea activar o desactivar al instructor? Recuerde que la fecha final del instructor se actualizara automaticamente (si se activa será nula si se desactiva sera la de hoy), si se activa un instructor su fecha de inicio se cambiara automaticamente a la fecha de hoy")
        print("1. Activar\n2. Desactivar")
        op2 = input()
        if op2 == "1":
            if instructores[instNum][3] == 1:
                print("El instructor ya esta activo")
                modificarInstructor()
                return
            cur.execute("UPDATE instructor SET activo = '1', fechafinal = NULL, fechainicio = CURRENT_DATE WHERE idinstructor = %s", (instructor,))
            conn.commit()
            print("Instructor activado con exito")
            MenuAdmin()
            return
        elif op2 == "2":
            if instructores[instNum][3] == 0:
                print("El instructor ya esta desactivado")
                modificarInstructor()
                return
            cur.execute("UPDATE instructor SET activo = '0', fechafinal = CURRENT_DATE WHERE idinstructor = %s", (instructor,))
            conn.commit()
            print("Instructor desactivado con exito")
            MenuAdmin()
            return
        else:
            print("No ha marcado una opcion valida")
            modificarInstructor()
            return
    elif op == "4":
        modificarInstructor()
        return
    else:
        print("No ha marcado una opcion valida")
        modificarInstructor()
        return

def nuevaSesion():
    print("Desea agregar una nueva sesion?\n1. Si\n2. No, regresar a menu de administradores")
    op = input()
    if op == "1":
        print("Ingrese los datos de la nueva sesion: ")
    elif op == "2":
        MenuAdmin()
        return
    else:
        print("No ha marcado una opcion valida")
        nuevaSesion()
        return
    cur.execute("SELECT idsesion FROM sesion ORDER BY idsesion DESC LIMIT 1")
    #Crear ID
    id = cur.fetchone()[0]+1

    #Obtener instructor
    cur.execute("SELECT * FROM instructor WHERE activo = '1' ORDER BY idinstructor ASC")
    instructores = cur.fetchall()
    for i in range (0,len(instructores)):
            print("ID:",instructores[i][0], ",Nombre: " ,instructores[i][1], ",Apellido:", instructores[i][2], ",Activo:", instructores[i][3], ",Fecha de inicio:", instructores[i][4], ",Fecha final:", instructores[i][5])
    instructor = input("Ingrese el ID del instructor que dara la sesion: ")
    if instructor.isnumeric():
        instructor = int(instructor)
        if instructor < 1 or instructor > len(instructores):
            print("No ha ingresado una ID valido")
            nuevaSesion()
            return
    instNum = instructor-1
    if instructores[instNum][3] == 0:
        print("El instructor no esta activo")
        nuevaSesion()
        return
    #Obtener categoria
    print("Seleccione categoria de la sesion")
    cur.execute("SELECT * FROM categoria ORDER BY idcategoria ASC")
    categorias = cur.fetchall()
    for i in range (0,len(categorias)-1):
        print(i+1, ".",  categorias[i][1])
    categoria = input("Ingrese el numero de la categoria: ")
    if categoria.isnumeric():
        categoria = int(categoria)-1
        if categoria < 0 or categoria > len(categorias)-1:
            print("No ha ingresado una categoria valida")
            nuevaSesion()
            return
    else:
        print("No ha ingresado una categoria valida")
        nuevaSesion()
        return
    selecCategoria = categorias[categoria][0]
    #Obtener fecha
    fecha = input("Ingrese la fecha de la sesion (YYYY-MM-DD): ")
    try:
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    except ValueError:
        print("No ha ingresado una fecha valida")
        nuevaSesion()
        return
    if fecha < date.today():
        print("La fecha ingresada es anterior a la fecha actual")
        nuevaSesion()
        return

    #Obtener hora
    hora = input("Ingrese la hora de la sesion (HH): ")
    if hora.isnumeric():
        hora = int(hora)
        if hora < 0 or hora > 23:
            print("No ha ingresado una hora valida")
            nuevaSesion()
            return
    hora = str(hora)+":00:00"


    #Obtener duracion
    duracion = input("Duracion de la sesion. \n1. Sesion de 30 minutos\n2. Sesion de 60 minutos\n")
    if duracion == "1":
        duracion = 30
    elif duracion == "2":
        duracion = 60
    else:
        print("No ha ingresado una opcion valida")
        nuevaSesion()
        return

    #Insertar sesion
    cur.execute("INSERT INTO sesion (idsesion, idinstructor, idcategoria, fecha, hora, duracion) VALUES (%s, %s, %s, %s, %s, %s)", (id, instructor, selecCategoria, fecha, hora, duracion))
    conn.commit()
    print("Sesion agregada con exito")
    MenuAdmin()
    return

def modificarSesion():

    cur.execute("SELECT * FROM sesion WHERE fecha >= CURRENT_DATE ORDER BY idsesion ASC")
    sesiones = cur.fetchall()
    if (len(sesiones)== 0):
        print("No existen sesiones proximas.")
        MenuAdmin()
        return
    print("Seleccione la sesion que desea modificar: ")
    sesIDs = []
    for i in range (0,len(sesiones)):
        sesIDs.append(sesiones[i][0])
    for i in range (0,len(sesiones)):
        print("ID:",sesiones[i][0], ",ID instructor: " ,sesiones[i][1], ",ID categoria:", sesiones[i][2], ",Fecha:", sesiones[i][3], ",Hora:", sesiones[i][4], ",Duracion:", sesiones[i][5])
    sesion = input("Ingrese el ID de la sesion: ")
    if sesion.isnumeric():
        sesion = int(sesion)
        if sesion not in sesIDs:
            print("No ha ingresado una ID valido")
            modificarSesion()
            return
    cur.execute("SELECT * FROM sesion WHERE idsesion = %s", (sesion,))
    ses1 = cur.fetchone()
    print("Que desea modificar?\n1. Instructor\n2. Categoria\n3. Fecha\n4. Hora\n5. Duracion\n6. Regresar a menu de administradores")
    op = input()
    if op == "1":
        cur.execute("SELECT * FROM instructor WHERE activo = '1' ORDER BY idinstructor ASC")
        instructores = cur.fetchall()
        insIDs = []
        for i in range (0,len(instructores)):
            insIDs.append(instructores[i][0])
        for i in range (0,len(instructores)):
                print("ID:",instructores[i][0], ",Nombre: " ,instructores[i][1], ",Apellido:", instructores[i][2], ",Activo:", instructores[i][3], ",Fecha de inicio:", instructores[i][4], ",Fecha final:", instructores[i][5])
        instructor = input("Ingrese el ID del instructor que dara la sesion: ")
        if instructor.isnumeric():
            instructor = int(instructor)
            if instructor not in insIDs:
                print("No ha ingresado una ID valido")
                modificarSesion()
                return

        instNum = instructor-1
        if instructores[instNum][3] == 0:
            print("El instructor no esta activo")
            modificarSesion()
            return
        if ses1[1] == instructor:
            print("El instructor ingresado es el mismo que el actual")
            modificarSesion()
            return
        cur.execute("UPDATE sesion SET idinstructor = %s WHERE idsesion = %s", (instructor, sesion))
        conn.commit()
        print("Instructor modificado con exito")
        MenuAdmin()
        return
    elif op == "2":
        print("Seleccione categoria de la sesion")
        cur.execute("SELECT * FROM categoria ORDER BY idcategoria ASC")
        categorias = cur.fetchall()
        for i in range (0,len(categorias)-1):
            print(i+1, ".",  categorias[i][1])
        categoria = input("Ingrese el numero de la categoria: ")
        if categoria.isnumeric():
            categoria = int(categoria)-1
            if categoria < 0 or categoria > len(categorias)-1:
                print("No ha ingresado una categoria valida")
                modificarSesion()
                return
        else:
            print("No ha ingresado una categoria valida")
            modificarSesion()
            return
        selecCategoria = categorias[categoria][0]
        if ses1[2] == selecCategoria:
            print("La categoria ingresada es la misma que la actual")
            modificarSesion()
            return
        cur.execute("UPDATE sesion SET idcategoria = %s WHERE idsesion = %s", (selecCategoria, sesion))
        conn.commit()
        print("Categoria modificada con exito")
        MenuAdmin()
        return
    elif op == "3":
        fecha = input("Ingrese la fecha de la sesion (YYYY-MM-DD): ")
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            print("No ha ingresado una fecha valida")
            modificarSesion()
            return
        if fecha < date.today():
            print("La fecha ingresada es anterior a la fecha actual")
            modificarSesion()
            return
        if ses1[3] == fecha:
            print("La fecha ingresada es la misma que la actual")
            modificarSesion()
            return
        cur.execute("UPDATE sesion SET fecha = %s WHERE idsesion = %s", (fecha, sesion))
        conn.commit()
        print("Fecha modificada con exito")
        MenuAdmin()
        return
    elif op == "4":
        hora = input("Ingrese la hora de la sesion (HH): ")
        if hora.isnumeric():
            hora = int(hora)
            if hora < 0 or hora > 23:
                print("No ha ingresado una hora valida")
                modificarSesion()
                return
        else:
            print("No ha ingresado una hora valida")
            modificarSesion()
            return
        hora = str(hora)+":00:00"
        if ses1[4] == hora:
            print("La hora ingresada es la misma que la actual")
            modificarSesion()
            return
        cur.execute("UPDATE sesion SET hora = %s WHERE idsesion = %s", (hora, sesion))
        conn.commit()
        print("Hora modificada con exito")
        MenuAdmin()
        return
    elif op == "5":
        duracion = input("Nueva duracion.\n1. 30 minutos\n2. 60 minutos ")
        if duracion.isnumeric():
            duracion = int(duracion)
            if duracion < 1 or duracion > 2:
                print("No ha ingresado una duracion valida")
                modificarSesion()
                return
        else:
            print("No ha ingresado una eleccion valida")
            modificarSesion()
            return
        if duracion == 1:
            duracion = 30
        if duracion == 2:
            duracion = 60
        if ses1[5] == duracion:
            print("La duracion ingresada es la misma que la actual")
            modificarSesion()
            return
        cur.execute("UPDATE sesion SET duracion = %s WHERE idsesion = %s", (duracion, sesion))
        conn.commit()
        print("Duracion modificada con exito")
        MenuAdmin()
        return
    elif op == "6":
        MenuAdmin()
        return

def eliminarSesion():
    print("Eliminar sesion")
    cur.execute("SELECT * FROM sesion WHERE fecha >= CURRENT_DATE ORDER BY idsesion ASC")
    sesiones = cur.fetchall()
    if (len(sesiones)== 0):
        print("No existen sesiones proximas.")
        MenuAdmin()
        return
    sesIDs = []
    for i in range (0,len(sesiones)):
        sesIDs.append(sesiones[i][0])
    for i in range (0,len(sesiones)):
        print("ID:",sesiones[i][0], ",Instructor:", sesiones[i][1], ",Categoria:", sesiones[i][2], ",Fecha:", sesiones[i][3], ",Hora:", sesiones[i][4], ",Duracion:", sesiones[i][5])
    sesion = input("Ingrese el ID de la sesion que desea eliminar: ")
    if sesion.isnumeric():
        sesion = int(sesion)
        if sesion not in sesIDs:
            print("No ha ingresado un ID valido")
            eliminarSesion()
            return
    else:
        print("No ha ingresado un ID valido")
        eliminarSesion()
        return
    cur.execute("DELETE FROM sesion WHERE idsesion = %s", (sesion,))
    conn.commit()
    print("Sesion eliminada con exito")
    MenuAdmin()
    return

def modificarUsuario():
    print("Modificar usuario")
    cur.execute("SELECT * FROM usuario ORDER BY idusuario ASC")
    usuarios = cur.fetchall()
    usuIDs = []
    for i in range (0,len(usuarios)):
        usuIDs.append(usuarios[i][0])
    for i in range (0,len(usuarios)):
        print("ID:",usuarios[i][0], ",Username:", usuarios[i][1], ",Email:", usuarios[i][3], ",Nombre:", usuarios[i][5], ",Apellido:", usuarios[i][6], ",Fecha Nacimiento:", usuarios[i][7], ",Direccion:", usuarios[i][8], ",Altura:", usuarios[i][9])
    usuario = input("Ingrese el ID del usuario que desea modificar: ")
    if usuario.isnumeric():
        usuario = int(usuario)
        if usuario not in usuIDs:
            print("No ha ingresado un ID valido")
            modificarUsuario()
            return
    else:
        print("No ha ingresado un ID valido")
        modificarUsuario()
        return
    cur.execute("SELECT * FROM usuario WHERE idusuario = %s", (usuario,))
    usu1 = cur.fetchone()
    print("Que desea modificar?")
    print("1. Username")
    print("2. Email")
    print("3. Nombre")
    print("4. Apellido")
    print("5. Fecha de nacimiento")
    print("6. Direccion")
    print("7. Altura")
    print("8. Volver")
    op = input("Ingrese el numero de la opcion: ")
    if op.isnumeric():
        op = int(op)
        if op < 1 or op > 8:
            print("No ha ingresado una opcion valida")
            modificarUsuario()
            return
    else:
        print("No ha ingresado una opcion valida")
        modificarUsuario()
        return
    if op == 1:
        user = input("Ingrese el nuevo usuario: ")
        if usu1[1] == user:
            print("El nombre ingresado es el mismo que el actual")
            modificarUsuario()
            return
        cur.execute("UPDATE usuario SET username = %s WHERE idusuario = %s", (nombre, usuario))
        conn.commit()
        print("Nombre modificado con exito")
        MenuAdmin()
        return
    elif op == 2:
        email = input("Ingrese el nuevo email: ")
        if usu1[3] == email:
            print("El email ingresado es el mismo que el actual")
            modificarUsuario()
            return
        cur.execute("UPDATE usuario SET email = %s WHERE idusuario = %s", (email, usuario))
        conn.commit()
        print("Email modificado con exito")
        MenuAdmin()
        return
    elif op == 3:
        nombre = input("Ingrese el nuevo nombre: ")
        if usu1[5] == nombre:
            print("El nombre ingresado es el mismo que el actual")
            modificarUsuario()
            return
        cur.execute("UPDATE usuario SET nombre = %s WHERE idusuario = %s", (nombre, usuario))
        conn.commit()
        print("Nombre modificado con exito")
        MenuAdmin()
        return
    elif op == 4:
        apellido = input("Ingrese el nuevo apellido: ")
        if usu1[6] == apellido:
            print("El apellido ingresado es el mismo que el actual")
            modificarUsuario()
            return
        cur.execute("UPDATE usuario SET apellido = %s WHERE idusuario = %s", (apellido, usuario))
        conn.commit()
        print("Apellido modificado con exito")
        MenuAdmin()
        return
    elif op == 5:
        fecha = input("Ingrese la nueva fecha de nacimiento (YYYY-MM-DD): ")
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            print("No ha ingresado una fecha valida")
            modificarUsuario()
            return
        if usu1[7] == fecha:
            print("La fecha ingresada es la misma que la actual")
            modificarUsuario()
            return
        cur.execute("UPDATE usuario SET fecha_nacimiento = %s WHERE idusuario = %s", (fecha, usuario))
        conn.commit()
        print("Fecha de nacimiento modificada con exito")
        MenuAdmin()
        return
    elif op == 6:
        direccion = input("Ingrese la nueva direccion: ")
        if usu1[8] == direccion:
            print("La direccion ingresada es la misma que la actual")
            modificarUsuario()
            return
        cur.execute("UPDATE usuario SET direccion = %s WHERE idusuario = %s", (direccion, usuario))
        conn.commit()
        print("Direccion modificada con exito")
        MenuAdmin()
        return
    elif op == 7:
        altura = input("Ingrese la nueva altura: ")
        if usu1[9] == altura:
            print("La altura ingresada es la misma que la actual")
            modificarUsuario()
            return
        cur.execute("UPDATE usuario SET altura = %s WHERE idusuario = %s", (altura, usuario))
        conn.commit()
        print("Altura modificada con exito")
        MenuAdmin()
        return
    elif op == 8:
        MenuAdmin()
        return



def bajaUsuario():
    cur.execute("SELECT * FROM usuario")
    usuarios = cur.fetchall()
    usuIDs = []
    for i in range (0,len(usuarios)):
        usuIDs.append(usuarios[i][0])
    print("Usuarios:")
    for i in range (0,len(usuarios)):
        print("ID:",usuarios[i][0], ",Username:", usuarios[i][1], ",Email:", usuarios[i][3], ",Nombre:", usuarios[i][5], ",Apellido:", usuarios[i][6], ",Fecha Nacimiento:", usuarios[i][7], ",Direccion:", usuarios[i][8], ",Altura:", usuarios[i][9])
    usuario = input("Ingrese el ID del usuario que desea desactivar: ")
    if usuario.isnumeric():
        usuario = int(usuario)
        if usuario not in usuIDs:
            print("No ha ingresado un ID valido")
            bajaUsuario()
            return
    else:
        print("No ha ingresado un ID valido")
        bajaUsuario()
        return
    cur.execute("UPDATE usuario SET activo = 0 WHERE idusuario = %s", (usuario,))
    conn.commit()
    print("Usuario desactivado con exito")
    MenuAdmin()
    return

def reportes():
    print("¿Que reporte desea ver?")
    print("1. Las 10 sesions que mas usuarios tuvieron.\n2. Sesiones y usuarios por categoria\n3. Top 5 entrenadores\n4. Cuentas diamante creadas en los ultimos 6 meses\n5. Hora pico en una fecha especifica\n6. Salir")
    op = input("Ingrese una opcion: ")
    if op.isnumeric():
        op = int(op)
        if op <1 or op >6:
            print("No ha ingresado una opcion valida")
            reportes()
            return
    else:
        print("No ha ingresado una opcion valida")
        reportes()
        return
    if op == 1:
        cur.execute("SELECT s.idsesion, COUNT(*) FROM sesion s, usuariosesion u WHERE s.idsesion = u.idsesion GROUP BY s.idsesion ORDER BY COUNT(*) DESC LIMIT 10")
        sesiones = cur.fetchall()
        print("Las 10 sesiones que mas usuarios tuvieron son:")
        for i in range (0,len(sesiones)):
            print("ID de sesion Sesion:", sesiones[i][0], ",Usuarios:", sesiones[i][1])
        MenuAdmin()
        return
    elif op == 2:
        fecha1 = input("Ingrese la fecha inicial (YYYY-MM-DD): ")
        fecha2 = input("Ingrese la fecha final (YYYY-MM-DD): ")
        hoy = date.today()
        try:
            fecha1valid = datetime.strptime(fecha1, '%Y-%m-%d').date()
            fecha2valid = datetime.strptime(fecha2, '%Y-%m-%d').date()
        except ValueError:
            print("No ha ingresado fechas validas")
            reportes()
            return
        if (fecha1valid >= hoy):
            print("No ha ingresado un intervalo valido.")
            reportes()
            return
        if (fecha2valid > hoy):
            print("No ha ingresado un intervalo valido.")
            reportes()
            return
        if(fecha1valid >= fecha2valid):
            print("No ha ingresado un intervalo valido.")
            reportes()
            return

        cur.execute("SELECT categoria.nombre, count(DISTINCT sesion.idsesion) as cuenta_sesion, count(usuariosesion.idusuario) AS cuenta_usuarios FROM sesion NATURAL JOIN usuariosesion NATURAL JOIN categoria WHERE sesion.fecha >= %s AND sesion.fecha <= %s GROUP BY categoria.nombre ORDER BY cuenta_sesion desc", (fecha1, fecha2))
        categorias = cur.fetchall()
        print("Sesiones y usuarios por categoria:")
        for i in range (0,len(categorias)):
            print("Categoria:", categorias[i][0], ",Cantidad de sesiones:", categorias[i][1], ",Cantidad de usuarios:", categorias[i][2])
        MenuAdmin()
        return
    elif op == 3:
        cur.execute("SELECT instructor.idinstructor, instructor.nombre, instructor.apellido, count(usuariosesion.idusuario) AS cuenta_usuarios FROM sesion NATURAL JOIN usuariosesion NATURAL JOIN instructor GROUP BY instructor.idinstructor, instructor.nombre, instructor.apellido ORDER BY cuenta_usuarios desc LIMIT 5")
        instructores = cur.fetchall()
        print("Top 5 instructores:")
        for i in range (0,len(instructores)):
            print("ID instructor:", instructores[i][0], ",Nombre: ", instructores[i][1], instructores[i][2], ",Cantidad de usuarios que han ido a sus sesiones:", instructores[i][3])
        MenuAdmin()
        return
    elif op == 4:
        cur.execute("SELECT count(*) FROM usuario WHERE suscripcion = 2 AND fechainicio >= (now() - interval '6 months')")
        cuentas = cur.fetchall()
        print("Cantidad de cuentas diamante creadas en los ultimos 6 meses:", cuentas[0][0])
        MenuAdmin()
        return
    elif op == 5:
        fecha = input("Ingrese la fecha en formato YYYY-MM-DD: ")
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            print("No ha ingresado una fecha valida")
            reportes()
            return
        cur.execute("SELECT hora, count(DISTINCT sesion.idsesion) as countsesion, count(usuariosesion.idusuario) as countusuarios FROM sesion NATURAL JOIN usuariosesion WHERE fecha = %s  GROUP BY hora  ORDER BY countusuarios DESC LIMIT 1", (fecha,))
        hora = cur.fetchone()
        if (hora == None):
            print("No hay sesiones registradas este dia.")
            MenuAdmin()
            return
        print("La hora pico en la fecha ingresada es:", hora[0], "con", hora[1], "sesiones y", hora[2], "usuarios")
        MenuAdmin()
        return
    elif op == 6:
        MenuAdmin()
        return


def crearAdmin():
    print("Ingrese los datos del nuevo administrador")
    cur.execute("SELECT idUsuario FROM Usuario ORDER BY idUsuario DESC LIMIT 1")
    newID = cur.fetchone()[0] + 1
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    fechanac = input("Fecha de nacimiento en formato YYYY-MM-DD: ")
    try:
        datetime.strptime(fechanac, '%Y-%m-%d')
    except ValueError:
        print("No ha ingresado una fecha valida")
        crearAdmin()
        return
    direccion = input("Direccion: ")
    cur.execute("INSERT INTO usuario (idusuario, username, userpassword, email, activo, nombre, apellido, fechanacimiento, direccion, clasificacion, fechainicio) VALUES (%s, %s, %s, %s, '1', %s, %s, %s, %s, '1', CURRENT_DATE)",
    (newID, username, password, email, nombre, apellido, fechanac, direccion))
    conn.commit()
    print("Administrador creado con exito")
    MenuAdmin()
    return



# -------------------------------- COMIENZO DEL PROGRAMA -------------------------------- #

main()
