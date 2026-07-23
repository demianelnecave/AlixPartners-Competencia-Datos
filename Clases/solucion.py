import pandas as pd  # type: ignore[reportMissingImports]
from Clases.asignacion import Asignacion

catalogo_productos = pd.read_csv("Datos-finales/catalogo_productos.csv")
operaciones_planta = pd.read_csv("Datos-finales/operaciones_planta.csv").drop('codigo_producto', axis=1) 
prod_op_merge = pd.concat([catalogo_productos, operaciones_planta], axis=1)

class Solucion:
    def __init__(self, grosor=None):
        self.grosor_elegido = grosor
        self.asignaciones = []
        self.tipos_cajas_utilizados = []
        self.cantidad_tipos_cajas = 0   
        
        self.cantidad_tipos_cajas_original = 204
        self.costo_packaging_original = 30295472.424999997
        self.costo_flete_original = 179068800
        self.costo_total_original = 209364272.425
        self.utilizacion_pallet_promedio_original = 0.8369364400001816
    
    def agregar_asignacion(self, asignacion, descuentos=True):
        if descuentos == True: 
            asignacion.caja.asignar_producto(asignacion.producto)
            
        self.asignaciones.append(asignacion)
        if asignacion.caja not in self.tipos_cajas_utilizados:
            self.tipos_cajas_utilizados.append(asignacion.caja)
            self.cantidad_tipos_cajas += 1
    
    def costo_packaging(self):
        costo = 0
        for asignacion in self.asignaciones:
            costo += asignacion.costo_packaging_producto_total()
        return costo
    
    def costo_flete(self):
        costo = 0
        for asignacion in self.asignaciones:
            costo += 150 * asignacion.cant_pallets_requeridas()
        return costo
    
    def costo_total(self):
        return self.costo_packaging() + self.costo_flete()
    
    def utilizacion_pallet_promedio(self):
        total = 0
        for caja in self.tipos_cajas_utilizados:
            total += caja.utilizacion_pallet()
        return total / self.cantidad_tipos_cajas

    def resumen_por_asignacion(self):
        datos = []
        for asignacion in self.asignaciones:
            producto = asignacion.producto
            caja = asignacion.caja
            costo_packaging = asignacion.costo_packaging_producto_total()
            cant_pallets = asignacion.cant_pallets_requeridas()
            datos.append({
                'codigo_producto': producto.codigo_producto,
                'volumen_producto_total': producto.demanda_total(),
                'demanda_total': producto.demanda_total(),
                'caja_id': caja.caja_id,
                'utilizacion_pallet': caja.utilizacion_pallet(),
                'utilizacion_caja': asignacion.utilizacion_caja(),
                'costo_packaging': costo_packaging,
                'cant_pallets': cant_pallets,
                'costo_flete': 150 * cant_pallets,
                'costo_total': costo_packaging + 150 * cant_pallets
            })
        
        df_resultados = pd.DataFrame(datos)
        df_resultados = prod_op_merge[['codigo_producto', 'volumen_producto_total']].merge(
            df_resultados, 
            on=['codigo_producto', 'volumen_producto_total'], 
            how='inner'
        ).drop('volumen_producto_total', axis=1) 
        
        return df_resultados
    
    def resumen_general(self):
        print("Situación original")
        print("-" * 50)
        print(f"Número de tipos de cajas distintos: {self.cantidad_tipos_cajas_original}")
        print(f"Costo packaging: {self.costo_packaging_original}")
        print(f"Costo flete: {self.costo_flete_original}")
        print(f"Costo total: {self.costo_total_original}")
        print(f"Utilización de pallet promedio: {self.utilizacion_pallet_promedio()}")

        print("\nSituación nueva")
        print("-" * 50)
        print(f"Número de tipos de cajas distintos: {self.cantidad_tipos_cajas}")
        print(f"Costo packaging: {self.costo_packaging()}")
        print(f"Costo flete: {self.costo_flete()}")
        print(f"Costo total: {self.costo_total()}")
        print(f"Utilización de pallet promedio: {self.utilizacion_pallet_promedio()}")
            
    def exportar_submmit(self, nombre_csv):
        datos = []
        for asignacion in self.asignaciones:
            producto = asignacion.producto
            caja = asignacion.caja
            datos.append({
                'codigo_producto': producto.codigo_producto,
                'volumen_producto_total': producto.demanda_total(),
                'caja_grosor_mm': caja.grosor_mm,
                'caja_exterior_largo': caja.dim_exterior_largo,
                'caja_exterior_ancho': caja.dim_exterior_ancho,
                'caja_exterior_alto': caja.dim_exterior_alto
            })

        df_resultados = pd.DataFrame(datos)
        
        df_resultados = prod_op_merge[['codigo_producto', 'volumen_producto_total']].merge(
            df_resultados, 
            on=['codigo_producto', 'volumen_producto_total'], 
            how='inner'
        ).drop('volumen_producto_total', axis=1) 
        
        df_resultados.to_csv(f"Soluciones/solucion{nombre_csv}.csv", index=False)