from Clases.caja import Caja

class Producto:
    def __init__(self, codigo_producto, cantidad_paquetes, peso_paquete, volumen_buenos_aires, volumen_curitiba, volumen_santiago,
                 volumen_monterrey, volumen_bakersfield, caja_id):
        self.codigo_producto = codigo_producto
        self.cantidad_paquetes = cantidad_paquetes
        self.peso_paquete = peso_paquete
        self.peso_caja = cantidad_paquetes * peso_paquete
        
        self.volumen_buenos_aires = volumen_buenos_aires
        self.volumen_curitiba = volumen_curitiba
        self.volumen_santiago = volumen_santiago
        self.volumen_monterrey = volumen_monterrey
        self.volumen_bakersfield = volumen_bakersfield
        self.volumen_total = (volumen_buenos_aires + volumen_curitiba + volumen_santiago +
                             volumen_monterrey + volumen_bakersfield)
        
        caja = Caja.buscar_por_id(caja_id)
        self.caja = caja
        self.dim_producto_ancho = caja.dim_interior_ancho
        self.dim_producto_largo = caja.dim_interior_largo
        self.dim_producto_alto = caja.dim_interior_alto
    
    def reasignar_caja(self, caja_id):
        self.caja = Caja.buscar_por_id(caja_id)
        
    def es_caja_asignable(self, caja):
        entra = (self.dim_producto_alto <= caja.dim_interior_alto and
                 self.dim_producto_ancho <= caja.dim_interior_ancho and
                 self.dim_producto_largo <= caja.dim_interior_largo)
        maximo_en_10 = (self.dim_producto_alto * 1.1 >= caja.dim_interior_alto and
                        self.dim_producto_ancho * 1.1 >= caja.dim_interior_ancho and
                        self.dim_producto_largo * 1.1 >= caja.dim_interior_largo)
        return entra and maximo_en_10

    def __repr__(self):
        return (f"<Producto {self.codigo_producto} | "
                f"Dim Prod: {self.dim_producto_ancho}x{self.dim_producto_largo}x{self.dim_producto_alto}mm | "
                f"Caja: {self.caja.caja_id}>")