from django.shortcuts import render
from .utils import buscar_solucion_A_estrella

def optimizar_llantas(request):
    empresas = ['Empresa1', 'Empresa2', 'Empresa3', 'Empresa4']
    ruedas = ['Tipo T', 'Tipo H', 'Tipo V', 'Tipo W']
    
    resultado = None
    costo_total = None
    
    if request.method == 'POST':
        tabla_precios = {}
        for emp in empresas:
            tabla_precios[emp] = {}
            for rueda in ruedas:
                input_name = f"{emp}_{rueda}"
                try:
                    valor = float(request.POST.get(input_name, 0))
                except ValueError:
                    valor = 0.0
                tabla_precios[emp][rueda] = valor
        
        nodo_solucion = buscar_solucion_A_estrella(tabla_precios, ruedas)
        
        if nodo_solucion:
            camino_empresas = nodo_solucion.get_camino()
            costo_total = nodo_solucion.get_costo_g()
            
            resultado = []
            for i, rueda in enumerate(ruedas):
                emp_asignada = camino_empresas[i]
                precio = tabla_precios[emp_asignada][rueda]
                resultado.append({
                    'rueda': rueda,
                    'empresa': emp_asignada,
                    'precio': precio
                })

    context = {
        'empresas': empresas,
        'ruedas': ruedas,
        'resultado': resultado,
        'costo_total': costo_total
    }
    return render(request, 'optimizador.html', context)