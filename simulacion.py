#Programa para simular sesiones de actividad
#Grupo 4:
#Juan Miguel González-Campo Asturias 21077
#Paulo Raul Sánchez González 21401
#Pedro Javier Marroquín Abrego 21801

import psycopg2 as pg2
import sys
from datetime import date
from datetime import datetime
import random

def simular(fecha, usuarios, conn, cur):
    #usuarios debe ser un múltiplo de 5

    #parte 1, crear nuevas Sesiones
    fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    cur.execute("SELECT * FROM instructor WHERE activo = true")
    instructores = cur.fetchall()
    simInstructores = []#obtener 5 instructores para las 5 sesiones que se simularán

    for i in range(0,5):
        ins = random.randint(0, len(instructores)-1)
        simInstructores.append(instructores[ins][0])#de esta forma se asegura que en verdad se guarde su idinstructor en caso algún instructor esté inactivo

    cur.execute("SELECT * FROM categoria")
    categorias = cur.fetchall()
    simCategorias = [] #Obtener 5 categorías

    for i in range(0,5):
        cat = random.randint(1,len(categorias))
        simCategorias.append(cat)

    horas = ["13:00:00", "14:00:00", "15:00:00", "16:00:00", "17:00:00"]
    duraciones = [30, 60]
    simDuraciones = []#obtener 5 duraciones
    for i in range(0,5):
        dur = random.randint(0,1)
        simDuraciones.append(duraciones[dur])


    #guardar las sesiones para que se inscriban usuarios posteriormente
    sesiones = []
    for i in range(0,5):
        cur.execute("SELECT idsesion FROM sesion ORDER BY idsesion DESC LIMIT 1")
        idsesion = cur.fetchone()[0]+1#tiene que ser un nuevo número de sesion cada iteración
        #posteriormente se inserta la sesion nueva en la tabla de sesiones
        cur.execute("INSERT INTO sesion(idsesion, idinstructor, idcategoria, fecha, hora, duracion) VALUES(%s,%s,%s,%s,%s,%s)", (idsesion, simInstructores[i],simCategorias[i],fecha, horas[i], simDuraciones[i]))
        conn.commit()
        #se guarda la sesion actual usuarios/5 veces para sus usuario/5 participantes participantes
        for j in range(0, int(usuarios/5)):
            sesiones.append(idsesion)




    #parte 2 inscripción y actividad de usuarios en estas 5 sesiones creadas
    cur.execute("SELECT idUsuario FROM usuario WHERE activo = true AND clasificacion = false")
    usrlist = cur.fetchall()
    allusrs = []
    usrSimulacion = []#se obtiene la cantidad de usuarios para los cuales se desea simular actividades
    for i in range(0, len(usrlist)):
        allusrs.append(usrlist[i][0])

    usrSimulacion = random.sample(allusrs, usuarios)

    ritmosSimulados = [] #se simulan los ritmos cardíacos para cada usuario durante su actividad
    for i in range(0, usuarios):
        ritmo = random.randint(145,160)
        ritmosSimulados.append(ritmo)

    caloriasSimuladas = []#se simulan las calorías quemadas durante la sesión
    for i in range(0, usuarios):
        calorias = random.randint(200,300)
        caloriasSimuladas.append(calorias)

    for i in range(0, usuarios):
        cur.execute("INSERT INTO usuariosesion(idusuario, idsesion, calorias, latidos) VALUES(%s,%s,%s,%s)", (usrSimulacion[i],sesiones[i], caloriasSimuladas[i], ritmosSimulados[i]))
        conn.commit()

    QUERY_sesiones = """SELECT usuario.nombre, usuario.apellido, sesion.fecha, categoria.nombre, instructor.nombre, instructor.apellido, usuariosesion.calorias, sesion.duracion, usuariosesion.latidos FROM usuariosesion
    LEFT JOIN usuario ON usuario.idusuario = usuariosesion.idusuario
    LEFT JOIN sesion ON sesion.idsesion = usuariosesion.idsesion
    LEFT JOIN categoria ON sesion.idcategoria = categoria.idcategoria
    LEFT JOIN instructor on sesion.idinstructor = instructor.idinstructor
    ORDER BY (usuariosesion.idsesion) DESC LIMIT %s"""
    cur.execute(QUERY_sesiones, (usuarios,))

    justSimulated = cur.fetchall()
    for i in range(0, usuarios):
        print("En la fecha "+str(justSimulated[i][2])+", el usuario "+str(justSimulated[i][0])+" "+str(justSimulated[i][1])+" tuvo una sesion de "+str(justSimulated[i][3])+" con el instructor "+str(justSimulated[i][4])+" "+str(justSimulated[i][5])+" en la cual quemo "+str(justSimulated[i][6])+" calorias, durante "+str(justSimulated[i][7])+" minutos, y su ritmo cardiaco fue de "+str(justSimulated[i][8])+" latidos por minuto.")

    print("Simulación exitosa.")
    return

conn = pg2.connect("host=localhost dbname=Proyecto2G4 user=postgres password=Itachi1104!")
cur = conn.cursor()
simular('2022-11-19',5,conn,cur)
