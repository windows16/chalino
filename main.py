from flet import*
import mysql.connector 

conexion = mysql.connector.connect(
    host='localhost',
    password='fullsql123', 
    user='root',
    database='alquiler',
    port='3306'
)

def main(ven: Page):
    def on_click():
      consulta_h = conexion.cursor()
      consulta_h.execute(f'select id_herramienta,descripcion_herramienta,precio_alquiler from herramientas')
      for fila in consulta_h:
        txt.value = fila
      ven.update()
    def clear():
        txt.value=''
        ven.update()
    btn = ElevatedButton(text='dale', icon=icons.ADS_CLICK,
        on_click=lambda e:on_click()
    )
    btn_c = ElevatedButton(text='limpiar', icon=icons.CLEAR,
        on_click=lambda e:clear()
    )
    txt = Text(weight=FontWeight.BOLD, size=23)
    
    ven.add(Container(Column([btn,txt,btn_c]),padding=padding.only(150)))


app(main)
