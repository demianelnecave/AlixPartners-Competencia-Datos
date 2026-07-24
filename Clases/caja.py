import copy
import numpy as np  # type: ignore[reportMissingImports]

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
    def __init__(self, caja_id, dim_interior_ancho, dim_interior_largo, dim_interior_alto, costo_unitario=None):
        
        self.caja_id = caja_id
        self.dim_interior_ancho = dim_interior_ancho
        self.dim_interior_largo = dim_interior_largo
        self.dim_interior_alto = dim_interior_alto
        
        self.grosor_mm = 0.0
        self.dim_exterior_ancho = 0.0
        self.dim_exterior_largo = 0.0
        self.dim_exterior_alto = 0.0
        
        self.unidades_buenos_aires_req = 0
        self.unidades_curitiba_req = 0
        self.unidades_santiago_req = 0
        self.unidades_monterrey_req = 0
        self.unidades_bakersfield_req = 0
        
        self.costo_unitario = 0.0
        if costo_unitario != None:
            self.costo_unitario = costo_unitario
        self.descuento_buenos_aires = 0.0
        self.descuento_curitiba = 0.0
        self.descuento_santiago = 0.0
        self.descuento_monterrey = 0.0
        self.descuento_bakersfield = 0.0
        
        self.productos_asignados = []
            
    def elegir_grosor(self, grosor_mm):
        self.grosor_mm = grosor_mm
        self.dim_exterior_ancho = self.dim_interior_ancho + 2 * grosor_mm
        self.dim_exterior_largo = self.dim_interior_largo + 2 * grosor_mm
        self.dim_exterior_alto = self.dim_interior_alto + 2 * grosor_mm
        
        costo_unitario_por_grosor = {3.0: 0.6, 4.5: 0.65, 5.0: 0.7}
        self.costo_unitario = costo_unitario_por_grosor[grosor_mm]
    
    def volumen_interno(self):
        return self.dim_interior_alto * self.dim_interior_ancho * self.dim_interior_largo
    
    def volumen_externo(self):
        '''
        Pre: El grosor debe ser previamente elegido.
        '''
        return self.dim_exterior_alto * self.dim_exterior_ancho * self.dim_exterior_largo   
    
    def perimetro(self):
        return (self.dim_exterior_ancho + self.dim_exterior_largo) * 2
    
    def carga_maxima(self):
        ect_por_grosor = {2.5: 600, 2.7: 730, 3.0: 1000, 4.1: 1200, 4.5: 1400, 
                          4.6: 1450, 4.7: 1500, 4.8: 1550, 5.0: 1650}
        ect = ect_por_grosor[self.grosor_mm]
        return ect * self.perimetro() / 9.81

    def redimensionar(self, nuevo_alto, nuevo_ancho, nuevo_largo):
        self.dim_interior_alto = nuevo_alto
        self.dim_interior_ancho = nuevo_ancho
        self.dim_interior_largo = nuevo_largo
        
        if self.grosor_mm != 0.0:
            self.dim_exterior_ancho = self.dim_interior_ancho + 2 * self.grosor_mm
            self.dim_exterior_largo = self.dim_interior_largo + 2 * self.grosor_mm
            self.dim_exterior_alto = self.dim_interior_alto + 2 * self.grosor_mm
            
    def cantidad_cajas_por_pallet(self):
        '''
        Pre: El grosor debe ser previamente elegido.
        '''
        cant_cajas_alto = 1800 // self.dim_exterior_alto
        cant_cajas_ancho = 1200 // self.dim_exterior_ancho
        cant_cajas_largo = 800 // self.dim_exterior_largo
        cant_cajas_pallet = cant_cajas_alto * cant_cajas_ancho * cant_cajas_largo
        return cant_cajas_pallet

    def maxima_cantidad_cajas_por_pallet(self, dimension):
        '''
        Pre: El grosor debe ser previamente elegido.
        '''
        caja_redimensionada = copy.deepcopy(self)
        caja_redimensionada.redimensionar(self.dim_interior_alto * 1.1, 
                                          self.dim_interior_ancho * 1.1, 
                                          self.dim_interior_largo * 1.1)
        
        if dimension == 'alto':
            res = 1800 // caja_redimensionada.dim_exterior_alto
        elif dimension == 'ancho':
            res = 1200 // caja_redimensionada.dim_exterior_ancho
        elif dimension == 'largo':
            res = 800 // caja_redimensionada.dim_exterior_largo
        
        return int(res)
    
    def utilizacion_pallet(self):
        '''
        Pre: El grosor debe ser previamente elegido.
        '''
        volumen_caja = self.dim_exterior_alto * self.dim_exterior_ancho * self.dim_exterior_largo
        volumen_cajas = volumen_caja * self.cantidad_cajas_por_pallet()
        volumen_pallet = 1800 * 1200 * 800
        return volumen_cajas / volumen_pallet

    def puntos_quiebre(self, dimension):
        """ 
        Encuentra valores donde cambia el número de cajas.
        n=3 -> 1200/3 = 400 mm  (entran 3 cajas) -> Punto de quiebre
        n=4 -> 1200/4 = 300 mm  (entran 4 cajas) -> Punto de quiebre
        n=5 -> 1200/5 = 240 mm  (entran 5 cajas) -> Punto de quiebre
        """
        puntos = []
        dim_original = self.__dict__[f'dim_interior_{dimension}']
        
        # Probar diferentes números de cajas por fila, hasta el máximo de lo permitido
        for n in range(1, self.maxima_cantidad_cajas_por_pallet(dimension) + 1):
            if dimension == 'alto': punto = 1800 / n
            elif dimension == 'ancho': punto = 1200 / n
            elif dimension == 'largo': punto = 800 / n
            
            # Si el punto está dentro del ±10%
            if dim_original * 0.9 <= punto <= dim_original * 1.1:
                puntos.append(punto)
        
        # Si no hay puntos, usamos el original y los límites
        if not puntos:
            puntos = [dim_original * 0.9, dim_original, dim_original * 1.1]
        
        # Redondear a 1 decimal y eliminar duplicados
        puntos = np.round(puntos, 1)
        puntos = np.unique(puntos)
        return puntos

    def buscar_redimensionamiento_optimo(self):           
        # Obtener puntos de quiebre
        opciones_alto = self.puntos_quiebre('alto')
        opciones_ancho = self.puntos_quiebre('ancho')
        opciones_largo = self.puntos_quiebre('largo')
        
        combinaciones = []
        mejor_opcion = []
        mejor_utilizacion_pallet = 0
        
        for alto in opciones_alto:
            for ancho in opciones_ancho:
                for largo in opciones_largo:
                    caja_redimensionada = copy.deepcopy(self)
                    caja_redimensionada.redimensionar(alto, ancho, largo)
                    
                    # Evaluamos según la métrica de utilizacion de pallet
                    utilizacion = caja_redimensionada.utilizacion_pallet()
                    if utilizacion > mejor_utilizacion_pallet:
                        mejor_utilizacion_pallet = utilizacion
                        mejor_opcion = [alto, ancho, largo, utilizacion]
                    
                    combinacion = {'alto': caja_redimensionada.dim_interior_alto, 
                                   'ancho': caja_redimensionada.dim_interior_ancho, 
                                   'largo': caja_redimensionada.dim_interior_largo, 
                                   'utilizacion_pallet': utilizacion}
                    combinaciones.append(combinacion)

        combinaciones_ordenadas = sorted(combinaciones, key=lambda x: x['utilizacion_pallet'], reverse=True)
        return mejor_opcion, combinaciones_ordenadas

    def unidades_total_requeridas(self):
        return (self.unidades_buenos_aires_req + self.unidades_curitiba_req + self.unidades_santiago_req +
                self.unidades_monterrey_req + self.unidades_bakersfield_req)
        
    def asignar_producto(self, producto):
        '''
        Pre: La asignación debe ser antes validada.
        '''
        self.productos_asignados.append(producto)
        plantas = ['buenos_aires', 'curitiba', 'santiago', 'monterrey', 'bakersfield']
        for planta in plantas:
            self.__dict__[f'unidades_{planta}_req'] += producto.__dict__[f'demanda_{planta}']
            self.__dict__[f'descuento_{planta}'] = calcular_descuento_por_volumen(self.__dict__[f'unidades_{planta}_req'])

    def revocar_producto(self, producto):
        if producto in self.productos_asignados:
            self.productos_asignados.remove(producto)
            plantas = ['buenos_aires', 'curitiba', 'santiago', 'monterrey', 'bakersfield']
            for planta in plantas:
                self.__dict__[f'unidades_{planta}_req'] -= producto.__dict__[f'demanda_{planta}']
                self.__dict__[f'descuento_{planta}'] = calcular_descuento_por_volumen(self.__dict__[f'unidades_{planta}_req'])
        else:
            print("El producto no utiliza este tipo de caja.")
    
    def costo_packaging_planta(self, planta):
        unidades = getattr(self, f'unidades_{planta}_req')
        descuento = getattr(self, f'descuento_{planta}')
        precio_con_descuento = self.costo_unitario * (1 + descuento)
        costo = unidades * precio_con_descuento
        return costo
    
    def costo_packaging_total(self):
        costo = 0
        plantas = ['buenos_aires', 'curitiba', 'santiago', 'monterrey', 'bakersfield']
        for planta in plantas:
            unidades_requeridas = getattr(self, f'unidades_{planta}_req')
            descuento = getattr(self, f'descuento_{planta}')
            precio_con_descuento = self.costo_unitario * (1 + descuento)
            costo += unidades_requeridas * precio_con_descuento
        return costo
    
    def __repr__(self):
        return (f"<Caja {self.caja_id} | "
                f"Int: {self.dim_interior_ancho} x {self.dim_interior_largo} x {self.dim_interior_alto}mm | "
                f"Compra Total: {self.unidades_total_requeridas()}>")