import pykka
from datetime import datetime

class StorageActor(pykka.ThreadingActor):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def on_receive(self, message):
        if 'price' in message:
            # Obtener la fecha y la hora actuales
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Guardar el precio con la fecha y hora
            with open(self.file_path, 'a') as f:
                f.write(f"{current_time}, {message['product']}, {message['source']}, {message['price']:.2f}\n")
            print(f"Datos guardados: {message}")
