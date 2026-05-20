from django.shortcuts import render
from .utils import buscar_solucion_A_estrella

def optimizar_llantas(request):
    empresas = ['Empresa1', 'Empresa2', 'Empresa3', 'Empresa4']
    ruedas = ['Tipo T', 'Tipo H', 'Tipo V', 'Tipo W']
    
    # Precios unitarios base de tu problema original
    precios_unitarios = {
        'Empresa1': {'Tipo T': 20, 'Tipo H': 30, 'Tipo V': 20, 'Tipo W': 40},
        'Empresa2': {'Tipo T': 50, 'Tipo H': 50, 'Tipo V': 40, 'Tipo W': 50},
        'Empresa3': {'Tipo T': 60, 'Tipo H': 55, 'Tipo V': 50, 'Tipo W': 60},
        'Empresa4': {'Tipo T': 100, 'Tipo H': 80, 'Tipo V': 60, 'Tipo W': 70}
    }

    resultado = None
    costo_total = None
    # Valores por defecto de las cantidades en la interfaz
    cantidades = {'Tipo T': 1, 'Tipo H': 1, 'Tipo V': 1, 'Tipo W': 1}
    
    if request.method == 'POST':
        # 1. Obtener las cantidades que el usuario escribió en el formulario
        for rueda in ruedas:
            try:
                cantidades[rueda] = int(request.POST.get(f"cant_{rueda}", 0))
            except ValueError:
                cantidades[rueda] = 0

        # 2. Construir la nueva tabla de precios matemáticos MULTIPLICADOS por la cantidad
        tabla_precios_totales = {}
        for emp in empresas:
            tabla_precios_totales[emp] = {}
            for rueda in ruedas:
                cantidad = cantidades[rueda]
                # Costo total para esa posición = precio_unitario * cantidad
                tabla_precios_totales[emp][rueda] = precios_unitarios[emp][rueda] * cantidad
        
        # 3. Ejecutar el algoritmo A* con la matriz de costos escalados
        nodo_solucion = buscar_solucion_A_estrella(tabla_precios_totales, ruedas)
        
        if nodo_solucion:
            camino_empresas = nodo_solucion.get_camino()
            costo_total = nodo_solucion.get_costo_g()
            
            resultado = []
            for i, rueda in enumerate(ruedas):
                emp_asignada = camino_empresas[i]
                cantidad = cantidades[rueda]
                precio_u = precios_unitarios[emp_asignada][rueda]
                subtotal = tabla_precios_totales[emp_asignada][rueda]
                
                # Solo mostrar en el resultado si se pidieron llantas de ese tipo
                if cantidad > 0:
                    resultado.append({
                        'rueda': rueda,
                        'cantidad': cantidad,
                        'empresa': emp_asignada,
                        'precio_unitario': precio_u,
                        'subtotal': subtotal
                    })

    context = {
        'empresas': empresas,
        'ruedas': ruedas,
        'cantidades': cantidades,
        'precios_unitarios': precios_unitarios,
        'resultado': resultado,
        'costo_total': costo_total
    }
    return render(request, 'optimizador.html', context)