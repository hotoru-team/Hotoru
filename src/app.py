import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv(dotenv_path='..', verbose=True)
app = Flask(__name__)


@app.route('/')
def hello():
    return os.getenv("EMAIL")

@app.route('/<name>')
def render(name):
    return render_template('hello.html.jinja', name=name)

if __name__ == '__main__':
    app.run()