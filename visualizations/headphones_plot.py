import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

def plot_price_history(file_path):
    # Leer datos del archivo, ahora con la fecha y hora incluidas
    data = pd.read_csv(file_path, header=None, names=['datetime', 'product', 'source', 'price'], parse_dates=['datetime'])
    
    # Asegurarse de que todos los datos de precios sean cadenas de texto
    data['price'] = data['price'].astype(str)

    # Eliminar caracteres no numéricos y convertir a tipo float, ignorando filas con valores vacíos
    data['price'] = data['price'].str.replace(',', '').str.replace(r'[^\d.]', '', regex=True)
    data = data[data['price'] != '']  # Eliminar filas con valores vacíos en 'price'
    data['price'] = data['price'].astype(float)

    # Crear un gráfico de líneas combinando los tres productos y sus fuentes
    plt.figure(figsize=(12, 8))
    
    # Graficar cada combinación de producto y fuente
    for product in data['product'].unique():
        product_data = data[data['product'] == product]
        
        for source in product_data['source'].unique():
            source_data = product_data[product_data['source'] == source]
            # Simplificar la etiqueta de la fuente
            source_label = source.split('/')[2]  # Toma solo el dominio para acortar la etiqueta
            plt.plot(source_data['datetime'], source_data['price'], label=f'{product} - {source_label}')
    
    # Configurar el formato del eje Y para evitar notación científica y mantener escala logarítmica para mejor visualización
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:,.2f}'.format(y)))  # Formato en decimales

    plt.title('Historial de precios de productos')
    plt.xlabel('Fecha y hora')
    plt.ylabel('Precio')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotar las etiquetas del eje X para mejor lectura
    plt.show()

if __name__ == "__main__":
    # Llamada a la función de visualización
    plot_price_history('data/auriculares_price_data.txt')
