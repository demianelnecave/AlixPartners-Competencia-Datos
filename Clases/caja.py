def calcular_descuento_por_volumen(volumen):
    if volumen < 20000:
        return 0.10   # +10% markup
    elif volumen < 50000:
        return 0.00   # sin descuento
    elif volumen < 100000:
        return -0.10  # -10% descuento
    elif volumen < 500000:
        return -0.20  # -20% descuento
    else:
        return -0.30  # -30% descuento (máximo)

class Caja:
    def __init__(self, caja_id, dim_interior_ancho, dim_interior_largo, dim_interior_alto, 
                 compra_buenos_aires, compra_curitiba, compra_santiago, compra_monterrey, compra_bakersfield,
                 costo_unitario):
        
        self.caja_id = caja_id
        self.dim_interior_ancho = dim_interior_ancho
        self.dim_interior_largo = dim_interior_largo
        self.dim_interior_alto = dim_interior_alto
        
        self.grosor_mm = 0.0
        self.dim_exterior_ancho = 0.0
        self.dim_exterior_largo = 0.0
        self.dim_exterior_alto = 0.0
        
        self.unidades_buenos_aires = compra_buenos_aires
        self.unidades_curitiba = compra_curitiba
        self.unidades_santiago = compra_santiago
        self.unidades_monterrey = compra_monterrey
        self.unidades_bakersfield = compra_bakersfield
        
        self.unidades_buenos_aires_usadas = 0
        self.unidades_curitiba_usadas = 0
        self.unidades_santiago_usadas = 0
        self.unidades_monterrey_usadas = 0
        self.unidades_bakersfield_usadas = 0
        
        self.costo_unitario = costo_unitario
        self.descuento_buenos_aires = 0
        self.descuento_curitiba = 0
        self.descuento_santiago = 0
        self.descuento_monterrey = 0
        self.descuento_bakersfield = 0
        
        self.productos_asignados = []
            
    def cambiar_grosor(self, grosor_mm):
        self.grosor_mm = grosor_mm
        self.dim_exterior_ancho = self.dim_interior_ancho + 2 * grosor_mm
        self.dim_exterior_largo = self.dim_interior_largo + 2 * grosor_mm
        self.dim_exterior_alto = self.dim_interior_alto + 2 * grosor_mm
    
    def volumen_interno(self):
        return self.dim_interior_alto * self.dim_interior_ancho * self.dim_interior_largo
    
    def volumen_externo(self):
        return self.dim_exterior_alto * self.dim_exterior_ancho * self.dim_exterior_largo   
    
    def perimetro(self):
        return (self.dim_exterior_ancho + self.dim_exterior_largo) * 2
    
    def carga_maxima(self):
        ect_por_grosor = {2.5: 600, 2.7: 730, 3.0: 1000, 4.1: 1200, 4.5: 1400, 
                          4.6: 1450, 4.7: 1500, 4.8: 1550, 5.0: 1650}
        ect = ect_por_grosor[self.grosor_mm]
        return ect / self.perimetro() / 9.81

    def unidades_total(self):
        return (self.unidades_buenos_aires + self.unidades_curitiba + self.unidades_santiago +
                self.unidades_monterrey + self.unidades_bakersfield)
        
    def es_asignable_por_dimension(self, producto):
        entra = (producto.dim_producto_alto <= self.dim_interior_alto and
                 producto.dim_producto_ancho <= self.dim_interior_ancho and
                 producto.dim_producto_largo <= self.dim_interior_largo)
        maximo_en_10 = (producto.dim_producto_alto * 1.1 >= self.dim_interior_alto and
                        producto.dim_producto_ancho * 1.1 >= self.dim_interior_ancho and
                        producto.dim_producto_largo * 1.1 >= self.dim_interior_largo)
        return entra and maximo_en_10
    
    def asignar_producto(self, producto):
        if self.es_asignable_por_dimension(producto):
            self.productos_asignados.append(producto)
            plantas = ['buenos_aires', 'curitiba', 'santiago', 'monterrey', 'bakersfield']
            for planta in plantas:
                self.__dict__[f'unidades_{planta}_usadas'] += producto.__dict__[f'produccion_{planta}']
                self.__dict__[f'descuento_{planta}'] = calcular_descuento_por_volumen(self.__dict__[f'unidades_{planta}_usadas'])
        else:
            print("No es una caja asignable para el producto.")
        
    def revocar_producto(self, producto):
        if producto in self.productos_asignados:
            self.productos_asignados.remove(producto)
            plantas = ['buenos_aires', 'curitiba', 'santiago', 'monterrey', 'bakersfield']
            for planta in plantas:
                self.__dict__[f'unidades_{planta}_usadas'] -= producto.__dict__[f'produccion_{planta}']
                self.__dict__[f'descuento_{planta}'] = calcular_descuento_por_volumen(self.__dict__[f'unidades_{planta}_usadas'])
        else: 
            print("El producto no usaba este tipo de caja.")
    
    def costo_total(self):
        costo = 0
        plantas = ['buenos_aires', 'curitiba', 'santiago', 'monterrey', 'bakersfield']
        
        for planta in plantas:
            unidades_usadas = getattr(self, f'unidades_{planta}_usadas')
            descuento = getattr(self, f'descuento_{planta}')
            precio_con_descuento = self.costo_unitario * (1 + descuento)
            costo += unidades_usadas * precio_con_descuento
        
        return costo
    
    def __repr__(self):
        return (f"<Caja {self.caja_id} | "
                f"Int: {self.dim_interior_ancho}x{self.dim_interior_largo}x{self.dim_interior_alto}mm>")