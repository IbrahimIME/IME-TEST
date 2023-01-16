import os
import traceback
from datetime import datetime

from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource
from werkzeug.utils import secure_filename

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import ADM_IMPORT_HISTORY, ImportHistorySchema

api = Namespace(path = "/import_history", name = "Import History")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

import_history_schema = ImportHistorySchema()
import_histories_schema = ImportHistorySchema(many=True)

# GET, POST
@api.route("")
@api.expect(header_token)
class ImportHistory(Resource):
	# Get ALL Import History
	@api.doc(
		description = "Get ALL Import History",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			histories = (
				db.session.query(ADM_IMPORT_HISTORY)
				.order_by(ADM_IMPORT_HISTORY.Import_Date_Time)
				.all()
			)

			if not histories:
				response = {"error": "Import History not found"}
				return make_response(jsonify(response), 200)
			else:
				response = import_histories_schema.jsonify(histories)
				return make_response(response, 200)

		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

	# Add an Import History
	@api.doc(
		description = "Add an Import History",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self):
		try:
			path = os.getenv("CSV_IMPORT_PATH")
			target = os.path.abspath(os.getenv("HTDOCS_PATH") + path)

			if not os.path.isdir(target):
				os.mkdir(target)

			object = ""
			if "Object" in request.headers:
				object = request.headers["Object"]

			result = None
			if "Result" in request.headers:
				result = request.headers["Result"]

			user = None
			if "Import_By" in request.headers:
				user = request.headers["Import_By"]

			file = request.files["file"]
			current_timestamp = datetime.now()
			current_datetime_str = current_timestamp.strftime("%Y%m%d%H%M%S")
			filename = current_datetime_str + "_" + secure_filename(object) + os.path.splitext(secure_filename(file.filename))[1]

			destination = "/".join([target, filename])
			file.save(destination)

			new_history = ADM_IMPORT_HISTORY(
				Object = object,
				File_Path = "/".join([path, filename]),
				Result = result,
				Import_Date_Time = current_timestamp,
				Import_By = user
			)

			db.session.add(new_history)
			db.session.commit()

			response = {"success": "Import History added"}
			return make_response(jsonify(response), 200)
			
		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# GET
@api.route("/<ID>")
@api.expect(header_token)
class SingleImportHistory(Resource):
	# Get Single Import History
	@api.doc(
		description = "Get Single Import History",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, ID):
		try:
			history = (
				db.session.query(ADM_IMPORT_HISTORY)
				.filter(ADM_IMPORT_HISTORY.ID == ID)
				.first()
			)

			if not history:
				response = {"error": "Import History not found"}
				return make_response(jsonify(response), 200)
			else:
				response = import_history_schema.jsonify(history)
				return make_response(response, 200)

		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()
			