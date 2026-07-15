from caja import Caja

class Producto:
    def __init__(self, cantidad_paquetes, peso_paquete, volumen_buenos_aires, volumen_curitiba, volumen_santiago,
                 volumen_monterrey, volumen_bakersfield):
        self.cantidad_paquetes = cantidad_paquetes
        self.peso_paquete = peso_paquete
        self.peso_caja = cantidad_paquetes * peso_paquete
        
        self.dim_producto_ancho = 0.0
        self.dim_producto_largo = 0.0
        self.dim_producto_alto = 0.0
        
        self.volumen_buenos_aires = volumen_buenos_aires
        self.volumen_curitiba = volumen_curitiba
        self.volumen_santiago = volumen_santiago
        self.volumen_monterrey = volumen_monterrey
        self.volumen_bakersfield = volumen_bakersfield
        
        self.caja = None
    
    def asignar_caja(self, caja_id):
        caja = Caja.buscar_por_id(caja_id)
        self.dim_producto_ancho = caja.dim_interior_ancho
        self.dim_producto_largo = caja.dim_interior_largo
        self.dim_producto_alto = caja.dim_interior_alto
        self.caja = caja
        
    def es_caja_asignable(self, caja):
        entra = (self.dim_producto_alto <= caja.dim_interior_alto and
                 self.dim_producto_ancho <= caja.dim_interior_ancho and
                 self.dim_producto_largo <= caja.dim_interior_largo)
        maximo_en_10 = (self.dim_producto_alto * 1.1 >= caja.dim_interior_alto and
                        self.dim_producto_ancho * 1.1 >= caja.dim_interior_ancho and
                        self.dim_producto_largo * 1.1 >= caja.dim_interior_largo)
        return entra and maximo_en_10