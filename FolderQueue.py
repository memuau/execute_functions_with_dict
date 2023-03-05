import os
import json
from shutil import move

class FolderQueue:
    def __init__(self, path_to_folder):
        self.new = path_to_folder + "/new/"
        self.processed = path_to_folder + "/processed/"
        self.previous_command_name = ""

    def __call__(self) -> dict:
        if filename := self.previous_command_name:
            move(self.new + filename, self.processed + filename)
        new_commands = [filename for filename in os.listdir(self.new) if filename.endswith(".json")]
        if not new_commands:
            self.previous_command_name = ""
            yield dict()
        with open(self.new + new_commands[0], "r") as f:
            self.previous_command_name = new_commands[0]
            yield json.load(f)
