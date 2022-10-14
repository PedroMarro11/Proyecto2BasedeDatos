#Programa que corre la aplicación de iHealth
#Grupo 4:
#Juan Miguel González-Campo Asturias 21077
#Paulo Raul Sánchez González 21401
#Pedro Javier Marroquín Abrego 21801
from re import I
import sys
import psycopg2 as pg2
import getpass
import funciones as f

conn = pg2.connect(host="localhost",database="Proyecto2G4",user="postgres",password="murcielago122")
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
            print("Usuario ", usrID)
            print("Bienvenido " + usr)
            #Se obtiene la clasificacion del usuario
            cur.execute("SELECT clasificacion FROM Usuario WHERE idusuario = %s", (int(usrID),))
            clasif = cur.fetchone()[0]

            #Se envia al usuario al menu correspondiente
            if clasif:
                MenuAdmin(usrID)
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
    print(infoUsr)
    nombre = infoUsr[5]
    #Revisa si la cuenta se encuentra activa
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
        
    print("¿Que desea hacer?\n1.Registro diario\n2. Ver y agregar sesiones\n3. Salir")
    op1 = input()
    if op1 == "1":
        cur.execute("SELECT fecha FROM registro WHERE idusuario = %s AND fecha = CURRENT_DATE", (usrID,))
        if cur.rowcount == 1:
            print("Ya ha realizado su registro diario")
            MenuCliente(usrID)
            return
        peso, calorias = f.registroDiario()
        cur.execute("INSERT INTO Registro (idusuario, calorias, pesoactual, fecha) VALUES (%s, %s, %s, CURRENT_DATE)", (usrID, calorias, peso))
        conn.commit()
        MenuCliente(usrID)
        return
    if op1 == "2":
        agregarSesion(usrID)
        return
    if op1 == "3":
        print("Gracias por usar iHealth")
        sys.exit()
    else:
        print("No ha marcado una opcion valida")
        MenuCliente(usrID)
        return
    


def agregarSesion(usrID):
    print("¿Cómo desea buscar la sesion?\n1. fecha \n2. hora\n3. duracion\n4. categoria\n5. instructor\n6. regresar")
    op = input()
    if op == "1":
        fecha = input("Ingrese la fecha de la sesion (YYYY-MM-DD): ")
        #revisar si la fehca es igual o mayor a la actual
        cur.execute("SELECT * FROM sesion WHERE fecha = %s", (fecha,))
        for i in range (cur.rowcount):
            print(i, ".",  cur.fetchone())
            
            
    if op == "2":
        hora = input("Ingrese la hora de la sesion (ingrese solo la hora exacta e.g. ""19"" o ""7""): ")
        hora = hora+":00:00"
        cur.execute("SELECT * FROM sesion WHERE hora = %s", (hora,))
        for i in range (cur.rowcount):
            print(i, ".",  cur.fetchone())
    if op == "3":
        duracion = input("Haga su selección: 1. Sesiones de 30 minutos 2. Sesiones de 1 hora): ")
        if duracion == "1":
            duracion = 30
        elif duracion == "2":
            duracion = 60
        cur.execute("SELECT * FROM sesion WHERE duracion = %s", (duracion,))
        for i in range (cur.rowcount):
            print(i, ".",  cur.fetchone())
    """if op == "4":
        categoria = input("Ingrese la categoria de la sesion: ")
        cur.execute("SELECT * FROM sesion WHERE categoria = %s", (categoria,))
        for i in range (cur.rowcount):
            print(i, ".",  cur.fetchone())"""
    if op == "5":
        instructor = input("Ingrese el nombre (solo nombre propio) del instructor: ")
        #cur.execute("SELECT * FROM sesion WHERE instructor = %s", (instructor,))
        #for i in range (cur.rowcount):
        #    print(i, ".",  cur.fetchone())
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
    


# --------------------------------- MENU ADMINS --------------------------------- #
""" Menu de administrador

:param usrID: ID del usuario que se esta registrando

:return: None
"""
def MenuAdmin(usrID):
    print("\n\nMENU ADMINISTRADOR")

    


# -------------------------------- COMIENZO DEL PROGRAMA -------------------------------- #
main()
