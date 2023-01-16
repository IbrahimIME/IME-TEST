import traceback

from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import ApiModel, LoggingMasterSchema

api = Namespace(path = "/object_logs", name = "Object Activity Log")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

# Api Model
object_logging_body = api.model("object_logging_body", model = ApiModel.object_log_body)

# Init Schema
logging_master_schema = LoggingMasterSchema()
logging_masters_schema = LoggingMasterSchema(many=True)

# POST
@api.route("")
@api.expect(header_token)
class LogtoDB(Resource):
	# Add an Object Activity Log
	@api.doc(
		description = "Add an Object Activity Log",
		body = object_logging_body,
		responses = {
			201: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self):
		try:
			args = request.get_json()

			new_activity_log = {
				"User": args["User"],
				"Org": args["Org"],
				"Roles": args["Roles"],
				"Action": args["Action"],
				"Object": args["Object"],
				"Object_ID": str(args["Object_ID"]),
				"Desc": args["Desc"],
				"IP": args["IP"],
				"User_Agent": args["User_Agent"]
			}
			new_logging_master = logging_master_schema.load(new_activity_log)

			db.session.add(new_logging_master)
			db.session.commit()

			response = {"success": "Object Activity Log added"}
			return make_response(jsonify(response), 201)

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
