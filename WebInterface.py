from flask import Flask, render_template, request, redirect, url_for
from ExampleClass import ExampleClass, PublicMethod
import json
from datetime import datetime


app = Flask(__name__)
app.jinja_env.globals.update(list=list)
methods = ExampleClass.get_public_methods()
last_command: str = ""


@app.route("/")
def home():
    return render_template("index.html", methods=methods, last_command=last_command)

@app.route("/executeCommand", methods=["POST"])
def executeCommand():
    command = methods[request.form["function"]].validate_command(request.form, with_types=True)
    if command.is_valid:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        with open(f"json_queue/new/{timestamp}.json", "w") as f:
            json.dump(command.converted, f)
        global last_command # Only for prototyping
        last_command = json.dumps(command.converted)
        return redirect(url_for("home"))
    else:
        last_command = command.errors
        return redirect(url_for("home"))
