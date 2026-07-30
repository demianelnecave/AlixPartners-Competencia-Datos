from Clases.asignacion import Asignacion
from Clases.caja import Caja
from Clases.producto import Producto
from Clases.solucion import Solucion

def relocate(solucion, cajas, cajas_asignables_por_producto, titulo_solucion):
    mejorable = True
    solucion.titulo = titulo_solucion
    
    while mejorable: 
        mejorable = False  
        print("Hola")  
        for asignacion in solucion.asignaciones:
            producto = asignacion.producto
            caja_original = asignacion.caja
            mejor_costo_total = solucion.costo_total()
            
            for caja_id in cajas_asignables_por_producto[producto.codigo_producto]:
                caja = cajas[caja_id]
                solucion.cambiar_asignacion(asignacion, caja)
                
                if solucion.costo_total() >= mejor_costo_total: # Si no mejora el costo, reasigno el original}
                    solucion.cambiar_asignacion(asignacion, caja_original)
                else:
                    mejor_costo_total = solucion.costo_total()
                    mejorable = True
                    print(solucion.costo_total())