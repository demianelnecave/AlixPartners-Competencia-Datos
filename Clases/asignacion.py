import math

class Asignacion:
    def __init__(self, producto, caja):
        self.producto = producto
        self.caja = caja

    def validar_por_dimension(self):
        maximo_en_10_porcent = (self.producto.dim_producto_alto * 1.1 >= self.caja.dim_interior_alto and
                                self.producto.dim_producto_ancho * 1.1 >= self.caja.dim_interior_ancho and
                                self.producto.dim_producto_largo * 1.1 >= self.caja.dim_interior_largo and
                                self.producto.dim_producto_alto * 0.9 <= self.caja.dim_interior_alto and
                                self.producto.dim_producto_ancho * 0.9 <= self.caja.dim_interior_ancho and
                                self.producto.dim_producto_largo * 0.9 <= self.caja.dim_interior_largo)
        
        tope_40mm = (self.producto.dim_producto_alto + 40 >= self.caja.dim_interior_alto and
                    self.producto.dim_producto_ancho + 40 >= self.caja.dim_interior_ancho and
                    self.producto.dim_producto_largo + 40 >= self.caja.dim_interior_largo and
                    self.producto.dim_producto_alto - 40 <= self.caja.dim_interior_alto and
                    self.producto.dim_producto_ancho - 40 <= self.caja.dim_interior_ancho and
                    self.producto.dim_producto_largo - 40 <= self.caja.dim_interior_largo)
        
        volumen_mayor = self.caja.volumen_interno() >= self.producto.volumen_producto()
        return maximo_en_10_porcent and tope_40mm and volumen_mayor
    
    def validar_por_headspace(self):
        return True
    
    def validar_por_resistencia(self):
        return True
    
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