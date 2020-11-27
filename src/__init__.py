from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from src.configs import Config
from flask_cors import CORS
from flask_redis import FlaskRedis

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = Config.POSTGRES_URL
app.config["REDIS_URL"] = Config.REDIS_URL

db = SQLAlchemy(app)
redis_client = FlaskRedis(app)
CORS(app)

from src.controllers import *