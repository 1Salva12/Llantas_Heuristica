class Nodo:
    def __init__(self, datos, padre=None):
        self.datos = datos          
        self.padre = padre          
        self.costo_g = 0            
        self.heuristica_h = 0       
        self.empresas_usadas = set() 
        
        if padre:
            self.empresas_usadas = set(padre.empresas_usadas)
            self.empresas_usadas.add(datos)
        elif datos:
            self.empresas_usadas.add(datos)

    def get_datos(self): return self.datos
    def get_padre(self): return self.padre
    def get_costo_g(self): return self.costo_g
    def set_costo_g(self, costo): self.costo_g = costo
    def get_heuristica_h(self): return self.heuristica_h
    def set_heuristica_h(self, h): self.heuristica_h = h
    def get_costo_f(self): return self.costo_g + self.heuristica_h
    def igual(self, otro_nodo): return self.get_camino() == otro_nodo.get_camino()

    def get_camino(self):
        camino = []
        nodo_actual = self
        while nodo_actual and nodo_actual.datos is not None:
            camino.append(nodo_actual.datos)
            nodo_actual = nodo_actual.padre
        camino.reverse()
        return camino

def calcular_heuristica(tabla_precios, empresas_usadas, ruedas_restantes):
    if not ruedas_restantes:
        return 0
    empresas_disponibles = [emp for emp in tabla_precios.keys() if emp not in empresas_usadas]
    if not empresas_disponibles:
        return 0
    suma_minimos = 0
    for rueda in ruedas_restantes:
        precios_validos = [tabla_precios[emp][rueda] for emp in empresas_disponibles if rueda in tabla_precios[emp]]
        if precios_validos:
            suma_minimos += min(precios_validos)
    return suma_minimos

def buscar_solucion_A_estrella(tabla_precios, orden_ruedas):
    nodos_frontera = []
    nodo_raiz = Nodo(None)
    nodo_raiz.set_costo_g(0)
    nodo_raiz.set_heuristica_h(calcular_heuristica(tabla_precios, nodo_raiz.empresas_usadas, orden_ruedas))
    nodos_frontera.append(nodo_raiz)
    
    while len(nodos_frontera) > 0:
        nodos_frontera.sort(key=lambda x: x.get_costo_f())
        nodo_actual = nodos_frontera.pop(0)
        nivel_actual = len(nodo_actual.empresas_usadas)
        
        if nivel_actual == len(orden_ruedas):
            return nodo_actual
            
        rueda_actual = orden_ruedas[nivel_actual]
        ruedas_restantes = orden_ruedas[nivel_actual + 1:]
        
        for empresa in tabla_precios.keys():
            if empresa not in nodo_actual.empresas_usadas:
                hijo = Nodo(empresa, padre=nodo_actual)
                costo_paso = tabla_precios[empresa].get(rueda_actual, 0)
                hijo.set_costo_g(nodo_actual.get_costo_g() + costo_paso)
                hijo.set_heuristica_h(calcular_heuristica(tabla_precios, hijo.empresas_usadas, ruedas_restantes))
                
                repetido = False
                for n in nodos_frontera:
                    if n.igual(hijo) and n.get_costo_f() <= child_cost if 'child_cost' in locals() else n.get_costo_f() <= hijo.get_costo_f():
                        repetido = True
                        break
                if not repetido:
                    nodos_frontera.append(hijo)
    return None