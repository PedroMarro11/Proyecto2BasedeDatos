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

