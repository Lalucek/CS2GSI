from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cs2gsi import GameState, GSIServer  # noqa: E402


def print_raw_weapons(state: GameState) -> None:
    player = state.raw.get("player")
    weapons = player.get("weapons") if isinstance(player, dict) else None
    if weapons:
        print(json.dumps(weapons))


def main() -> None:
    server = GSIServer("127.0.0.1", 8004)
    server.subscribe(print_raw_weapons)
    print(f"Starting GSI server for weapon info on {server.host}:{server.port}...")
    server.run()


if __name__ == "__main__":
    main()
