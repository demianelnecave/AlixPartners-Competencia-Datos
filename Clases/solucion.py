import pandas as pd  # type: ignore[reportMissingImports]
from Clases.asignacion import Asignacion

catalogo_productos = pd.read_csv("Datos-finales/catalogo_productos.csv")
operaciones_planta = pd.read_csv("Datos-finales/operaciones_planta.csv").drop('codigo_producto', axis=1) 
prod_op_merge = pd.concat([catalogo_productos, operaciones_planta], axis=1)

class Solucion:
    def __init__(self, grosor):
        self.grosor_elegido = grosor
        self.asignaciones = []
        self.tipos_cajas_utilizados = []
        self.cantidad_tipos_cajas = 0   
        
        self.costo_packaging_original = 0.0
        self.costo_flete_original = 0.0
        self.costo_total_original = 0.0
    
    def agregar_asignacion(self, producto, caja, descuentos=True):
        if descuentos == True: 
            caja.asignar_producto(producto)
            
        asignacion = Asignacion(producto, caja)
        self.asignaciones.append(asignacion)
        if caja not in self.tipos_cajas_utilizados:
            self.tipos_cajas_utilizados.append(caja)
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
        return None
            
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