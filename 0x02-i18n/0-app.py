#!/usr/bin/env python3
""" Module to start a Flask web application
"""
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_world():
    """ Function to render a template """
    render_template('0-index.html')


if __name__ == "__main__":
    app.run(host='', port=5000)