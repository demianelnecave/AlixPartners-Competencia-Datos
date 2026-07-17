class Producto:
    def __init__(self, codigo_producto, cantidad_paquetes, peso_paquete, produccion_buenos_aires, produccion_curitiba, 
                 produccion_santiago, produccion_monterrey, produccion_bakersfield, dim_producto_ancho, dim_producto_largo,
                 dim_producto_alto):
        
        self.codigo_producto = codigo_producto
        self.cantidad_paquetes = cantidad_paquetes
        self.peso_paquete = peso_paquete
        self.peso_caja = cantidad_paquetes * peso_paquete
        
        self.produccion_buenos_aires = produccion_buenos_aires
        self.produccion_curitiba = produccion_curitiba
        self.produccion_santiago = produccion_santiago
        self.produccion_monterrey = produccion_monterrey
        self.produccion_bakersfield = produccion_bakersfield
        
        self.dim_producto_ancho = dim_producto_ancho
        self.dim_producto_largo = dim_producto_largo
        self.dim_producto_alto = dim_producto_alto

    def produccion_total(self):
        return (self.produccion_buenos_aires + self.produccion_curitiba + self.produccion_santiago +
                self.produccion_monterrey + self.produccion_bakersfield)

    def __repr__(self):
        return (f"<Producto {self.codigo_producto} | "
                f"Dim Prod: {self.dim_producto_ancho}x{self.dim_producto_largo}x{self.dim_producto_alto}mm | "
                f"Volumen Total: {self.produccion_total()}>")