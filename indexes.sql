
-- indexes bitacora
CREATE INDEX bitacora_fecha ON bitacora(fecha);
CREATE INDEX bitacora_hora ON bitacora(hora);
CREATE INDEX bitacora_fecha_admin ON bitacora (fecha, adminname);
CREATE INDEX bitacora_hora_admin ON bitacora (hora, adminname);
CREATE INDEX bitacora_adminname ON bitacora (adminname);

-- indexes infopago
CREATE INDEX infopago_idusuario ON infopago (idusuario);

-- indexes instructor
CREATE INDEX instructor_idinstructor ON instructor(idinstructor);
CREATE INDEX instructor_nombre ON instructor(nombre);
CREATE INDEX instructor_apellido ON instructor(apellido);

--indexes registro
CREATE INDEX registro_idusuario ON registro(idusuario);
CREATE INDEX registro_fecha ON registro(fecha);

--indexes sesion
CREATE INDEX sesion_idsesion ON sesion (idsesion);
CREATE INDEX sesion_idcategoria ON sesion (idcategoria);
CREATE INDEX sesion_idinstructor ON sesion (idinstructor);
CREATE INDEX sesion_fecha ON sesion(fecha);
CREATE INDEX sesion_hora ON sesion(hora);

-- indexes usuario
CREATE INDEX usuario_idusuario ON usuario(idusuario);
CREATE INDEX usuario_username ON usuario(username);
CREATE INDEX usuario_nombre ON usuario(nombre);
CREATE INDEX usuario_apellido ON usuario (apellido);
CREATE INDEX usuario_nombre_apellido ON usuario (nombre, apellido);
CREATE INDEX usuario_fechaNacimiento ON usuario (fechanacimiento);
CREATE INDEX usuario_fechaInicio ON USUARIO (FECHAINICIO);

--indexes usuario sesion
CREATE INDEX usuariosesion_idusuario ON usuariosesion (idusuario);
CREATE INDEX usuariosesion_idsesion ON usuariosesion (idsesion);
