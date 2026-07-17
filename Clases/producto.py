class Producto:
    def __init__(self, codigo_producto, cantidad_paquetes, peso_paquete, volumen_buenos_aires, volumen_curitiba, 
                 volumen_santiago, volumen_monterrey, volumen_bakersfield, dim_producto_ancho, dim_producto_largo,
                 dim_producto_alto):
        
        self.codigo_producto = codigo_producto
        self.cantidad_paquetes = cantidad_paquetes
        self.peso_paquete = peso_paquete
        self.peso_caja = cantidad_paquetes * peso_paquete
        
        self.volumen_buenos_aires = volumen_buenos_aires
        self.volumen_curitiba = volumen_curitiba
        self.volumen_santiago = volumen_santiago
        self.volumen_monterrey = volumen_monterrey
        self.volumen_bakersfield = volumen_bakersfield
        
        self.dim_producto_ancho = dim_producto_ancho
        self.dim_producto_largo = dim_producto_largo
        self.dim_producto_alto = dim_producto_alto

    def volumen_total(self):
        return (self.volumen_buenos_aires + self.volumen_curitiba + self.volumen_santiago +
                self.volumen_monterrey + self.volumen_bakersfield)

    def __repr__(self):
        return (f"<Producto {self.codigo_producto} | "
                f"Dim Prod: {self.dim_producto_ancho}x{self.dim_producto_largo}x{self.dim_producto_alto}mm | "
                f"Volumen Total: {self.volumen_total()}>")