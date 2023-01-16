import datetime
import logging
import os
from logging import FileHandler
from urllib.parse import quote_plus

from concurrent_log_handler import ConcurrentRotatingFileHandler
from dotenv import load_dotenv
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

from .log_configs import LevelFilter, formatter

load_dotenv()

def system_setting_app():
	app = Flask(__name__)
	blueprint = Blueprint("api", __name__)
	api = Api(
		blueprint,
		title = "BMS Endpoints",
		version = "1.0",
		description = "System Setting Endpoints"
	)

	app.register_blueprint(blueprint)
	CORS(app)
	app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{username}:{password}@{host}:{port}/{db_name}".format(
		username	= os.getenv("DB_USERNAME"),
		password	= quote_plus(os.getenv("DB_PASSWORD")),
		host		= os.getenv("DB_HOST"),
		port		= os.getenv("DB_PORT"),
		db_name		= os.getenv("DB_NAME")
	)
	app.config["SQLALCHEMY_POOL_SIZE"] = 10
	app.config["SQLALCHEMY_MAX_OVERFLOW"] = 50
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	db = SQLAlchemy()
	db.__init__(app)

	Base = automap_base()
	Base.prepare(db.engine, reflect = True, schema = "public")

	AdtBase = automap_base()
	AdtBase.prepare(db.engine, reflect = True, schema = "Adt")

	ma = Marshmallow()
	ma.init_app(app)

	log_path = os.path.dirname(__file__) + "/../logs"
	if not os.path.isdir(log_path):
		os.mkdir(log_path)

	werkzeug_logger = logging.getLogger("werkzeug")
	werkzeug_logger.setLevel(logging.DEBUG)
	werkzeug_handler = FileHandler(log_path + "/" + str(datetime.datetime.now().strftime("%Y_%m_%d")) + "_werkzeug_log.log")
	werkzeug_logger.addHandler(werkzeug_handler)

	logger = logging.getLogger("SYSTEM_SETTING")
	logger.setLevel(logging.DEBUG)

	if not os.path.isdir(log_path + "/" + __name__):
		os.mkdir(log_path + "/" + __name__)

	handler = ConcurrentRotatingFileHandler(log_path + "/" + __name__ + "/" + str(datetime.datetime.now().strftime("%Y_%m_%d")) + ".log", "a", 100*1024, 30) # 100KB
	handler.setFormatter(formatter)

	log_level = (
		db.session.query(Base.classes.ADM_SETTING_MAPPING)
		.filter(Base.classes.ADM_SETTING_MAPPING.Additional_Name == "BACKEND_LVL")
		.first()
	)
	
	if log_level.Additional_Value == "NOTSET":
		handler.addFilter(LevelFilter(0, 0))

	elif log_level.Additional_Value == "DEBUG":
		handler.addFilter(LevelFilter(10, 50))

	elif log_level.Additional_Value == "INFO":
		handler.addFilter(LevelFilter(20, 50))

	elif log_level.Additional_Value == "WARNING":
		handler.addFilter(LevelFilter(30, 50))

	elif log_level.Additional_Value == "ERROR": 
		handler.addFilter(LevelFilter(40, 50))

	elif log_level.Additional_Value == "CRITICAL":
		handler.addFilter(LevelFilter(50, 50))

	logger.addHandler(handler)

	return api, app, AdtBase, Base, db, ma, logger

api, app, AdtBase, Base, db, ma, logger = system_setting_app()
