SELECT * FROM USUARIO

select * from sesion


-- query para ver las horas totales que tenemos hasta el momento
SELECT sum(sesion.duracion)/60 as horastotales
FROM usuariosesion LEFT JOIN sesion ON sesion.idsesion = usuariosesion.idsesion



--reporteria

-- sesiones que mas usuarios tuvieron en cada hora entre 9am y 6pm para un día dado

SELECT s.idsesion, COUNT(*) FROM sesion s, usuariosesion u WHERE s.idsesion = u.idsesion AND s.fecha = %s AND s.hora='9:00:00' GROUP BY s.idsesion ORDER BY COUNT(*) DESC LIMIT 5




SELECT instructor.idinstructor, instructor.nombre, instructor.apellido, count(usuariosesion.idusuario) AS cuenta_usuarios,  EXTRACT(WEEK FROM sesion.fecha) AS semana FROM sesion NATURAL JOIN usuariosesion NATURAL JOIN instructor WHERE EXTRACT(WEEK FROM sesion.fecha) = EXTRACT(WEEK FROM DATE %S) GROUP BY instructor.idinstructor, instructor.nombre, instructor.apellido, semana ORDER BY cuenta_usuarios desc LIMIT 5