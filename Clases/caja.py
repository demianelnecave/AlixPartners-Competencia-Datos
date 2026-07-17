class Caja:
    def __init__(self, caja_id, dim_interior_ancho, dim_interior_largo, dim_interior_alto, grosor_mm, 
                 compra_buenos_aires, compra_curitiba, compra_santiago, compra_monterrey, compra_bakersfield,
                 costo_unitario):
        
        self.caja_id = caja_id
        self.dim_interior_ancho = dim_interior_ancho
        self.dim_interior_largo = dim_interior_largo
        self.dim_interior_alto = dim_interior_alto
        
        self.grosor_mm = grosor_mm
        self.dim_exterior_ancho = dim_interior_ancho + 2 * grosor_mm
        self.dim_exterior_largo = dim_interior_largo + 2 * grosor_mm
        self.dim_exterior_alto = dim_interior_alto + 2 * grosor_mm
        
        self.unidades_buenos_aires = compra_buenos_aires
        self.unidades_curitiba = compra_curitiba
        self.unidades_santiago = compra_santiago
        self.unidades_monterrey = compra_monterrey
        self.unidades_bakersfield = compra_bakersfield
        
        self.costo_unitario = costo_unitario
        
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
            self.unidades_buenos_aires -= producto.produccion_buenos_aires
            self.unidades_curitiba -= producto.produccion_curitiba
            self.unidades_santiago -= producto.produccion_santiago
            self.unidades_monterrey -= producto.produccion_monterrey
            self.unidades_bakersfield -= producto.produccion_bakersfield
        else:
            print("No es una caja asignable para el producto.")
    
    def revocar_producto(self, producto):
        if producto in self.productos_asignados:
            self.productos_asignados.remove(producto)
            self.volumen_buenos_aires += producto.volumen_buenos_aires
            self.volumen_curitiba += producto.volumen_curitiba
            self.volumen_santiago += producto.volumen_santiago
            self.volumen_monterrey += producto.volumen_monterrey
            self.volumen_bakersfield += producto.volumen_bakersfield
        else: 
            print("El producto no usaba este tipo de caja.")
    
    def __repr__(self):
        return (f"<Caja {self.caja_id} | "
                f"Int: {self.dim_interior_ancho}x{self.dim_interior_largo}x{self.dim_interior_alto}mm | "
                f"Ext: {self.dim_exterior_ancho}x{self.dim_exterior_largo}x{self.dim_exterior_alto}mm | "
                f"Grosor: {self.grosor_mm}mm>")