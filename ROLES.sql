

CREATE GROUP adminadmin;
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
GRANT INSERT ON bitacora TO adminusuarios, adminsesiones, adminadmin, admininstructores, adminreportes;

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

SELECT * FROM PG_ROLES;

