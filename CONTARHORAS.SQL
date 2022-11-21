

SELECT SUM(sesion.duracion)/60 FROM usuariosesion LEFT JOIN sesion ON usuariosesion.idsesion = sesion.idsesion

SELECT COUNT(*) FROM usuario WHERE CLASIFICACION = '0'
