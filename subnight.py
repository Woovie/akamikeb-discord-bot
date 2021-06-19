import os.path

class Subnight():
    def __init__(self):
        self.subnight_file = "game.txt"

    def set(self, game: str) -> bool:
        with open(self.subnight_file, 'w') as openfile:
            openfile.write(game)
        with open(self.subnight_file, 'r') as openfile:
            if openfile.read() == game:
                return True
            else:
                return False

    def get(self) -> str:
        if os.path.exists(self.subnight_file):
            with open(self.subnight_file, 'r') as openfile:
                return openfile.read()
        else:
            with open(self.subnight_file, 'w') as openfile:
                openfile.write("")
                return ""
