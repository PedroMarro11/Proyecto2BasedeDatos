

CREATE OR REPLACE FUNCTION crearSmartwatch ()
RETURNS TRIGGER AS $$
DECLARE 
    idsmart INT;
BEGIN 
   
    IF new.clasificacion = '0' THEN 
        SELECT idusuario INTO idsmart
        FROM usuario
        WHERE idusuario = new.idusuario;

        INSERT INTO smartwatch (idsmartwatch, idusuario) VALUES (idsmart, new.idusuario);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;


CREATE or replace TRIGGER crearSmartwatch
AFTER INSERT 
ON usuario
    FOR EACH ROW EXECUTE PROCEDURE crearSmartwatch();
    
UPDATE usuario
SET activo = '1';

SELECT * FROM USUARIO
SELECT * from smartwatch

DELETE FROM smartwatch where idusuario = 9 or idusuario = 8 or idusuario = 1
