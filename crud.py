import oracledb
from flet import*


def main(page: Page):
   
    page.title = "CRUD con Oracle"
    
    # funcion para conectar la base de datos
    def conectar():
        return oracledb.connect(
            user='vehiculos', 
            password='fullsql123', 
            dsn='localhost/XEPDB1',
        )
    

   
    # Función para obtener las opciones de marcas
    def obtener_marcas():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_marca, marca FROM marca")
        marcas = [{"id": row[0], "nombre": row[1]} for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return marcas

    # Función para obtener las opciones de estados
    def obtener_estados():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_estado, estado FROM estado")
        estados = [{"id": row[0], "nombre": row[1]} for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return estados
    
    def registrar_vehiculo():
       
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.callproc('insertar_vehiculo', 
                [placa.value, color.value, int(marca.value), int(estado.value), int(precio_venta.value)])
            conn.commit()
        except Exception as ex:
             page.add(SnackBar(Text(f"Error en los datos {ex}", color=colors.RED),
                 open=True, duration=5000))
        finally:
            page.add(SnackBar(Text("Vehiculo registrado"), open=True, duration=5000))
            cursor.close()
            conn.close()
    
    def limpiar_componentes_vehiculo():
        placa.value = ""
        color.value = ""
        marca.value = ""
        estado.value = ""
        precio_venta.value = ""

    # componentes para registrar un vehiculo
    placa = TextField(label="Placa", border_color=colors.BLUE_GREY_800, width=350)
    color = TextField(label="Color", border_color=colors.BLUE_GREY_800, width=350)
    # Dropdown para seleccionar marca
    marcas = obtener_marcas()
    marca = Dropdown(
        label="Marca", border_color=colors.BLUE_GREY_800,
        options=[dropdown.Option(key=m["id"], 
           text=f' {m["id"]} {m["nombre"]}', data=m["id"]) for m in marcas],
        width=350,
    )

    estados = obtener_estados()
    # Dropdown para seleccionar estado
    estado = Dropdown(
        label="Estado",  border_color=colors.BLUE_GREY_800,
        options=[dropdown.Option(key=e["id"], 
            text=f' {e["id"]} {e["nombre"]}', data=e["id"]) for e in estados],
        width=350,
    )
    precio_venta = TextField(label="Precio de venta", border_color=colors.BLUE_GREY_800, width=350)
    add_vehiculo = ElevatedButton("Registrar vehiculo🚗", on_click=lambda e: registrar_vehiculo())
    

    def ver_vehiculos(e):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(f'select id_vehiculo, placa, color, marca, estado, precio_venta\
            from vehiculo v, marca m, estado e where v.id_marca = m.id_marca and v.id_estado = e.id_estado')
            info_vehi = []
            for vehi in cursor.fetchall():
                id_vehiculo, placa, color, marca, estado, precio_venta = vehi
                info_vehi.append({
                    'id_vehiculo': id_vehiculo,
                    'placa': placa,
                    'color': color,
                    'marca': marca,
                    'estado': estado,
                    'precio_venta': precio_venta
                })
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)
            
        vista_vehiculos.controls=[
            ListTile(
                title=Text( f'🚘{p['placa']}', weight='bold',size=19),
                subtitle=Text(f"""Color: {p['color']},  Marca: {p['marca']}, 
                    Estado: {p['estado']},  Precio: {p['precio_venta']}""", 
                    weight='bold', size=15),
                data=p['id_vehiculo'],
                on_click=lambda e:print(e.control.data) 
            ) for p in info_vehi if barra_busqueda.value in p['placa'] 
            or barra_busqueda.value in p['color'] or barra_busqueda.value in p['marca']
            or barra_busqueda.value in p['estado'] or barra_busqueda.value in str(p['precio_venta'])
        ] 
        vista_vehiculos.update()
    
    def cerrar_barra_busqueda(e):
        barra_busqueda.value = ""
        vista_vehiculos.clean()
        vista_vehiculos.update()
        barra_busqueda.update()
        
    # componentes para ver y buscar vehiculos
    vista_vehiculos = ListView(expand=1, spacing=0, padding=padding.only(0),)
    barra_busqueda = SearchBar(
        bar_leading=IconButton(icon=icons.SEARCH),
        on_change=ver_vehiculos,
        on_tap=ver_vehiculos,
        bar_trailing=[IconButton(icon=icons.CLOSE, on_click = cerrar_barra_busqueda)],
   )
    

    def componentes_de_ventas():
        page.clean()
        page.add(barra_nav,barra_busqueda,vista_vehiculos)
        
    # funcion para añadir style components para poder registrar un vehiculo
    def componentes_vehiculo():
        page.clean()
        page.add(placa,color,marca,estado,precio_venta,add_vehiculo,barra_nav)


    def cambiar_pestaña(e):
      
      cambio_pestñ = e.control.selected_index
      if cambio_pestñ == 1:  componentes_vehiculo()
      elif cambio_pestñ == 0: componentes_de_ventas()
      elif cambio_pestñ == 2: 
          page.clean()
          page.add(barra_nav)
      page.update()

    barra_nav = NavigationBar(
      selected_index=0,  on_change= cambiar_pestaña,
      destinations=[
         NavigationBarDestination(icon=icons.LIST, label=' ventas '),
         NavigationBarDestination(icon=icons.ADD, label='Registrar \n vehiculo'),
         NavigationBarDestination(icon=icons.EDIT, label=' \nclientes'),
         
      ],
      indicator_color=colors.GREEN_600
   )
    

    page.add(barra_nav,barra_busqueda,vista_vehiculos)
   
app(main)

