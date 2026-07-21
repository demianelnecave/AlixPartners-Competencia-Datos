class Producto:
    def __init__(self, codigo_producto, cantidad_paquetes, peso_paquete, demanda_buenos_aires, demanda_curitiba, 
                 demanda_santiago, demanda_monterrey, demanda_bakersfield, dim_producto_ancho, dim_producto_largo,
                 dim_producto_alto):
        
        self.codigo_producto = codigo_producto
        self.cantidad_paquetes = cantidad_paquetes
        self.peso_paquete = peso_paquete
        self.peso_caja = cantidad_paquetes * peso_paquete
        
        self.demanda_buenos_aires = demanda_buenos_aires
        self.demanda_curitiba = demanda_curitiba
        self.demanda_santiago = demanda_santiago
        self.demanda_monterrey = demanda_monterrey
        self.demanda_bakersfield = demanda_bakersfield
        
        self.dim_producto_ancho = dim_producto_ancho
        self.dim_producto_largo = dim_producto_largo
        self.dim_producto_alto = dim_producto_alto
        
        self.cajas_asignables = []

    def demanda_total(self):
        return (self.demanda_buenos_aires + self.demanda_curitiba + self.demanda_santiago +
                self.demanda_monterrey + self.demanda_bakersfield)
        
    def agregar_caja_asignable(self, caja_id):
        self.cajas_asignables.append(caja_id)
        
    def volumen_producto(self):
        return self.dim_producto_alto * self.dim_producto_ancho * self.dim_producto_largo

    def __repr__(self):
        return (f"<Producto {self.codigo_producto} | "
                f"Dim Prod: {self.dim_producto_ancho} x {self.dim_producto_largo} x {self.dim_producto_alto}mm | "
                f"Demanda Total: {self.demanda_total()}>")