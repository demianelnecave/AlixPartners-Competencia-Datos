from Clases.asignacion import Asignacion
from Clases.caja import Caja
from Clases.producto import Producto
from Clases.solucion import Solucion

def solucion_greedy(cajas, productos, lista_productos_ordenados, cajas_asignables_por_producto, titulo_solucion, 
                    criterio_greedy, grosor):
    
    solucion = Solucion(grosor, titulo_solucion)

    for codigo_producto in lista_productos_ordenados:
        producto = productos[codigo_producto]
        metricas = {}  # caja_id -> (volumen_total, costo_packaging, costo_flete, costo_total, utilizacion_pallet)
        
        for caja_id in cajas_asignables_por_producto[codigo_producto]:
            caja = cajas[caja_id]
            
            # Volumen requerido actual (antes de asignar este producto)
            volumen_total = caja.unidades_total_requeridas()
            utilizacion_pallet = caja.utilizacion_pallet()
            
            # Costo simulado de asignar este producto a esta caja
            asignacion = Asignacion(producto, caja)
            caja.asignar_producto(producto)
            
            # Calculamos los costos del producto utilizando ese tipo de caja
            costo_packaging = asignacion.costo_packaging_producto_total()
            costo_flete = 150 * asignacion.cant_pallets_requeridas()
            costo_total = costo_packaging + costo_flete
            metricas[caja_id] = (volumen_total, costo_packaging, costo_flete, costo_total, utilizacion_pallet)
            
            # Revertimos la asignación para que no se aplique un descuento posterior
            caja.revocar_producto(producto)
        
        # Criterios a elegir
        if criterio_greedy == "minimizar_costo_total":
            caja_id_optima = min(metricas, key=lambda id: (metricas[id][3]))
        elif criterio_greedy == "maximizar_volumen_tipo":        
            caja_id_optima = max(metricas, key=lambda id: (metricas[id][0], -metricas[id][3])) # Desempate con costo minimo total
        elif criterio_greedy == "minimizar_costo_flete":
            caja_id_optima = min(metricas, key=lambda id: (metricas[id][2]))
        elif criterio_greedy == "maximizar_utilizacion_pallet":
            caja_id_optima = max(metricas, key=lambda id: (metricas[id][4]))
        
        caja_optima = cajas[caja_id_optima]
        asignacion = Asignacion(producto, caja_optima)
        solucion.agregar_asignacion(asignacion)    
    
    return solucion