"""
  App Controller
"""

from src import app
from flask import jsonify

@app.route('/ping')
def ping():
  return jsonify({ "data": "pong" })


