--funcion reporte 2 proyecto 3
CREATE OR REPLACE FUNCTION topinstructoressemana (fechaparam DATE)
    RETURNS TABLE (
        idinstructor INT,
        nombre VARCHAR(120),
        apellido VARCHAR(120),
        cuentaUsuarios BIGINT,
        semana NUMERIC
    ) AS $$

        BEGIN
            RETURN QUERY SELECT 
                instructor.idinstructor, instructor.nombre, instructor.apellido, count(usuariosesion.idusuario) AS cuenta_usuarios,  EXTRACT(WEEK FROM sesion.fecha) AS semana
                FROM sesion NATURAL JOIN usuariosesion NATURAL JOIN instructor
                WHERE EXTRACT(WEEK FROM sesion.fecha) = EXTRACT(WEEK FROM fechaparam)
                GROUP BY instructor.idinstructor, instructor.nombre, instructor.apellido, semana ORDER BY
                cuenta_usuarios desc LIMIT 5;
            END; $$
            LANGUAGE plpgsql;
            
-- funcion reporte 1 proyecto 3

CREATE OR REPLACE FUNCTION top5sesionesdiahora(fechaparam DATE, horaparam TIME)
    RETURNS TABLE (
        idsesion INT,
        usuarios BIGINT
    ) AS $$
        BEGIN
            RETURN QUERY SELECT
            s.idsesion, COUNT(*) 
            FROM sesion s, usuariosesion u 
            WHERE s.idsesion = u.idsesion AND s.fecha = fechaparam AND s.hora=horaparam
            GROUP BY s.idsesion 
            ORDER BY COUNT(*) DESC 
            LIMIT 5;
        END; $$
        LANGUAGE plpgsql;
        
    
-- fucntion report 3 proyecto 3

CREATE OR REPLACE FUNCTION top5adminscambios(fechainiparam DATE, fechafinparam DATE)
    RETURNS TABLE (
        administrador NAME,
        cambios BIGINT
    ) AS $$
        BEGIN
            RETURN QUERY SELECT
            adminname, COUNT(cambioid) 
            FROM bitacora 
            WHERE fecha >= fechainiparam AND fecha <= fechafinparam 
            GROUP BY adminname 
            ORDER BY COUNT(cambioid) DESC 
            LIMIT 5;
        END; $$
        LANGUAGE plpgsql;

DROP FUNCTION top5adminscambios

SELECT * FROM top5adminscambios('2022-11-20', '2022-11-21')

SELECT adminname, COUNT(cambioid) FROM bitacora WHERE fecha >= '2022-11-20' AND fecha <= '2022-11-21' GROUP BY adminname ORDER BY COUNT(cambioid) DESC LIMIT 5


-- FUNCION 4 PROYECTO 3

-- query
SELECT usuario.idusuario, usuario.username, max(sesion.fecha)
FROM usuariosesion NATURAL JOIN usuario NATURAL JOIN sesion
GROUP BY usuario.idusuario, usuario.username
HAVING max(sesion.fecha) <= (now() - interval '3 weeks')
ORDER BY max(sesion.fecha) desc
LIMIT 20

CREATE OR REPLACE FUNCTION top20usuarios3semanas()
    RETURNS TABLE (
        usuarioid INT,
        usuariousername varchar(12),
        lastexercise DATE
    ) AS $$
        BEGIN
            RETURN QUERY SELECT
            usuario.idusuario, usuario.username, max(sesion.fecha)
            FROM usuariosesion NATURAL JOIN usuario NATURAL JOIN sesion
            GROUP BY usuario.idusuario, usuario.username
            HAVING max(sesion.fecha) <= (now() - interval '3 weeks')
            ORDER BY max(sesion.fecha) desc
            LIMIT 20;
        END; $$
        LANGUAGE plpgsql;
     
SELECT * FROM top20usuarios3semanas();
