#Programa que corre la aplicación de iHealth
#Grupo 4:
#Juan Miguel González-Campo Asturias 21077
#Paulo Raul Sánchez González 21401
#Pedro Javier Marroquín Abrego 21801
from re import I
import sys
import psycopg2 as pg2
import getpass

conn = pg2.connect(host="localhost",database="Proyecto2G4",user="postgres",password="murcielago122")
cur = conn.cursor()


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
    elif opc == "2":
        Register()
    else:
        sys.exit()



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
            else:
                MenuCliente(usrID)
        else:
            print("\nUsuario o contrasena incorrectos")
            SignIn()
                    
    elif opc == "2":
        main()
    else:
        print("No ha marcado una opcion valida\n")
        SignIn()



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
        #Se piden los datos del nuevo usuario
        usr = input("Ingrese su usuario: ")
        usr = usr.lower()
        #verifica que este nombre de usuario no haya sido registrado
        cur.execute("SELECT * FROM Usuario WHERE username = %s", (usr,))
        if cur.rowcount == 1:
            print("Este usuario ya existe")
            Register()

        pswd = getpass.getpass("Ingrese su password (sensible a casos): ")
        pswd2 = getpass.getpass("Confirme su password (sensible a casos): ")
        #Verifica que las contraseñas sean iguales
        if pswd != pswd2:
            print("Las contrasenas no coinciden")
            Register()
        
        #Se inserta ID generado, datos de usuario, clasificacion de usuario
        cur.execute("INSERT INTO Usuario (idusuario, username, userpassword, email, activo, clasificacion, fechainicio) VALUES (%s, %s, %s, %s, '0','0',CURRENT_DATE)", (newID, usr, pswd, email))
        conn.commit()
        print("Usuario registrado con exito")
        main()
    elif opc == "2":
        main()
    else:
        print("No ha marcado una opcion valida\n")
        Register()

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
        else:
            main()
    #Revisa si el usuario es nuevo
    if nombre is None:
        ingresoDatosCliente(usrID)
        
    print("¿Que desea hacer?\n1.")
    return

def MenuAdmin(usrID):
    print("\n\nMENU ADMINISTRADOR")

    return

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

    cur.execute("UPDATE Usuario SET nombre = %s, apellido = %s, fechanacimiento = %s, altura = %s, direccion = %s WHERE idusuario = %s", (nombre, apellido, fechaNac, estatura, direccion, usrID))
    conn.commit()
    print("Perfil actualizado con exito")
    return True

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
            print("Nombre en Tarjeta (incluido apellido): ")
            nombre = input()

            cur.execute("INSERT INTO infopago (idusuario, numtarjeta, nombretarjeta) VALUES (%s, %s, %s)", (usrID, tarjeta, nombre))
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
            if op3 == "2":
                print("Sentimos que no haya podido realizar el pago ahora, su cuenta se encuentra inactiva")
                cur.execute("UPDATE Usuario SET activo = '0', suscripcion = NULL WHERE idusuario = %s", (usrID,))
                MenuCliente(usrID)
            else:
                print("No ha marcado una opcion valida")
                activarCuenta(usrID)
        else:
            activarCuenta(usrID)
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
            print("Nombre en Tarjeta (incluido apellido): ")
            nombre = input()

            cur.execute("INSERT INTO infopago (idusuario, numtarjeta, nombretarjeta) VALUES (%s, %s, %s)", (usrID, tarjeta, nombre))
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
            if op3 == "2":
                print("Sentimos que no haya podido realizar el pago ahora, su cuenta se encuentra inactiva")
                cur.execute("UPDATE Usuario SET activo = '0' WHERE idusuario = %s", (usrID,))
                conn.commit()
                MenuCliente(usrID)
            else:
                print("No ha marcado una opcion valida")
                activarCuenta(usrID)
        else:
            activarCuenta(usrID)
    elif op == "3":
        print("Su cuenta se mantendra inactiva")
        MenuCliente(usrID)
    else:
        print("No ha marcado una opcion valida")
        activarCuenta(usrID)


main()
