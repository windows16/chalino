CREATE OR REPLACE PROCEDURE llenar_cuotas(codvehiculo NUMBER)
AS
    abono NUMBER;
    precio_vehiculo NUMBER;
    id_venta NUMBER;
    fechav DATE;
    cuota NUMBER;
    estado vehiculo.id_estado%TYPE;
BEGIN
    -- Obtener el estado del vehículo
    SELECT id_estado INTO estado FROM vehiculo WHERE id_vehiculo = codvehiculo;
     -- Verificar el estado del vehículo
    IF estado = 1 THEN
        DBMS_OUTPUT.PUT_LINE('El vehículo ya está vendido.');
        RETURN;
    END IF;
    -- Obtener el ID de la venta asociada al vehículo
    SELECT id_venta, cuotas, fechaventa INTO id_venta, cuota, fechav FROM venta WHERE id_vehiculo = codvehiculo;

    SELECT precio_venta into precio_vehiculo FROM vehiculo WHERE id_vehiculo = codvehiculo;
    -- Calcular el monto de cada cuota
    abono := precio_vehiculo / cuota;

    -- Generar cuotas
    WHILE cuota > 0 LOOP
        INSERT INTO ventacuotas (id_ventacuotas, id_venta, fecha_de_abono, cuota_de_abono)
        VALUES (
            NVL((SELECT MAX(id_ventacuotas) FROM ventacuotas), 0) + 1,
            id_venta,
            fechav,
            abono
        );
        -- Incrementar la fecha y reducir el contador de cuotas
        fechav := fechav + 30;
        cuota := cuota - 1;
    END LOOP;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No se encontró información para el vehículo.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Ocurrió un error: ' || SQLERRM);
END;
/

/*Realizar un procedimiento que calcule el costo total y también actualice el precio de venta 
del vehículo agregándole un 60% de ganancia. Tome en cuenta los costos de importaciones para 
calcular el costo total, también que cambie el estado del vehículo a disponible para la venta 
una vez terminados los costos, esto es solo para los vehículos que estén en reparación.*/

CREATE or REPLACE PROCEDURE costo_total(no_vehiculo vehiculo.id_vehiculo%type) 
as
estado_vehiculo estado.ESTADO%type;
id_import  importacion.id_importacion%type;
total importacion.COSTOTOTAL%TYPE;
res VARCHAR2(255);
begin
  select es.estado into estado_vehiculo from vehiculo ve, estado es 
    where ve.id_estado=es.id_estado and id_vehiculo=no_vehiculo;
if estado_vehiculo = 'reparacion' THEN
    select id_importacion into id_import from importacion where id_vehiculo=no_vehiculo;
    select costotraidaquetzal+impuestos+tramites+placas+otrosgastos into total
      from IMPORTACIONCOSTOS where id_importacion=id_import;
    update IMPORTACION set COSTOTOTAL=total where ID_IMPORTACION=id_import;
    UPDATE VEHICULO set PRECIO_VENTA=PRECIO_VENTA+PRECIO_VENTA*0.6 where ID_VEHICULO=no_vehiculo;
    update VEHICULO set id_estado=(SELECT id_estado from estado where estado='disponible') 
      where ID_VEHICULO=no_vehiculo;
    select ' costo total vehiculo '||no_vehiculo||' : '||costototal||
      ' precio de venta : '||precio_venta||' estado:'||id_estado
          into res from VEHICULO,IMPORTACION 
            WHERE VEHICULO.ID_VEHICULO=no_vehiculo and IMPORTACION.ID_VEHICULO=no_vehiculo;
    dbms_output.put_line(res);
else dbms_output.put_line(' no se puede calcular el costo total');
end if;
end;
/

  EXECUTE costo_total(1);


CREATE OR REPLACE PROCEDURE insertar_vehiculo(
 p_placa  VEHICULO.placa%TYPE,
 p_color  VEHICULO.color%TYPE,
 p_id_marca  VEHICULO.id_marca%TYPE,
 p_id_estado  VEHICULO.id_estado%TYPE,
 p_precio_venta  VEHICULO.precio_venta%TYPE
) AS
BEGIN
    INSERT INTO VEHICULO (id_vehiculo,placa, color, id_marca, id_estado, precio_venta)
    VALUES ((select max(id_vehiculo) from vehiculo) + 1,p_placa, p_color, p_id_marca, p_id_estado, p_precio_venta);
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        -- Manejo de errores
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20001, 'Error al insertar el vehículo: ' || SQLERRM);
END insertar_vehiculo;
/














    








