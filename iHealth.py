#Programa que corre la aplicación de iHealth
#Grupo 4:
#Juan Miguel González-Campo Asturias 21077
#Paulo Raul Sánchez González 21401
#Pedro Javier Marroquín Abrego 21801
import sys
import psycopg2 as pg2

def main():
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
    print("""1. Continuar
2. Regresar a Inicio""")
    opc = input("Ingrese su eleccion: ")
    if opc == "1":
        usr = input("Ingrese su usuario: ")
        #vrfusr = #sacar usuario de BDS en forma de Booleano
        #if vrfusr == True:
            #vrfpswd = #obtener su password guardado
            #clasificacion = #obtener si es cliente o admin
            #try = True
            #while(try):
                #pswd = input("Ingrese su password: ")
                #if pswd == vrfpswd:
                    #if clasificacion == "Cliente":
                        #MenuCliente()
                    #elif clasificacion == "Admin":
                        #MenuAdmin()
                #else:
                    #lp = True
                    #while lp:
                        #retry = input("Password incorrecto, intentar nuevamente (1) o regresar (2): ")
                        #if retry == "1":
                            #lp = False
                        #elif: retry == "2":
                            #SignIn()
                        #else:
                            #continue
                    
    elif opc == "2":
        main()
    else:
        print("No ha marcado una opcion valida")
        SignIn()
def Register():
    print("""1. Continuar
2. Regresar a Inicio""")
    opc = input("Ingrese su eleccion: ")
    if opc == "1":
        usr = input("Ingrese su usuario: ")
        pswd = input("Ingrese su password: ")
        email = input("Ingrese su email: ")
    elif opc == "2":
        main()
    else:
        print("No ha marcado una opcion valida")
        Register()

def MenuCliente():
    return

def MenuAdmin():
    return
main()
