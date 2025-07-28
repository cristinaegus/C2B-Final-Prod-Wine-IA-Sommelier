import pandas as pd

# Cargar el dataset original
csv_path = 'static/dataset_vinos_combinado_ultra_limpio_20250717_122604.csv'
df = pd.read_csv(csv_path)

# Eliminar duplicados por nombre_completo, año y bodega
df_sin_duplicados = df.drop_duplicates(subset=['nombre_completo', 'año', 'bodega'])

# Guardar el resultado en un nuevo archivo
output_path = 'static/dataset_vinos_limpieza_total_final.csv'
df_sin_duplicados.to_csv(output_path, index=False)

print(f"Vinos únicos: {len(df_sin_duplicados)}")
print(f"Archivo guardado en: {output_path}")
