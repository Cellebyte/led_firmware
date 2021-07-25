import json

import uasyncio
import gc


class Store:
    state_file = "state.json"
    max_count = 240

    def __init__(self, debug=False) -> None:
        self.state = {}
        try:
            with open(self.state_file, "r") as file:
                self.state = json.load(file)
        except OSError as e:
            print("Cannot find state file {}".format(e))
        self.debug = debug

    async def load_state(self):
        try:
            with open(self.state_file, "r") as file:
                return json.loads(file.read())
        except OSError as e:
            print("Cannot find state file {}".format(e))
        return {}

    async def start(self):
        count = 0
        while True:
            count += 1
            if count >= self.max_count:
                count = 0
            await self.loop(count)
            gc.collect()
            await uasyncio.sleep_ms(15)

    def save(self, key, objects):
        self.state[key] = objects

    def load(self, key, default=None):
        return self.state.get(key, default)

    def store_state(self):
        with open(self.state_file, "w") as file:
            file.write(json.dumps(self.state))

    async def loop(self, count):
        if count % self.max_count == 1:
            if self.state != (await self.load_state()):
                self.store_state()
                print("Saved state! ;)")
            else:
                print("State on Disk is the same as the store.")
        if self.debug:
            print("Hello from Store :: {}".format(count))
