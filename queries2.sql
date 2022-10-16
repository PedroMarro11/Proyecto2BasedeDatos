SELECT * FROM CATEGORIA

SELECT * FROM USUARIO
INSERT INTO categoria (idcategoria, nombre)
VALUES (1, 'Cardio'), (2, 'Aerobicos'), (3, 'Spinnning'), (4, 'Pesas')

SELECT * FROM INSTRUCTOR

INSERT INTO instructor (idinstructor, nombre, apellido, activo, fechainicio)
VALUES (1, 'Juan', 'Perez', '1', CURRENT_DATE), (2, 'Jose', 'Perez', '1', CURRENT_DATE), (3, 'Juan', 'Gonzalez', '1', CURRENT_DATE), (4, 'Maria', 'Sanchez', '1', CURRENT_DATE)

select * from sesion

INSERT INTO sesion (idsesion, idinstructor, idcategoria, fecha, hora, duracion)
VALUES (4, 2, 1, '2022-10-14', '15:00:00', '30'), (5, 2, 2, '2022-10-13', '11:00:00', '60'), (6, 3, 1, '2022-10-12', '7:00:00', '30')

SELECT * FROM usuariosesion


SELECT sesion.idsesion, inst.nombre as nombre, inst.apellido as apellido, cat.nombre as categoria, fecha, hora, duracion
FROM sesion
    LEFT JOIN usuariosesion as usr ON sesion.idsesion = usr.idsesion
    LEFT JOIN instructor as inst ON sesion.idinstructor = inst.idinstructor
    LEFT JOIN categoria as cat ON sesion.idcategoria = cat.idcategoria
WHERE usr.idusuario = 2 AND fecha < CURRENT_DATE
ORDER BY fecha asc, hora asc
    
INSERT INTO usuariosesion (idusuario, idsesion)
VALUES (2, 5), (2,4), (2,6)

SELECT max(pesoactual), min(pesoactual), avg(pesoactual) FROM registro WHERE idusuario = 2

INSERT INTO registro (idusuario, calorias, pesoactual, fecha)
VALUES (2, 2300, 140, '2022-10-1'), (2, 1950, 138, '2022-10-2')

SELECT * FROM instructor

UPDATE instructor SET activo = '1', fechafinal = NULL, fechainicio = CURRENT_DATE WHERE idinstructor = 1

UPDATE instructor SET activo = '0', fechafinal = CURRENT_DATE WHERE idinstructor = 1


alter table usuariosesion
    DROP CONSTRAINT fk_sesion,
    ADD CONSTRAINT fk_sesion
        FOREIGN KEY (idsesion)
            REFERENCES sesion (idsesion) ON DELETE CASCADE
            
SELECT s.idsesion, COUNT(*) FROM sesion s, usuariosesion u WHERE s.idsesion = u.idsesion GROUP BY s.idsesion ORDER BY COUNT(*) DESC LIMIT 10

INSERT INTO usuariosesion (idsesion, idusuario)
VALUES (5, 3)

SELECT categoria.nombre, count(DISTINCT sesion.idsesion) as cuenta_sesion, count(usuariosesion.idusuario) AS cuenta_usuarios
FROM sesion 
    NATURAL JOIN usuariosesion
    NATURAL JOIN categoria
GROUP BY categoria.nombre
ORDER BY cuenta_sesion desc

SELECT instructor.idinstructor, instructor.nombre, instructor.apellido, count(usuariosesion.idusuario) AS cuenta_usuarios 
FROM sesion 
    NATURAL JOIN usuariosesion 
    NATURAL JOIN instructor 
GROUP BY instructor.idinstructor, instructor.nombre, instructor.apellido
ORDER BY cuenta_usuarios desc LIMIT 5

SELECT count(*)
FROM usuario
WHERE suscripcion = 2 AND fechainicio >= (now() - interval '6 months')

SELECT hora, count(DISTINCT sesion.idsesion) as countsesion, count(usuariosesion.idusuario) as countusuarios
FROM sesion NATURAL JOIN usuariosesion
WHERE fecha = %s 
GROUP BY hora 
ORDER BY countusuarios DESC LIMIT 1