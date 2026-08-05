from Clases.asignacion import Asignacion
from Clases.caja import Caja
from Clases.producto import Producto
from Clases.solucion import Solucion

def relocate(solucion, productos, cajas_asignables_por_producto, titulo_solucion):
    mejorable = True
    solucion.titulo = titulo_solucion
    
    cajas_solucion = []
    for asignacion in solucion.asignaciones:
        if asignacion.caja not in cajas_solucion:
            cajas_solucion.append(asignacion.caja)
    
    while mejorable: 
        mejorable = False  
        for codigo, producto in productos.items():
            for asig in solucion.asignaciones:
                if asig.producto == producto:
                    asignacion = asig
            
            caja_original = asignacion.caja
            mejor_costo_total = solucion.costo_total()
            
            for caja in cajas_solucion:
                caja_id = caja.caja_id
                if caja_id in cajas_asignables_por_producto[producto.codigo_producto]:
                    solucion.cambiar_asignacion(asignacion, caja)
                    
                    if solucion.costo_total() >= mejor_costo_total: # Si no mejora el costo, reasigno el original
                        solucion.cambiar_asignacion(asignacion, caja_original)
                    else:
                        print("Baja de ", mejor_costo_total, "a ", solucion.costo_total())
                        caja_original = caja
                        mejor_costo_total = solucion.costo_total()
                        mejorable = True