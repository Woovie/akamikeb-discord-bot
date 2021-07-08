import os.path
import json

class Subnight():
    def __init__(self):
        self.subnight_file = "game.json"
        self.data = {}
        self.get()

    def set(self, game: dict):
        with open(self.subnight_file, 'w') as openfile:
            openfile.write(json.dumps(game))
            self.data = game

    def get(self):
        if os.path.exists(self.subnight_file):
            with open(self.subnight_file, 'r') as openfile:
                self.data = json.loads(openfile.read())
        else:
            with open(self.subnight_file, 'w') as openfile:
                seed_data = {"name": "", "url": ""}
                openfile.write(json.dumps(seed_data))
                self.data = seed_data
