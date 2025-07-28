import pandas as pd

# Ruta al archivo CSV
csv_path = 'static/dataset_vinos_limpio.csv'

def limpiar_nombre_completo(path):
    df = pd.read_csv(path)
    if 'nombre_completo' in df.columns:
        df['nombre_completo'] = df['nombre_completo'].astype(str).str.split(',').str[0]
        nuevo_path = 'static/dataset_vinos_limpio_nombre.csv'
        df.to_csv(nuevo_path, index=False)
        print(f'Columna "nombre_completo" limpiada correctamente. Archivo guardado en {nuevo_path}')
    else:
        print('La columna "nombre_completo" no existe en el archivo.')

if __name__ == '__main__':
    limpiar_nombre_completo(csv_path)
