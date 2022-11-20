CREATE TABLE adminClasificaciones (
    clasifID INT,
    descripcion VARCHAR(30)
);


insert into adminClasificaciones (clasifID, descripcion) VALUES (1, 'adminadmin'), (2, 'adminusuarios'), (3, 'admininstructores'), (4, 'adminsesiones'), (5, 'adminreportes');

ALTER TABLE usuario 
ADD COLUMN adminClasif INT;


CREATE OR REPLACE FUNCTION nuevoAdmin()
RETURNS TRIGGER AS $$
DECLARE
    usernombre VARCHAR(12);
    userpass VARCHAR(12);
BEGIN

    usernombre = new.username;
    userpass = new.userpassword;
    
    IF new.clasificacion = '1' THEN
        IF new.adminClasif = 1 THEN
            
            execute 'CREATE USER ' || QUOTE_IDENT(usernombre) || ' WITH PASSWORD ' || QUOTE_literal(userpass) || ' IN GROUP adminadmin';
        END IF;
        IF new.adminClasif = 2 THEN
            execute 'CREATE USER ' || QUOTE_IDENT(usernombre) || ' WITH PASSWORD ' || QUOTE_literal(userpass) || ' IN GROUP admiusuarios';
        END IF;
        IF new.adminClasif = 3 THEN
            execute 'CREATE USER ' || QUOTE_IDENT(usernombre) || ' WITH PASSWORD ' || QUOTE_literal(userpass) || ' IN GROUP admininstructores';
        END IF;
        IF new.adminClasif = 4 THEN
            execute 'CREATE USER ' || QUOTE_IDENT(usernombre) || ' WITH PASSWORD ' || QUOTE_literal(userpass) || ' IN GROUP adminsesiones';
        END IF;
        IF new.adminClasif = 5 THEN
            execute 'CREATE USER ' || QUOTE_IDENT(usernombre) || ' WITH PASSWORD ' || QUOTE_literal(userpass) || ' IN GROUP adminreportes';
        END IF;
    END IF;
    
    RETURN NEW;
    
END;
$$ LANGUAGE PLPGSQL;


CREATE OR REPLACE TRIGGER nuevoAdmin
AFTER INSERT 
ON usuario
    FOR EACH ROW EXECUTE FUNCTION nuevoAdmin();
    
SELECT * FROM usuario
    
INSERT INTO usuario (idusuario, username, userpassword, email, activo, nombre, apellido, fechanacimiento, direccion, clasificacion, fechainicio, adminclasif) 
VALUES (9, 'adminprueba', 'hola', 'prueba', '1','prueba','prueba',CURRENT_DATE,'prueba','1',CURRENT_DATE,1)



SELECT * FROM PG_ROLES;
    