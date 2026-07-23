import math
import copy

class Asignacion:
    def __init__(self, producto, caja):
        self.producto = producto
        self.caja = caja

    def validar_por_dimension(self):
        caja_redimensionada = copy.deepcopy(self.caja)
        caja_redimensionada.dim_interior_alto *= 1.1
        caja_redimensionada.dim_interior_ancho *= 1.1
        caja_redimensionada.dim_interior_largo *= 1.1
        
        volumen_mayor = caja_redimensionada.volumen_interno() >= self.producto.volumen_producto()
        return volumen_mayor
    
    def validar_por_headspace(self):
        grosor = self.caja.grosor_mm
        headspace_por_grosor = {3: 0.06, 4.5: 0.08, 5: 0.1}
        headspace_max = headspace_por_grosor[grosor]
        
        headspace_alto = self.caja.dim_interior_alto - self.producto.dim_producto_alto
        headspace_ancho = self.caja.dim_interior_ancho - self.producto.dim_producto_ancho
        headspace_largo = self.caja.dim_interior_largo - self.producto.dim_producto_largo
        
        chequeo_headspace = (headspace_alto / self.caja.dim_interior_alto <= headspace_max and
                             headspace_ancho / self.caja.dim_interior_ancho <= headspace_max and
                             headspace_largo / self.caja.dim_interior_largo <= headspace_max)
        
        tope_40mm = headspace_alto <= 40 and headspace_ancho <= 40 and headspace_largo <= 40
        
        return chequeo_headspace and tope_40mm
    
    def validar_por_resistencia(self):        
        carga_maxima = self.caja.carga_maxima()
        
        # Calculemos y comparemos con el peso total de las cajas apiladas
        cant_cajas_alto = 1800 // self.caja.dim_exterior_alto
        peso_caja = self.producto.peso_caja
        peso_total = peso_caja * cant_cajas_alto
        
        return carga_maxima >= peso_total
    
    def es_asignacion_valida(self):
        return self.validar_por_dimension() and self.validar_por_headspace() and self.validar_por_resistencia()

    def utilizacion_caja(self):
        volumen_producto = self.producto.dim_producto_alto * self.producto.dim_producto_ancho * self.producto.dim_producto_largo
        volumen_caja_interna = self.caja.dim_interior_alto * self.caja.dim_interior_ancho * self.caja.dim_interior_largo
        return volumen_producto / volumen_caja_interna

    def cant_pallets_requeridas(self):
        cantidad = 0
        plantas = ['buenos_aires', 'curitiba', 'santiago', 'monterrey', 'bakersfield']
        for planta in plantas:
            volumen = getattr(self.producto, f'demanda_{planta}')
            cajas_por_pallet = self.caja.cantidad_cajas_por_pallet()
            cantidad += math.ceil(volumen / cajas_por_pallet) # Redondear siempre para arriba
        return cantidad

    def costo_pakaging_producto_planta(self, planta):
        '''
        Pre: El producto debe ser vinculado al tipo de caja de la asignación.
        '''
        unidades = getattr(self.producto, f'demanda_{planta}')
        descuento = getattr(self.caja, f'descuento_{planta}')
        precio_con_descuento = self.caja.costo_unitario * (1 + descuento)
        costo = unidades * precio_con_descuento
        return costo
    
    def costo_packaging_producto_total(self):
        '''
        Pre: El producto debe ser vinculado al tipo de caja de la asignación.
        '''
        costo = 0
        plantas = ['buenos_aires', 'curitiba', 'santiago', 'monterrey', 'bakersfield']
        for planta in plantas:
            unidades = getattr(self.producto, f'demanda_{planta}')
            descuento = getattr(self.caja, f'descuento_{planta}')
            precio_con_descuento = self.caja.costo_unitario * (1 + descuento)
            costo += unidades * precio_con_descuento
        return costo

    def __repr__(self):
        return (f"<Producto {self.producto.codigo_producto} | "
                f"Tipo de Caja: {self.caja.caja_id}>")