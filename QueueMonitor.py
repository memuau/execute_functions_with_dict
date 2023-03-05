from time import sleep
import json
import os

from ExampleClass import ExampleClass
from FolderQueue import FolderQueue

machine = ExampleClass()
queue = FolderQueue("json_queue")

while True:
    if command := next(queue()):
        result = machine.execute_command(command)
        print(result)
    sleep(1)
