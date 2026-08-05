from Clases.asignacion import Asignacion
from Clases.caja import Caja
from Clases.producto import Producto
from Clases.solucion import Solucion

def swap(solucion, productos, cajas_asignables_por_producto, titulo_solucion):
    mejorable = True
    solucion.titulo = titulo_solucion
    
    cajas_solucion = []
    for asignacion in solucion.asignaciones:
        if asignacion.caja not in cajas_solucion:
            cajas_solucion.append(asignacion.caja)
    
    while mejorable: 
        mejorable = False  
        
        # Recorremos todos los pares de productos
        productos_lista = list(productos.values())
        for i in range(len(productos_lista)):
            for j in range(i + 1, len(productos_lista)):
                producto_i = productos_lista[i]
                producto_j = productos_lista[j]
                
                # Encontrar las asignaciones de cada producto                
                for asig in solucion.asignaciones:
                    if asig.producto == producto_i:
                        asignacion_i = asig
                    elif asig.producto == producto_j:
                        asignacion_j = asig
                
                # Guardar las cajas originales
                caja_original_i = asignacion_i.caja
                caja_original_j = asignacion_j.caja
                
                # Verificar si el swap es válido (ambas cajas son asignables para los productos)
                if (caja_original_j.caja_id in cajas_asignables_por_producto[producto_i.codigo_producto] and 
                    caja_original_i.caja_id in cajas_asignables_por_producto[producto_j.codigo_producto]):
                    
                    costo_actual = solucion.costo_total()
                    
                    # Realizar el swap
                    solucion.cambiar_asignacion(asignacion_i, caja_original_j)
                    solucion.cambiar_asignacion(asignacion_j, caja_original_i)
                    
                    # Verificar si mejoró
                    if solucion.costo_total() >= costo_actual:
                        # Si no mejora, deshacer el swap
                        solucion.cambiar_asignacion(asignacion_i, caja_original_i)
                        solucion.cambiar_asignacion(asignacion_j, caja_original_j)
                    else:
                        print(f"Swap mejoró de {costo_actual} a {solucion.costo_total()}")
                        mejorable = True