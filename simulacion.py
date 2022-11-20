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
    #parte 1, crear nuevas Sesiones
    fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    cur.execute("SELECT * FROM instructor WHERE activo = true")
    instructores = cur.fetchall()
    simInstructores = []#obtener 5 instructores para las 5 sesiones que se simularán

    for i in range(0,5):
        ins = random.randint(1, len(intructores))
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

    for i in range(0,5):
        cur.execute("SELECT idsesion FROM sesion ORDER BY idsesion DESC LIMIT 1")
        idsesion = cur.fetchone()[0]+1#tiene que ser un nuevo número de sesion cada iteración
        cur.execute("INSERT INTO sesion(idsesion, idinstructor, idcategoria, fecha, hora, duracion) VALUES(%s,%s,%s,%s,%s,%s)", (idsesion, simInstructores[i],simCategorias[i],fecha, horas[i], simDuraciones[i]))
        conn.commit()

    #parte 2 inscripción y actividad de usuarios en estas 5 sesiones creadas
    
    print("Simulación exitosa.")
        return
