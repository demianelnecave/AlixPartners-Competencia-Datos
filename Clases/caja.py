class Caja:
    _todas_las_cajas = {}
    
    def __init__(self, caja_id, dim_interior_ancho, dim_interior_largo, dim_interior_alto, grosor_mm):
        self.caja_id = caja_id
        self.dim_interior_ancho = dim_interior_ancho
        self.dim_interior_largo = dim_interior_largo
        self.dim_interior_alto = dim_interior_alto
        
        self.grosor_mm = grosor_mm
        self.dim_exterior_ancho = dim_interior_ancho + 2 * grosor_mm
        self.dim_exterior_largo = dim_interior_largo + 2 * grosor_mm
        self.dim_exterior_alto = dim_interior_alto + 2 * grosor_mm
        
        Caja._todas_las_cajas[caja_id] = self
    
    def cambiar_grosor(self, grosor_mm):
        self.grosor_mm = grosor_mm
        self.dim_exterior_ancho = self.dim_interior_ancho + 2 * grosor_mm
        self.dim_exterior_largo = self.dim_interior_largo + 2 * grosor_mm
        self.dim_exterior_alto = self.dim_interior_alto + 2 * grosor_mm
    
    def dimension_interna(self):
        return self.dim_interior_alto * self.dim_interior_ancho * self.dim_interior_largo
    
    def dimension_externa(self):
        return self.dim_exterior_alto * self.dim_exterior_ancho * self.dim_exterior_largo   
    
    def perimetro(self):
        return (self.dim_exterior_ancho + self.dim_exterior_largo) * 2
    
    def carga_maxima(self):
        ect_por_grosor = {2.5: 600, 2.7: 730, 3.0: 1000, 4.1: 1200, 4.5: 1400, 
                          4.6: 1450, 4.7: 1500, 4.8: 1550, 5.0: 1650}
        ect = ect_por_grosor[self.grosor_mm]
        return ect / self.perimetro() / 9.81
    
    def __repr__(self):
        return (f"<Caja {self.caja_id} | "
                f"Int: {self.dim_interior_ancho}x{self.dim_interior_largo}x{self.dim_interior_alto}mm | "
                f"Ext: {self.dim_exterior_ancho}x{self.dim_exterior_largo}x{self.dim_exterior_alto}mm | "
                f"Grosor: {self.grosor_mm}mm>")

    @classmethod
    def buscar_por_id(cls, caja_id):
        return cls._todas_las_cajas.get(caja_id)