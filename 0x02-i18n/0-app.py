#!/usr/bin/env python3
""" Module to start a Flask web application
"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_world():
    """ Function to render a template """
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)
