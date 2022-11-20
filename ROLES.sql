

CREATE GROUP adminadmin SUPERUSER;
CREATE GROUP adminusuarios;
CREATE GROUP adminsesiones;
CREATE GROUP admininstructores;
CREATE GROUP adminreportes;

GRANT ALL PRIVILEGES on usuario TO adminusuarios;
GRANT ALL PRIVILEGES on sesion, usuariosesion TO adminsesiones;
GRANT ALL PRIVILEGES on instructor, nutricionista, consulta TO admininstructores;
GRANT SELECT on instructor, categoria TO adminsesiones;
GRANT SELECT on usuariosesion, sesion, categoria, instructor, usuario, bitacora TO adminreportes;
GRANT ALL PRIVILEGES ON categoria, bitacora, consulta, infopago, instructor, nutricionista, registro, sesion, smartwatch, usuario, usuariosesion TO adminadmin;
GRANT INSERT, SELECT ON bitacora TO adminusuarios, adminsesiones, adminadmin, admininstructores, adminreportes;
GRANT ALL PRIVILEGES ON adminClasificaciones TO adminadmin;
GRANT DELETE, SELECT ON infopago TO adminusuarios; 
GRANT SELECT ON usuario TO adminsesiones;

DROP OWNED by adminadmin;
DROP OWNED by adminusuarios;
DROP OWNED by adminsesiones;
DROP OWNED by admininstructores;
DROP OWNED by adminreportes;

DROP GROUP adminadmin;
DROP GROUP adminusuarios;
DROP GROUP adminsesiones;
DROP GROUP admininstructores;
DROP GROUP adminreportes;

drop user admin1;
drop user adminprueba;
CREATE USER admin1 WITH PASSWORD 'admin' IN GROUP adminadmin SUPERUSER;
CREATE USER adminprueba WITH PASSWORD 'hola' IN GROUP adminadmin SUPERUSER;

SELECT * FROM PG_ROLES;


