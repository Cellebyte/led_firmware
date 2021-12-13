import json
from typing import Any

import uasyncio
from errors import MISSING_STATE_FILE


class Store:
    state_file = "state.json"
    max_count = 240

    def __init__(self) -> None:
        self.state = {}
        try:
            with open(self.state_file, "r") as file:
                self.state = json.load(file)
        except OSError as e:
            print(MISSING_STATE_FILE.format(e))

    async def load_state(self):
        try:
            with open(self.state_file, "r") as file:
                return json.loads(file.read())
        except OSError as e:
            print(MISSING_STATE_FILE.format(e))
        return {}

    async def start(self):
        count = 0
        while True:
            count += 1
            if count >= self.max_count:
                count = 0
            await self.loop(count)
            await uasyncio.sleep_ms(100)

    def save(self, key: str, objects: Any):
        self.state[key] = objects

    def delete(self, key: str) -> Any:
        return self.state.pop(key, None)

    def load(self, key: str, default: Any) -> Any:
        return self.state.get(key, default)

    def store_state(self):
        with open(self.state_file, "w") as file:
            file.write(json.dumps(self.state))

    async def loop(self, count):
        if count % self.max_count == 1:
            if self.state != (await self.load_state()):
                self.store_state()
                print("State is Updated!")
            else:
                print("State is Current!")
