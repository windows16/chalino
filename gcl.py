
from flet import*


def main(ven: Page):
    

    
    class Nodo:
        def __init__(self, regla):
            self.regla = regla
            self.hijo = []
    
        def mostrar_arbol(self, prefijo="", es_ultimo=True):
            connector = "└── " if es_ultimo else "├── "
            print(prefijo + connector + self.regla)
            txt.controls.append(Text(prefijo + connector + self.regla))
            ven.update()
            # Mostrar los hijos
            new_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            for i, hij in enumerate(self.hijo):
                es_ultimo_hij = i == len(self.hijo) - 1
                hij.mostrar_arbol(new_prefijo, es_ultimo_hij)
        
    def derivar_izquierda(palabra):
        """Derivación por la izquierda"""
        if not palabra:
            return Nodo('ε')

        raiz = Nodo('S')
        actual = raiz

        for i, char in enumerate(palabra):
            l_nodo = Nodo('L')
            l_nodo.hijo.append(Nodo(char))
            
            if i < len(palabra) - 1:
                s_node = Nodo('S')
                actual.hijo.extend([l_nodo, s_node])
                actual = s_node
            else:
                actual.hijo.append(l_nodo)
        return raiz

    def derivar_derecha(palabra):
        """Derivación por la derecha"""
        if not palabra:
            return Nodo('ε')

        raiz = Nodo('S')
        for char in reversed(palabra):
            new_raiz = Nodo('S')
            l_nodo = Nodo('L')
            l_nodo.hijo.append(Nodo(char))
            new_raiz.hijo = [l_nodo, raiz]
            raiz = new_raiz

        return raiz
    
    def evt_derivar_izquierda():
        deriv_izq=derivar_izquierda(entrada.value)
        deriv_izq.mostrar_arbol()
    def evt_derivar_derecha():
        deriv_der=derivar_derecha(entrada.value)
        deriv_der.mostrar_arbol()
    
    def limpiar_texto():
        txt.controls.clear()
        ven.update()
   
    btn_limpia = ElevatedButton("Limpiar derivaciones", on_click= lambda e: limpiar_texto())
    
    btn_derivar_izquierda = ElevatedButton("derivar por izq", on_click= lambda e:evt_derivar_izquierda()
            , )
    btn_derivar_derecha = ElevatedButton("derivar por der", on_click= lambda e:evt_derivar_derecha())
    entrada = TextField(label="Cadena a derivar", autofocus=True, width=300, border_radius=5, border_color="blue")
    txt = Column( scroll="always", width=1500, 
        height=400)
    ven.add(Row([entrada, btn_derivar_izquierda, btn_derivar_derecha]), txt, btn_limpia)
app(main,view=WEB_BROWSER)



