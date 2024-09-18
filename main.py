import argparse
import json
import sched
import socket
import time
from actors.search_actors import SearchActor, parse_fullh4rd, parse_mercadolibre, parse_shoppingnet, parse_4krc, parse_gamingcity
from actors.storage_actor import StorageActor
from actors.compare_actor import CompareActor

# Configuración de argumentos para modo cliente o servidor
parser = argparse.ArgumentParser(description="Modo de ejecución: Servidor o Cliente")
parser.add_argument('--mode', choices=['server', 'client'], required=True, help="Modo de ejecución: server o client")
args = parser.parse_args()

# Dirección y puerto del servidor
SERVER_IP = ''
SERVER_PORT = 65432

def run_server():
    # Configuración del socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Servidor escuchando en {SERVER_IP}:{SERVER_PORT}")

    # Crear instancias de actores de almacenamiento
    storage_actors = {
        'Mouse': StorageActor.start('data/mouse_price_data.txt'),
        'Teclado': StorageActor.start('data/teclado_price_data.txt'),
        'Auriculares': StorageActor.start('data/auriculares_price_data.txt')
    }

    def handle_client_connection(client_socket):
        while True:
            # Recibir el mensaje del cliente
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            try:
                # Convertir el mensaje de JSON a diccionario
                data = json.loads(message)
                product_name = data.get('product', '')
                if product_name in storage_actors:
                    # Enviar datos al actor de almacenamiento correspondiente
                    storage_actors[product_name].tell(data)
                    print(f"Datos recibidos y guardados para {product_name}: {data}")
            except Exception as e:
                print(f"Error al procesar mensaje: {e}")

        client_socket.close()

    # Manejar conexiones entrantes
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexión establecida con {addr}")
        handle_client_connection(client_socket)

def run_client():
    # Conexión con el servidor
    def send_to_server(data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP, SERVER_PORT))
            message = json.dumps(data)
            client_socket.sendall(message.encode('utf-8'))
            print(f"Enviado al servidor: {data}")

    # Leer configuración desde config.json
    with open('config/config.json', 'r') as config_file:
        config = json.load(config_file)

    # Crear instancias de actores de búsqueda
    search_actors = []

    for product in config['products']:
        product_name = product['name']
        
        for source in product['sources']:
            if 'fullh4rd' in source:
                search_actors.append(SearchActor.start(product_name, source, parse_fullh4rd))
            elif 'mercadolibre' in source:
                search_actors.append(SearchActor.start(product_name, source, parse_mercadolibre))
            elif 'shoppingnet' in source:
                search_actors.append(SearchActor.start(product_name, source, parse_shoppingnet))
            elif 'shop.4krc' in source:
                search_actors.append(SearchActor.start(product_name, source, parse_4krc))
            elif 'gamingcity' in source:
                search_actors.append(SearchActor.start(product_name, source, parse_gamingcity))

    # Función de búsqueda programada
    def schedule_search(scheduler):
        for actor in search_actors:
            result = actor.ask({'action': 'fetch_price'})
            # Enviar el resultado al servidor
            send_to_server(result)
            
        scheduler.enter(30, 1, schedule_search, (scheduler,))

    # Programar la búsqueda de precios cada 30 segundos
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_search, (scheduler,))
    scheduler.run()

# Ejecutar según el modo especificado
if args.mode == 'server':
    run_server()
elif args.mode == 'client':
    run_client()

