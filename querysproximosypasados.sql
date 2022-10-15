---------Proximas---------------------
select ses.idsesion,ses.idinstructor,ses.fecha,ses.hora,ses.duracion
from sesion as ses 
inner join(
    select* 
    from 
        usuariosesion as us
    inner join sesion as s on us.idsesion=s.idsesion
    inner join usuario as u on us.idusuario=u.idusuario
    where 
        s.fecha>current_date and us.idusuario='1'
) as k
on ses.fecha=k.fecha
order by ses.fecha asc
--mejorado
SELECT s1.idsesion, s1.nombre, s1.apellido, s1.categoria, s1.fecha, EXTRACT(WEEK FROM s1.fecha) as semana, s1.hora, s1.duracion FROM usuariosesion as us
    LEFT JOIN (
        SELECT s.idsesion, ins.nombre, ins.apellido, cat.nombre as categoria, s.fecha, s.hora, s.duracion FROM sesion as s
            LEFT JOIN instructor as ins ON s.idinstructor = ins.idinstructor
            LEFT JOIN categoria as cat ON s.idcategoria = cat.idcategoria)s1
    ON us.idsesion = s1.idsesion
WHERE EXTRACT(WEEK FROM s1.fecha) = EXTRACT(WEEK FROM CURRENT_DATE)
    AND us.idusuario = 1
ORDER BY s1.fecha, s1.hora ASC
--------Pasadas----------
select ses.idsesion,ses.idinstructor,ses.fecha,ses.hora,ses.duracion
from sesion as ses 
inner join(
    select* 
    from 
        usuariosesion as us
    inner join sesion as s on us.idsesion=s.idsesion
    inner join usuario as u on us.idusuario=u.idusuario
    where 
        s.fecha<current_date
) as k
on ses.fecha=k.fecha
order by ses.fecha desc

--mejorado
SELECT s1.idsesion, s1.nombre, s1.apellido, s1.categoria, s1.fecha, EXTRACT(WEEK FROM s1.fecha) as semana, s1.hora, s1.duracion FROM usuariosesion as us
    LEFT JOIN (
        SELECT s.idsesion, ins.nombre, ins.apellido, cat.nombre as categoria, s.fecha, s.hora, s.duracion FROM sesion as s
            LEFT JOIN instructor as ins ON s.idinstructor = ins.idinstructor
            LEFT JOIN categoria as cat ON s.idcategoria = cat.idcategoria)s1
    ON us.idsesion = s1.idsesion
WHERE s1.fecha < CURRENT_DATE
    AND us.idusuario = 1
ORDER BY s1.fecha, s1.hora DESC
