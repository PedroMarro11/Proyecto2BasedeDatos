

CREATE TABLE bitacora (
    cambioID INT,
    tabla TEXT,
    operacion TEXT,
    fecha DATE,
    hora TIME,
    adminName NAME

);


insert into bitacora (cambioID, tabla, operacion, fecha, hora, adminName) VALUES (0, NULL, NULL, NULL, NULL, NULL );

CREATE OR REPLACE FUNCTION bitacoraData ()
RETURNS TRIGGER AS $$
DECLARE 
    categoria TEXT;
    operacion TEXT;
    idcambio INT;
BEGIN 
    categoria = TG_TABLE_NAME;
    operacion = TG_OP;
    
    SELECT cambioID+1 INTO idcambio
    FROM bitacora
    ORDER BY cambioID DESC;
    
    INSERT INTO bitacora (cambioID, tabla, operacion, fecha, hora, adminName) values (idcambio, categoria, operacion, CURRENT_DATE, CURRENT_TIME, CURRENT_USER);
    
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;
    

CREATE TRIGGER bitacoraUs 
AFTER INSERT OR UPDATE OR DELETE
ON usuario
    FOR EACH ROW  EXECUTE FUNCTION bitacoraData ();
    
CREATE TRIGGER bitacoraSes 
AFTER INSERT OR UPDATE OR DELETE
ON sesion
    FOR EACH ROW  EXECUTE FUNCTION bitacoraData ();

CREATE TRIGGER bitacoraIns 
AFTER INSERT OR UPDATE OR DELETE
ON instructor
    FOR EACH ROW  EXECUTE FUNCTION bitacoraData ();

CREATE TRIGGER bitacoraNut 
AFTER INSERT OR UPDATE OR DELETE
ON nutricionista
    FOR EACH ROW  EXECUTE FUNCTION bitacoraData ();
    
CREATE TRIGGER bitacoraUsSes
AFTER INSERT OR UPDATE OR DELETE
ON usuarioSesion
    FOR EACH ROW  EXECUTE FUNCTION bitacoraData ();

CREATE TRIGGER bitacoraCons
AFTER INSERT OR UPDATE OR DELETE
ON consulta
    FOR EACH ROW  EXECUTE FUNCTION bitacoraData ();



INSERT INTO nutricionista (idnutricionista, nombre, apellido, activo, fechainicio) VALUES (1, 'Jose', 'Ortiz', '1', CURRENT_DATE);
    
select * from bitacora;

ALTER TABLE usuario 
ADD CONSTRAINT unicousuario UNIQUE(username);


