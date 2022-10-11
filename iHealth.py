#Programa que corre la aplicación de iHealth
#Grupo 4:
#Juan Miguel González-Campo Asturias 21077
#Paulo Raul Sánchez González 21401
#Pedro Javier Marroquín Abrego 21801
import sys
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
    return
def Register():
    return
main()
