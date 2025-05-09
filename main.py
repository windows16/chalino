
import datetime
from flet import*
import sqlite3
import os
import platform # Importa el módulo 'os'


def main(ven: Page):
   ven.theme_mode = ThemeMode.LIGHT
   
   def tema():
      ven.theme_mode = ThemeMode.LIGHT if ven.theme_mode == ThemeMode.DARK else ThemeMode.DARK
      cambiar_tema.icon =icons.DARK_MODE if ven.theme_mode == ThemeMode.LIGHT else icons.LIGHT_MODE
      ven.update()


   cambiar_tema = IconButton( icon= icons.DARK_MODE,  on_click=lambda e: tema(),)

   temita = Container( cambiar_tema,  padding=padding.only(260,30))
   
   id_pedido = TextField(  label='id_pedido', border_color=colors.BLUE_GREY_800, width=110 )
   pedido = Container(id_pedido,padding=padding.only(0,30))
   
   cant = TextField( label='cant', border_color=colors.BLUE_GREY_800,  width=60)
   
   id_herramienta = Text()
   
   def llenar_texto(e):
    
      for elem in e.control.data:
        id_herramienta.value=elem['id']
        herramienta.value=elem['herr']
        precio.value=elem['Q']
        list_view.visible=False
        ven.update()
   
      
   def textbox_changed(string):
      con_bd1 = sqlite3.connect('alquiler.db')
      list_view.visible=True
      herramientas = []
      consulta_h = con_bd1.cursor()
      consulta_h.execute(f'select id_herramienta,descripcion_herramienta,precio_alquiler from herramientas;')
      for fila in consulta_h:
           v1,v2,q = fila
           herramientas.append({'id':f'{v1}','herr':v2,'Q':q})
      cad = string.control.value
      list_view.controls = [
         ListTile(title=Text(pe['herr']+'   Q'+str(pe['Q']),size=12, weight=FontWeight.W_900),
            data=[{'id':pe['id'],'herr':pe['herr'],'Q':pe['Q']}],
            on_click=llenar_texto) for pe in herramientas if cad.lower() in pe['herr']
      ] 
      if list_view.controls==[]:
        list_view.visible=False
      con_bd1.close()
      ven.update()
   
   herramienta = TextField(label="herramienta 🛠️", border_color=colors.BLUE_GREY_800,
       on_change=textbox_changed, on_focus=textbox_changed,)
   list_view = ListView(expand=3, padding=padding.only(10),spacing=0,visible=False)
    
   btn_agregar= IconButton(
      icon=icons.ADD_BOX, on_click= lambda e: añadir_herr(), icon_size=30, tooltip='añadir'
   )
   btn_update = IconButton(icon=icons.SAVE_AS_SHARP,  
      icon_size=30,tooltip='Guardar cambios', on_click= lambda e:update_herr(e)
   )
   
   actualizar = Container(btn_update,padding=padding.only(230,20))
   agregar = Container(btn_agregar,padding=padding.only(230,20))
   desc_herra = Container(herramienta, width=200)
   cant_desc = Container(Row([cant,desc_herra]),padding=padding.only(0,20))
   
   def limpiar_datos():

      cant.value=None
      herramienta.value=''
      precio.value=None
      view2.controls = [ ]
      herramienta.error_text=None
      cant.error_text=None
      id_pedido.error_text=None
      id_herramienta.value=None
      ven.update()

   def limpiar_herr():
      herramienta.value=''
      ven.update()

   btn_limpiar = IconButton(
      icon=icons.REFRESH, icon_size=25, on_click=lambda e: limpiar_datos()
   )
   limpiar = Container(
      btn_limpiar, padding=padding.only(180,30)
   )
   btn_limpiar_herr = IconButton(
      icon=icons.CLOSE, icon_size=25, on_click=lambda e: limpiar_herr()
   )

      
   def update_herr(e):
      
      if not id_pedido.value:
        id_pedido.error_text='obligatorio'
        ven.update()
        return
      id_pedido.error_text=None
      if not cant.value:
         cant.error_text='obligatorio'
         ven.update()
         return
      cant.error_text=None
      herramienta.error_text=None
      try: 
         con_bd2 = sqlite3.connect('alquiler.db')
         consulta = con_bd2.cursor()
         consulta.execute(f'update pedido set cant_herramienta={cant.value} where id_herramienta=(select id_herramienta from herramientas where descripcion_herramienta = \'{herramienta.value}\');') 
         con_bd2.commit()
      except Exception as ex:
         cant.error_text=ex
         con_bd2.close()
      mostrar_pedidos()
      set_id(e)
      
   def ver_p():
      con_bd3 = sqlite3.connect('alquiler.db')
      pedido = []
      consul=con_bd3.cursor()
      consul.execute(f'select inf.id_info_pedido,cliente,cant_herramienta,descripcion_herramienta,precio_alquiler from info_pedido inf,herramientas h,pedido p where h.id_herramienta = p.id_herramienta and p.id_info_pedido = inf.id_info_pedido and inf.id_info_pedido={id_valor.value};')
      for i in consul:
           id2,client2,cant2,desc2,precio = i
           pedido.append({'id2':f'{id2}','client2':client2,'cant2':cant2,'desc2':desc2,'precio':precio})
     
      view2.controls = [
         ListTile(title=Text(f'{p['cant2']}     {p['desc2']}   Q{p['cant2']*p['precio']}',weight='bold',
           size=13),data=[{'cant':p['cant2'],'des':p['desc2'],'id':p['id2']}],
           on_long_press=lambda e:op_pedido(e), )for p in pedido  
      ]
      con_bd3.close()
      ven.update()

   def añadir_herr():
      con_bd4 = sqlite3.connect('alquiler.db')
      consulta = con_bd4.cursor()
      consulta.execute(f'select p.id_info_pedido,cliente,cant_herramienta,descripcion_herramienta,precio_alquiler from info_pedido inf,herramientas h,pedido p where h.id_herramienta = p.id_herramienta and p.id_info_pedido = inf.id_info_pedido and inf.id_info_pedido={id_pedido.value};')
      pedi = []
      for i in consulta:
        num_ped,cliente,can,desc,precio=i
        pedi.append({'idp':num_ped,'herr':desc})
      
      for p in pedi:
         if herramienta.value == p['herr'] and id_pedido.value == str(p['idp']):
            herramienta.error_text='herramienta existente'
            ven.update()
            return
      if not id_pedido.value:
        id_pedido.error_text='obligatorio'
        ven.update()
        return
      id_pedido.error_text=None
      if not cant.value:
         cant.error_text='obligatorio'
         ven.update()
         return
      cant.error_text=None
      if herramienta.value == '':
        herramienta.error_text='obligatorio'
        ven.update()
        return
      herramienta.error_text=None
      
      try:
         consulta = con_bd4.cursor()
         consulta.execute(f'insert into pedido(cant_herramienta,id_herramienta,id_info_pedido) values({cant.value},(select id_herramienta from herramientas where descripcion_herramienta = \'{herramienta.value}\'),{id_pedido.value});') 
         con_bd4.commit()
      except Exception as ex:
         cant.error_text=ex
         con_bd4.close()
      ver_p()
      
   
   def cerrar(e):
      herramienta.value=''
      cant.value=''
      id_pedido.value=''
      herramienta.error_text=None
      cant.error_text=None
      id_pedido.error_text=None
      mostrar_pedidos()
      set_id(e)
      

   def registrar_pedido():
      ven.controls.clear()
      desc_herra.visible=True
      barra_nav.selected_index=2
      id_pedido.value=id_valor.value
      ven.add(Row([con_cerrar,limpiar]),Row([pedido]),Row([cant_desc,btn_limpiar_herr]),
      list_view,agregar,view2
      )
      
   
   des_he=Text(weight=FontWeight.BOLD, size=17)
   btn_cerrar= IconButton(icon=icons.ARROW_BACK_IOS, on_click=lambda e:cerrar(e))
   con_cerrar=Container(btn_cerrar,padding=padding.only(0,30))

   def update_pedido():
      ven.controls.clear()
      desc_herra.visible=False
      des_he.value=herramienta.value
      barra_nav.selected_index=2
      ven.add(Row([con_cerrar,limpiar]),Text(''),Text('  '),Row([cant,des_he])
         ,Column([actualizar])
      )
      
      ven.update()

   def eliminar_pedido(e):
      con_bd5 = sqlite3.connect('alquiler.db')
      consulta = con_bd5.cursor()
      consulta.execute(f'delete from pedido where id_herramienta=(select id_herramienta from herramientas where descripcion_herramienta = \'{herramienta.value}\') and id_info_pedido={id_valor.value};') 
      con_bd5.commit()
      con_bd5.close()
      herramienta.value=''
      cant.value=''
      id_pedido.value=''
      set_id(e)
      

   ingañil = TextField(label='albañil',border_color=colors.BLUE_GREY_800, width=200)
   cliente = TextField(label='cliente', border_color=colors.BLUE_GREY_800, width=200)
   direc = TextField( label='direccion', border_color=colors.BLUE_GREY_800, width=270)

   dia = TextField( label='dia', border_color=colors.BLUE_GREY_800, width=55)
   mes = TextField(label='mes', border_color=colors.BLUE_GREY_800, width=60)
   año = TextField(label='año', border_color=colors.BLUE_GREY_800, width=85)
   
   fecha = Container(Row([Icon(icons.CALENDAR_MONTH),dia,mes,año]),padding=padding.only(50))
   albañil = Container(ingañil,padding=padding.only(70))
   cliente_dir = Container(
      Column([fecha,cliente,albañil,direc]),
      padding=padding.only(0,30)
   )
   
   btn_regis = ElevatedButton(
      text='➕registrar', on_click=lambda e: añadir_infoPedido(e)
   )
   btn_update2 = ElevatedButton(
      text='✍️guardar cambios', on_click=lambda e: actualizar_infp(e)
   )
   registrar = Container(btn_regis,padding=padding.only(140,20))
   upd_info = Container(btn_update2,padding=padding.only(0,15), visible=False)

   btn_refresh = IconButton(
      icon_size=25,tooltip='refrescar',icon=icons.REFRESH,on_click=lambda e: limpiar2()
   )
   btn_cerrar2 = IconButton(
      icon_size=25,tooltip='cerrar',icon=icons.CLOSE,on_click=lambda e: refresh(e)
   )
   refrescar = Container(btn_refresh,padding=padding.only(0,30))
   cerrar2 = Container(btn_cerrar2,padding=padding.only(200,30))

   btn_update4 = ElevatedButton(text='✍️Editar', 
    on_click= lambda e: update_infop(e))
   btn_elim2 = ElevatedButton(text='🗑️eliminar', 
      on_click= lambda e: elim_infop(e))
   actualizar4 = Container(btn_update4, padding=padding.only(150), visible=False)
   eliminar2 = Container(btn_elim2, padding=padding.only(150), visible=False)
   
   def limpiar2():
       dia.value=''
       mes.value=''
       año.value=''
       cliente.value=''
       ingañil.value=''
       direc.value=''
       dia.error_text=None
       mes.error_text=None
       año.error_text=None
       cliente.error_text=None
       ingañil.error_text=None
       direc.error_text=None
       ven.update()

   def refresh(e):
       upd_info.visible=False
       registrar.visible=True
       actualizar4.visible=False
       eliminar2.visible=False
       limpiar2()
       mostrar_pedidos()
       on_change(e)
       ven.update()
   

   def op_infop(pe):
      for p in pe.control.data:
         dia.value = p['fech'][0:2]
         mes.value = p['fech'][3:5]
         año.value= p['fech'][6:10]
         cliente.value=p['cli']
         ingañil.value=p['alb']
         direc.value=p['dir']
         id_valor.value=p['id']
      actualizar4.visible=True
      eliminar2.visible=True
      ven.update()
   
   def update_infop(e):
      ven.controls.clear()
      ven.add(Row([refrescar,cerrar2]),cliente_dir,registrar,upd_info,id_valor)
      upd_info.visible=True
      registrar.visible=False
      ven.update()


   def elim_infop(e):

      try:
       con_bd6 = sqlite3.connect('alquiler.db')
       consul = con_bd6.cursor()
       consul.execute(f'delete from info_pedido where id_info_pedido={int(id_valor.value)};')
       con_bd6.commit()
      except: con_bd6.close()

      fechita = str(str(dia.value)+'/'+str(mes.value)+'/'+str(año.value))
      dir= str(direc.value)
      cli=str(cliente.value)
      alb=str(ingañil.value)      
      try:
       con_papelera = sqlite3.connect('alquiler.db')
       cursor = con_papelera.cursor()
       cursor.execute(f'insert into papelera(id_info_pedido,direccion, cliente, fecha, encargado_obra) values(\'{id_valor.value}\',\'{dir}\',\'{cli}\',\'{fechita}\',\'{alb}\');') 
       con_papelera.commit()
      except: con_papelera.close()
      limpiar2()
      mostrar_pedidos()
      on_change(e)

     

   def actualizar_infp(e):

      fecha_hoy = datetime.date.today()
      año_actual = [str(fecha_hoy.year),str(fecha_hoy.year-1)]
      dias31 = [str(val) for val in range(10,32)]
      dias31+=['01', '02', '03', '04', '05', '06', '07', '08', '09']
      meses12 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
      
      if not dia.value or dia.value not in dias31:
         dia.error_text='obligatorio'
         ven.update()
         return
      dia.error_text=None
      if not mes.value or mes.value not in meses12:
         mes.error_text='obligatorio'
         ven.update()
         return
      mes.error_text=None
      if not año.value or año.value not in año_actual:
         año.error_text='obligatorio'
         ven.update()
         return 
      año.error_text=None

      if not cliente.value and not ingañil.value:
         cliente.error_text='obligatorio'
         ingañil.error_text='obligatorio'
         ven.update()
         return
      cliente.error_text=None
      ingañil.error_text=None
      if not direc.value:
         direc.error_text='obligatorio'
         ven.update()
         return
      fechita = str(str(dia.value)+'/'+str(mes.value)+'/'+str(año.value))
      dir= str(direc.value)
      cli=str(cliente.value)
      alb=str(ingañil.value)
      
      try:
         con_bd7 = sqlite3.connect('alquiler.db')
         consul = con_bd7.cursor()
         consul.execute(f'update info_pedido set direccion=\'{dir}\',cliente=\'{cli}\',fecha=\'{fechita}\',encargado_obra=\'{alb}\' where id_info_pedido={int(id_valor.value)};')
         con_bd7.commit()
      except Exception as ex:
         cliente.error_text=ex
         ingañil.error_text=ex
         con_bd7.close()
      limpiar2()
      mostrar_pedidos()
      on_change(e)

      
   def añadir_infoPedido(e):
      
      fecha_hoy = datetime.date.today()
      año_actual = [str(fecha_hoy.year),str(fecha_hoy.year-1)]
      dias31 = [str(val) for val in range(10,32)]
      dias31+=['01', '02', '03', '04', '05', '06', '07', '08', '09']
      meses12 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
      
      if not dia.value or dia.value not in dias31:
         dia.error_text='obligatorio'
         ven.update()
         return
      dia.error_text=None
      if not mes.value or mes.value not in meses12:
         mes.error_text='obligatorio'
         ven.update()
         return
      mes.error_text=None
      if not año.value or año.value not in año_actual:
         año.error_text='obligatorio'
         ven.update()
         return 
      año.error_text=None
      if not cliente.value and not ingañil.value:
         cliente.error_text='obligatorio'
         ingañil.error_text='obligatorio'
         ven.update()
         return
      cliente.error_text=None
      ingañil.error_text=None
      if not direc.value:
         direc.error_text='obligatorio'
         ven.update()
         return
      direc.error_text=None

   
      fechita = str(str(dia.value)+'/'+str(mes.value)+'/'+str(año.value))
      dir= str(direc.value)
      client=str(cliente.value)
      alb=str(ingañil.value)

      con_bd8 = sqlite3.connect('alquiler.db')
      cursor = con_bd8.cursor()
      try:
         cursor.execute(f'insert into info_pedido(direccion, cliente, fecha, encargado_obra) values(\'{dir}\',\'{client}\',\'{fechita}\',\'{alb}\');') 
         cursor.execute('commit;')
      except Exception as ex: 
         cliente.error_text=ex
         ingañil.error_text=ex
         con_bd8.close()
      limpiar2()
      mostrar_pedidos()
      on_change(e)


   def registrar_infoPedido():
      hoy = datetime.date.today()

      if hoy.day<10:  dia.value=f'0{hoy.day}'
      else: dia.value=str(hoy.day)
      if hoy.month<10:  mes.value=f'0{hoy.month}'
      else: mes.value=str(hoy.month)
      año.value=str(hoy.year)
      ven.controls.clear()
      temita.padding.left=206
      barra_nav.selected_index=1
      ven.add(Row([refrescar,temita]),barra_nav,cliente_dir,registrar,upd_info)
   
   
   def datos_papelera(e):
      con_papelera = sqlite3.connect('alquiler.db')
      consul=con_papelera.cursor()
      consul.execute(f'select id_info_pedido,cliente,fecha,encargado_obra,direccion from papelera')
      pedidos_p=[]
      for i in consul:
         id2,client2,fecha2,alba,dir = i
         pedidos_p.append({'id2':f'{id2}','client2':f'{client2}','fecha':f'{fecha2}','albañil':f'{alba}','dir':f'{dir}'})
      
      valor_bus = str(e.data)
      view_papelera.controls=[ListTile(title=Text(' 🗃️ '+pe['id2']+')   '+pe['client2']+
        ',  '+pe['dir']+',  '+pe['albañil']+',  '+pe['fecha']  ,size=14,weight='bold'), 
        data=[{'id':pe['id2'],'cli':pe['client2'],'dir':pe['dir'],
          'alb':pe['albañil'],'fech':pe['fecha']}], 
        on_long_press=opciones_papelera) for pe in pedidos_p if valor_bus 
        in pe['id2'] or valor_bus in pe['client2'] or valor_bus in pe['dir']
        or valor_bus in pe['albañil'] or valor_bus in pe['fecha']
      ]
      ven.update()
   
   def opciones_papelera(pape):
      btn_elim_perma.visible=True
      btn_restaurar.visible=True
      ven.update()
      btn_restaurar.on_click=lambda e: revertir_cambios(pape)
      btn_elim_perma.on_click=lambda e: borrar_permanente(pape)
      ven.update()
   
   def borrar_permanente(pape):
      for p in pape.control.data:
         id_valor_p=p['id']

      con_bp = sqlite3.connect('alquiler.db')
      cursor = con_bp.cursor()
      try:
         cursor.execute(f'delete from pedido where id_info_pedido={id_valor_p};') 
         cursor.execute('commit;')
      except Exception as ex: 
         con_bp.close()     

      con_bp2 = sqlite3.connect('alquiler.db')
      cursor2 = con_bp2.cursor()
      try: 
         cursor2.execute(f'delete from papelera where id_info_pedido={id_valor_p};') 
         cursor2.execute('commit;')
      except Exception as ex: con_bp2.close()

      btn_elim_perma.visible=False
      btn_restaurar.visible=False
      mostrar_pedidos()
      on_change(pape)
      
   def revertir_cambios(pape):
      for p in pape.control.data:
         fecha_p = p['fech']
         cliente_p=p['cli']
         ingañil_p=p['alb']
         direc_p=p['dir']
         id_valor_p=p['id']
      
      con_bp = sqlite3.connect('alquiler.db')
      cursor = con_bp.cursor()
      try:
         cursor.execute(f'insert into info_pedido(id_info_pedido,direccion, cliente, fecha, encargado_obra) values(\'{id_valor_p}\',\'{direc_p}\',\'{cliente_p}\',\'{fecha_p}\',\'{ingañil_p}\');') 
         cursor.execute('commit;')
      except Exception as ex: 
         con_bp.close()

      con_bp2 = sqlite3.connect('alquiler.db')
      cursor2 = con_bp2.cursor()   
      try: 
         cursor2.execute(f'delete from papelera where id_info_pedido={id_valor_p};') 
         cursor2.execute('commit;')
      except Exception as ex: con_bp2.close()

      btn_elim_perma.visible=False
      btn_restaurar.visible=False
      mostrar_pedidos()
      on_change(pape)
      

   def salir_papelera(e):
      ven.controls.clear()
      mostrar_pedidos()
      on_change(e)

   def ver_papelera():
      ven.controls.clear()
      ven.add(Text(''),btn_salirpapelera, barra_papelera, view_papelera,
         Container(Column([btn_restaurar, btn_elim_perma]), padding=padding.only(120)))   
      ven.update()

   btn_elim_perma = ElevatedButton(text='borrar permanente', icon=icons.DELETE_FOREVER,
      visible= False)
   btn_restaurar = ElevatedButton(text='restaurar', icon=icons.RESTART_ALT, 
         visible=False)
   btn_salirpapelera = IconButton(icon=icons.ARROW_BACK_IOS, on_click=salir_papelera)
   view_papelera = ListView(expand=1, spacing=0, padding=padding.only(0))
   btn_papelera = ElevatedButton( text=' 🗑️ papelera' , on_click=lambda e: ver_papelera(),)
   barra_papelera = SearchBar(
        bar_leading=IconButton(icon=icons.SEARCH, on_click=datos_papelera),
        on_change=datos_papelera,
        on_tap=datos_papelera
   )
   
   


   def añadir_btn(e):
      password.visible=True
      btn_confirmar.visible=True
      btn_cancelar.visible=True
      boton_guardar_db.visible=False
      ven.update()

   def cancelar_pass(e):
      password.visible=False
      btn_confirmar.visible=False
      btn_cancelar.visible=False
      boton_guardar_db.visible=True
      ven.update()

   # Función al presionar el botón
   def verificar_pass(e):
      if password.value != 'fullpy123':
            ven.add(SnackBar(Text(f"pass invalido"), open=True))
      else: 
         btn_confirmar.visible=False
         btn_cancelar.visible=False
         password.visible=False
         ven.update()
         guardar_bd(e)
      

    # Botón de envío
   btn_confirmar = ElevatedButton(text="Confirmar", on_click=verificar_pass,visible=False)
   btn_cancelar = ElevatedButton(text="❌", on_click= cancelar_pass, visible=False,)
   
   # Campos de entrada
   password = TextField(label="Contraseña", 
         password=True, 
        can_reveal_password=True,
        border_color=colors.BLUE_GREY_800,
        width=200,
        visible=False,)
   
   def guardar_bd(e):
        
        nombre_archivo = "alquiler.db"
        if platform.system() == "Windows":
            ruta_guardado = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
        elif platform.system() == "Darwin":  # macOS
            ruta_guardado = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)
        else:  # Linux y otros
            ruta_guardado = os.path.join(os.path.expanduser("~"), "Downloads", nombre_archivo)

        try:
            import shutil
            shutil.copy(nombre_archivo, ruta_guardado)
            ven.add(SnackBar(Text(f"Base de datos guardada en: {ruta_guardado}"), open=True))
            
        except Exception as ex:
            ven.add(SnackBar(Text(f"Error al guardar la base de datos: {ex}"), open=True))
            
   boton_guardar_db = ElevatedButton(
        text='📥 db',
        on_click=añadir_btn, 
    )
   
   def copiar_portapapeles():
      peido=pediito.get_p()
      if not peido:
         return print('nadota')
   
      for p in peido: 
         infop=f'  cliente : {p['client2']} \n  albañil : {p['albañil']} \n  fecha : {p['fecha']} \n  direccion : {p['dir']} '
   
      content =''
      total=0
      for p in peido:
         content += '\n'
         content += '   '+str(p['cant2'])
         content += '    🛠️'+p['desc2']
         semitotal=p['precio']*int(p['cant2'])
         total += semitotal
         content += '  💵 Q'+str(semitotal)
      ven.set_clipboard(infop+'\n\n  cant  descripcion'+content+' \n'
      +' \n  total : Q'+str(total)+'\n deposito: Q'+str(round(total*0.4,3))+'\n')
      

   class obtener_pedido:
    def __init__(self,pedio):
      self.pedio=pedio
  
    def get_p(self):
      return self.pedio
    

   btn_copiar = IconButton(icon=icons.COPY, tooltip='copiar',
    on_click=lambda e:copiar_portapapeles()) 
   copiar = Container(btn_copiar,padding=padding.only(10),visible=False,)

   def set_id(e):
      if e.control.data:
         for p in e.control.data:
            id_valor.value=p['id']
         pedidos_exis(e)
      else: pedidos_exis(e)
   
   def op_pedido(pe):
      for p in pe.control.data:
         cant.value=p['cant']
         herramienta.value=p['des']
         id_pedido.value=p['id']
      actualizar3.visible=True
      eliminar.visible=True
      agregar2.visible=False
      copiar.visible=False
      ven.update()
   
   total_f = Text(size=13, weight='bold',visible=False)
   
   def pedidos_exis(d):
      con_bd9 = sqlite3.connect('alquiler.db')
      copiar.visible=True
      total_f.visible=True
      herramienta.value=''
      cant.value=''
      id_pedido.value=''
      actualizar4.visible=False
      eliminar2.visible=False
      actualizar3.visible=False
      eliminar.visible=False
      barra.visible=False
      barra2.visible=True
      view.visible=False
      view2.visible=True
      info_p.visible=True
      agregar2.visible=True
      pedido = []
      consul=con_bd9.cursor()
      consul.execute(f'select inf.id_info_pedido,cliente,cant_herramienta,descripcion_herramienta,precio_alquiler,encargado_obra,fecha,direccion from info_pedido inf,herramientas h,pedido p where h.id_herramienta = p.id_herramienta and p.id_info_pedido = inf.id_info_pedido and inf.id_info_pedido={id_valor.value};')
      for i in consul:
           id2,client2,cant2,desc2,precio,alba,fecha2,dir = i
           pedido.append({'id2':f'{id2}','client2':client2,'cant2':cant2,'desc2':desc2,'precio':precio,'fecha':f'{fecha2}','albañil':alba,'dir':dir})
      
      info_p.value=f'  cant        descripcion​'
      
      view2.controls = [
         ListTile(title=Text(f'{p['cant2']}     🛠️{p['desc2']}   💵 Q{p['cant2']*p['precio']} ',
            weight=FontWeight.W_900,
           size=13),data=[{'cant':p['cant2'],'des':p['desc2'],'id':p['id2']}],
           on_long_press=lambda e:op_pedido(e),
         )for p in pedido if str(d.data) in str(p['cant2']) or str(d.data) in p['desc2'] 
      ]
      global pediito
      pediito = obtener_pedido(pedido)
      tot=0
      for ped in pedido:
         tot+=ped['cant2']*ped['precio']
      total_f.value=f' total :  Q{tot}\n deposito : Q{round(tot*0.40,3)}'
      con_bd9.close()
      ven.update()
      

   def on_change(e):
        con_bd10 = sqlite3.connect('alquiler.db')
        copiar.visible=False
        total_f.visible=False
        id_valor.value=''
        actualizar3.visible=False
        eliminar.visible=False
        actualizar4.visible=False
        eliminar2.visible=False
        agregar2.visible=False
        barra.visible=True
        barra2.visible=False
        view.visible=True
        view2.visible=False
        info_p.visible=False
        pedidos = []
        consulta = con_bd10.cursor()
        consulta.execute(f'select id_info_pedido,cliente,fecha,encargado_obra,direccion from info_pedido;')
        for fila in consulta.fetchall():
            id,client,fech,alba,dir = fila
            if client == None: client=''
            if alba == None: alba=''
            pedidos.append({'id_pedido':f'{id}','cliente':f'{client}','fecha':f'{fech}','albañil':alba,'dir':dir})      

        valor_bus = str(e.data)
        view.controls=[ListTile(title=Text(' 📝  '+pe['cliente']+
        ',  '+pe['dir']+',  '+pe['albañil']+',  '+pe['fecha']  ,size=14,weight='bold'), 
        data=[{'id':pe['id_pedido'],'cli':pe['cliente'],'dir':pe['dir'],
          'alb':pe['albañil'],'fech':pe['fecha']}], 
        on_click=lambda e: set_id(e), on_long_press=op_infop
        ) 
        for pe in pedidos if valor_bus 
        in pe['id_pedido'] or valor_bus in pe['cliente'] or valor_bus in pe['dir']
        or valor_bus in pe['albañil'] or valor_bus in pe['fecha']
          ]
        con_bd10.close()      
        ven.update()

   
   def clear_txt(e):
       view.controls=[]
       view2.controls=[]
       barra2.value=''
       barra.value=''
       actualizar3.visible=False
       eliminar.visible=False
       actualizar4.visible=False
       eliminar2.visible=False
       total_f.visible=False
       info_p.visible=False
       ven.update()

   barra = SearchBar(
        bar_leading=IconButton(icon=icons.SEARCH, on_click=on_change),
        on_change=on_change,
        on_tap=on_change,
        bar_trailing=[IconButton(icon=icons.CLOSE, on_click=clear_txt)]
   )
   barra2 = SearchBar(
        bar_leading=IconButton(icon=icons.ARROW_BACK, on_click=on_change),
        view_elevation=0,
        on_change=lambda v:set_id(v),
        on_tap=lambda v:set_id(v),
        bar_trailing=[IconButton(icon=icons.CLOSE, on_click=clear_txt)],
        visible=False
   )
   info_p = Text(weight=FontWeight.BOLD,size=13)
   view= ListView(expand=1, spacing=0, padding=padding.only(0))
   view2= ListView(expand=1, spacing=0, padding=padding.only(0))
   
   barra_cont= Container(barra,width=300)
   barra_cont2= Container(barra2,width=300)
   
   btn_agregar2 = IconButton(icon=icons.ADD, tooltip='agregar',on_click=lambda e: registrar_pedido())
   btn_update3 = ElevatedButton(text='✍️Editar', 
    on_click= lambda e: update_pedido())
   btn_elim = ElevatedButton(text='🗑️eliminar', 
      on_click= lambda e: eliminar_pedido(e))
   agregar2 = Container(btn_agregar2,padding=padding.only(185,0), visible=False)
   actualizar3 = Container(btn_update3, padding=padding.only(150), visible=False)
   eliminar = Container(btn_elim, padding=padding.only(150), visible=False)
   id_valor = Text(weight='bold')

   
   def mostrar_pedidos():
      ven.controls.clear()
      barra_nav.selected_index=0
      temita.padding.left=150
      ven.add(Row([btn_papelera,temita]),barra_nav,barra_cont,barra_cont2,view,info_p,view2,
         Column([eliminar,actualizar3]),Column([eliminar2,actualizar4]),total_f,
         Row([agregar2,copiar]),id_valor,boton_guardar_db
      )
      ven.add(Container(btn_cancelar, padding=padding.only(150)),
         Column([password,btn_confirmar],alignment='center'))
   
   precio = TextField( label='Q 💵', border_color=colors.BLUE_GREY_800, width=65)
   btn_regisherr = ElevatedButton(text='➕agregar'
     , on_click = lambda e:agregar_regisherr())
   btn_elimherr = ElevatedButton(text='🗑️borrar'
   , on_click = lambda e:elim_regisherr())
   btn_updprecio = ElevatedButton(text='🔄modificar',
    on_click=lambda b:update_precioher())
   btn_limpiar2 = IconButton(icon=icons.CLEAR_ROUNDED, on_click = lambda e:limpiar3())
   
   txt_confirmar_del = Text('\nSeguro quiere eliminar la herramienta del registro? \n'
      +'la herramienta se eliminara tambien en los pedidos',weight=FontWeight.BOLD, 
      size=17, visible=False)
   btn_si_elim= ElevatedButton(text='si', on_click=lambda e: si_eliminar())
   btn_no_elim= ElevatedButton(text='no', on_click=lambda e:no_eliminar())

   elimherr = Container(btn_elimherr, padding=padding.only())
   updprecio = Container(btn_updprecio, padding=padding.only())
   regisherr = Container(btn_regisherr, padding=padding.only())
   btns_si_no=Container(Row([btn_si_elim,btn_no_elim]),
      visible=False, padding=padding.only(80))
   
   def limpiar3():
      id_herramienta.value=''
      herramienta.value=''
      precio.value=''
      list_view.controls =[]
      herramienta.error_text=None
      precio.error_text=None
      ven.update()

   def agregar_regisherr():
      
      if not precio.value:
         precio.error_text='obligatorio'
         ven.update()
         return
      precio.error_text=None
      if herramienta.value == '':
        herramienta.error_text='obligatorio'
        ven.update()
        return
      herramienta.error_text=None

      try:
         con_bd11 = sqlite3.connect('alquiler.db')
         consult2 = con_bd11.cursor()
         consult2.execute(f'insert into herramientas(descripcion_herramienta, precio_alquiler) values(\'{herramienta.value}\',{precio.value});') 
         con_bd11.commit()
      except Exception as ex:
         precio.error_text=ex
         ven.update()
         con_bd11.close()
         return
      limpiar3()
      
      
   def si_eliminar(): 
      try:
         con_bd12 = sqlite3.connect('alquiler.db')
         consult2 = con_bd12.cursor()
         consult2.execute(f'delete from herramientas where id_herramienta = \'{id_herramienta.value}\';') 
         con_bd12.commit()
      except Exception as ex: 
         precio.error_text=ex
         ven.update()
         con_bd12.close()
         return
      elimherr.visible=True
      updprecio.visible=True 
      regisherr.visible=True
      txt_confirmar_del.visible=False
      btns_si_no.visible=False
      ven.update()
      limpiar3()
      

   def no_eliminar():
      
      elimherr.visible=True
      updprecio.visible=True 
      regisherr.visible=True
      txt_confirmar_del.visible=False
      btns_si_no.visible=False
      ven.update()

   def elim_regisherr():
      if herramienta.value == '':
           herramienta.error_text='obligatorio'
           ven.update()
           return
      elimherr.visible=False
      updprecio.visible=False 
      regisherr.visible=False
      herramienta.error_text=None
      txt_confirmar_del.visible=True
      btns_si_no.visible=True
      ven.update()
      

   def update_precioher():
      
      if not precio.value:
         precio.error_text='obligatorio'
         ven.update()
         return
      precio.error_text=None
      if herramienta.value == '':
        herramienta.error_text='obligatorio'
        ven.update()
        return
      herramienta.error_text=None
      try:
         con_bd13 = sqlite3.connect('alquiler.db')
         consult2 = con_bd13.cursor()
         consult2.execute(f'update herramientas set precio_alquiler={int(precio.value)},descripcion_herramienta=\'{herramienta.value}\' where id_herramienta = {int(id_herramienta.value)};') 
         con_bd13.commit()
      except Exception as ex:
         precio.error_text=ex
         ven.update()
         con_bd13.close()
         return  
      limpiar3()
      


   def herram_regis():
      ven.controls.clear()
      temita.padding.left=258
      barra_nav.selected_index=2
      desc_herra.visible=True
      ven.add(temita,Text(''),Text(''),barra_nav,Row([desc_herra,precio,btn_limpiar2]),list_view,
         txt_confirmar_del,btns_si_no,Text(''),
         Row([elimherr ,updprecio, regisherr]), id_herramienta)
      

   def cambiar_pestaña(e):
      
      cambio_pestñ = e.control.selected_index
      if cambio_pestñ == 1:  registrar_infoPedido()
      elif cambio_pestñ == 0: 
         mostrar_pedidos()
         on_change(e)
      elif cambio_pestñ == 2: herram_regis()
      ven.update()

   barra_nav = NavigationBar(
      selected_index=0,  on_change= cambiar_pestaña,
      destinations=[
         NavigationBarDestination(icon=icons.LIST, label='Ver pedidos'),
         NavigationBarDestination(icon=icons.ADD, label='Registrar \n pedido'),
         NavigationBarDestination(icon=icons.EDIT, label='     Editar\nherramientas'),
         
      ],
      indicator_color=colors.GREEN_600
   )
   
   mostrar_pedidos()
   
   

app(main)


