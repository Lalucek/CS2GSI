from aiohttp import web
from threading import Thread
from . import JSONparser as jp

class GSIListener:
    def __init__(self, host, port, token=None):
        self.host = host
        self.port = port
        self.token = token
        self.parser = jp.PayloadParser()
        self.gs_object = None
        self.first_packet = True
    async def handle_data(self, request):
        try:
            data = await request.json()
            #if self.first_packet:
            #    print(data)
            #    self.first_packet = False
            self.gs_object = self.parser.parseData(data)
            if(self.first_packet):
                print(self.gs_object.phase_info.phase)
                self.first_packet = False
            return web.Response(text="Payload received", status=200)
        except Exception as e:
            print(f"Error: {e}")
            return web.Response(text="Server error: " + str(e), status=500)

    def start(self):
        app = web.Application()
        app.router.add_post('/', self.handle_data)
        web.run_app(app, host=self.host, port=self.port)

if __name__ == "__main__":
    listener = GSIListener("127.0.0.1", 8080)
    listener.start()