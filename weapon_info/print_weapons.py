import sys
import os
import json
from aiohttp import web

# Add parent directory to path to import cs2gsi
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cs2gsi.GSIReader import GSIListener


class WeaponInfoListener(GSIListener):
    async def handle_data(self, request):
        try:
            data = await request.json()

            # Parse using the library
            self.gs_object = self.parser.parseData(data)

            # Print raw weapons data
            if (
                self.gs_object
                and self.gs_object.player
                and self.gs_object.player.playerWeapons
            ):
                raw_weapons = self.gs_object.player.playerWeapons.raw_weapons
                if raw_weapons:
                    print(json.dumps(raw_weapons))

            return web.Response(text="Payload received", status=200)
        except Exception as e:
            print(f"Error: {e}")
            return web.Response(text="Server error: " + str(e), status=500)


if __name__ == "__main__":
    print("Starting GSI server for weapon info on 127.0.0.1:8004...")
    listener = WeaponInfoListener("127.0.0.1", 8004)
    listener.start()
