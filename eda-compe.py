#%%
import pandas as pd 
import numpy as np
#%%
path = "Datos-finales/"
catalogo_productos = pd.read_csv(f"{path}catalogo_productos.csv")
especificaciones_cajas = pd.read_csv(f"{path}especificaciones_cajas.csv")
operaciones_planta = pd.read_csv(f"{path}operaciones_planta.csv")
procurement_cajas = pd.read_csv(f"{path}procurement_cajas.csv")

#%%
ids = catalogo_productos['codigo_producto']
#%%
'''
medidas no siguen un formato único
'''
especificaciones_cajas['caja_grosor_mm'].unique()
#%%
import re

def normalizar_medida(valor):
    v = valor.strip()
    v = re.sub(r'mm', '', v, flags=re.IGNORECASE)  # saca "mm"
    v = v.strip()
    v = v.replace(',', '.')  # unifica separador decimal
    return float(v)

especificaciones_cajas['caja_grosor_mm'] = especificaciones_cajas['caja_grosor_mm'].apply(normalizar_medida)
#%%

especificaciones_cajas['cantidad_cajas_largo'].unique()


especificaciones_cajas['cantidad_cajas_ancho'].unique()


especificaciones_cajas['cantidad_cajas_alto'].unique()


especificaciones_cajas['cantidad_cajas_total'].unique()
#%%
PALLET_LARGO = 1200
PALLET_ANCHO = 800
PALLET_ALTURA_MAX = 1800
 
 
def chequear_espesor_pared(df):
    """
    Compara, por eje, la diferencia real exterior-interior contra 2*grosor.
    """
    resultados = []
    for eje, col_int, col_ext in [
        ("largo", "caja_interior_largo", "caja_exterior_largo"),
        ("ancho", "caja_interior_ancho", "caja_exterior_ancho"),
        ("alto", "caja_interior_alto", "caja_exterior_alto"),
    ]:
        diff_real = df[col_ext] - df[col_int]
        diff_esperada = 2 * df["caja_grosor_mm"]
        delta = diff_real - diff_esperada
 
        resultados.append(pd.DataFrame({
            "caja_tipo_id": df["caja_tipo_id"],
            "eje": eje,
            "diff_real": diff_real,
            "diff_esperada": diff_esperada,
            "delta": delta,  # negativo = redondeó hacia abajo, positivo = hacia arriba
        }))
 
    df_check = pd.concat(resultados, ignore_index=True)
 
    print("=== Resumen de delta (diff_real - diff_esperada) por eje ===")
    print(df_check.groupby("eje")["delta"].describe())
    print()
 
    # Cuántos tipos de caja tienen AL MENOS un eje con delta != 0 (tolerancia 0.05mm)
    tol = 0.05
    df_check["desvia"] = df_check["delta"].abs() > tol
    pct_por_eje = df_check.groupby("eje")["desvia"].mean() * 100
    print("=== % de filas que se desvían de 'exterior = interior + 2*grosor' (tol 0.05mm) ===")
    print(pct_por_eje.round(1).astype(str) + "%")
    print()
 
    # Signo del desvío: ¿hay un sesgo sistemático hacia abajo o hacia arriba?
    desviadas = df_check[df_check["desvia"]]
    if len(desviadas) > 0:
        print("=== Signo del desvío (entre las filas que se desvían) ===")
        print(desviadas.groupby("eje")["delta"].apply(lambda x: (x < 0).mean() * 100).round(1).astype(str) + "% redondea hacia abajo")
 
    return df_check
 
 
def chequear_apilado(df):
    """
    Recalcula cantidad_cajas_* y utilizacion a partir de las dimensiones
    exteriores reportadas, y compara contra lo que ya viene en el archivo.
    """
    df = df.copy()
 
    df["calc_cajas_ancho"] = (PALLET_ANCHO // df["caja_exterior_largo"]).astype(int)
    df["calc_cajas_largo"] = (PALLET_LARGO // df["caja_exterior_ancho"]).astype(int)
    df["calc_cajas_alto"] = (PALLET_ALTURA_MAX // df["caja_exterior_alto"]).astype(int)
    df["calc_cajas_total"] = df["calc_cajas_ancho"] * df["calc_cajas_largo"] * df["calc_cajas_alto"]
 
    vol_pallet = PALLET_LARGO * PALLET_ANCHO * PALLET_ALTURA_MAX
    vol_cajas = df["caja_exterior_largo"] * df["caja_exterior_ancho"] * df["caja_exterior_alto"] * df["calc_cajas_total"]
    df["calc_utilizacion"] = vol_cajas / vol_pallet
 
    df["match_cajas_total"] = np.isclose(df["calc_cajas_total"], df["cantidad_cajas_total"])
    df["match_utilizacion"] = np.isclose(df["calc_utilizacion"], df["utilizacion"], atol=1e-4)
 
    n = len(df)
    print(f"=== Chequeo de apilado ({n} tipos de caja) ===")
    print(f"cantidad_cajas_total coincide: {df['match_cajas_total'].sum()}/{n} ({df['match_cajas_total'].mean():.1%})")
    print(f"utilizacion coincide:          {df['match_utilizacion'].sum()}/{n} ({df['match_utilizacion'].mean():.1%})")
    print()
 
    if not df["match_cajas_total"].all():
        print("Filas donde NO coincide cantidad_cajas_total (revisar orientación o redondeo):")
        cols = ["caja_tipo_id", "cantidad_cajas_largo", "cantidad_cajas_ancho", "cantidad_cajas_alto",
                "cantidad_cajas_total", "calc_cajas_largo", "calc_cajas_ancho", "calc_cajas_alto", "calc_cajas_total"]
        print(df.loc[~df["match_cajas_total"], cols].head(20).to_string(index=False))
 
    return df
 
 
if __name__ == "__main__":
     
    df_espesor = chequear_espesor_pared(especificaciones_cajas)
    df_apilado = chequear_apilado(especificaciones_cajas)
 
    
 #%%
'''
Valores NaN en cantidad total de cajas se calculan
'''
cant_cajas_total_is_nan = especificaciones_cajas['cantidad_cajas_total'].isna()
cant_cajas_total_nan = especificaciones_cajas.loc[cant_cajas_total_is_nan]

cant_cajas_largo = cant_cajas_total_nan['cantidad_cajas_largo']
cant_cajas_ancho = cant_cajas_total_nan['cantidad_cajas_ancho']
cant_cajas_alto = cant_cajas_total_nan['cantidad_cajas_alto']
cant_cajas_total_nan['cantidad_cajas_total'] = cant_cajas_alto * cant_cajas_ancho * cant_cajas_largo

especificaciones_cajas.loc[cant_cajas_total_is_nan] = cant_cajas_total_nan
 #%%
'''
 Hay un par de medidas exteriores que no cuadran exacto con el cálculo
 
         medida_ext = medida_int + 2*grosor_lado
 '''
 
desviados = df_espesor.loc[df_espesor['desvia'] == True, 'caja_tipo_id']

especificaciones_cajas[]