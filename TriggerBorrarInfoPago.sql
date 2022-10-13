DROP FUNCTION borrarInfoPago()

CREATE FUNCTION borrarInfoPago()
RETURNS TRIGGER AS $$
DECLARE idborrar INT;
DECLARE checkactivo Boolean;
BEGIN

    SELECT idusuario INTO idborrar
    FROM usuario
    WHERE idusuario = old.idusuario;
    
    SELECT activo INTO checkactivo
    FROM usuario
    WHERE idusuario = old.idusuario;
    
    IF (checkactivo is false) THEN
        DELETE FROM infopago
        WHERE idusuario = idborrar;
    END IF;
    RETURN NEW;
END;
$$ Language PLPGSQL;

DROP TRIGGER desactivarcuenta ON usuario

CREATE TRIGGER desactivarcuenta
AFTER UPDATE
ON usuario
FOR EACH ROW
    EXECUTE PROCEDURE borrarInfoPago();
