import pykka

class CompareActor(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()

    def on_receive(self, message):
        # Simplemente recibe los mensajes de los precios sin hacer ninguna operación
        pass