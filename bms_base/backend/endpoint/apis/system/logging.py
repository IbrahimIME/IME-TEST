import traceback
from datetime import datetime

from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource
from sqlalchemy import Date, cast

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import (ADM_USER_ACTIVITY, ActivityLogSchema, ApiModel,
                              LoggingMasterSchema)

api = Namespace(path = "/logging", name = "Logging")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

# Api Model
object_logging_body = api.model("object_logging_body", model = ApiModel.object_log_body)

# Init Schema
logging_master_schema = LoggingMasterSchema()
logging_masters_schema = LoggingMasterSchema(many=True)
activity_log_schema = ActivityLogSchema()
activity_logs_schema = ActivityLogSchema(many=True)

# POST
@api.route("/object")
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

# POST
@api.route("/activity")
@api.expect(header_token)
class UserActivity(Resource):
	# Log User Activity
	@api.doc(
		description = "Log User Activity",
		responses = {
			201: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self):
		try:
			args = request.get_json()
			args["Date_Time"] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

			new_log = activity_log_schema.load(args, session = db.session)

			db.session.add(new_log)
			db.session.commit()

			response = {"success": "User Activity Log added"}
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
@api.route("/activity/<LogDate>")
@api.expect(header_token)
class GetActivityLogs(Resource):
	# Get User Activity Logs
	@api.doc(
		description = "Get User Activity Log",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, LogDate):
		try:
			activity_logs = (
				db.session.query(ADM_USER_ACTIVITY)
				.filter(cast(ADM_USER_ACTIVITY.Date_Time, Date) == LogDate)
				.order_by(ADM_USER_ACTIVITY.Date_Time.desc())
				.all()
			)

			if not activity_logs:
				response = {"error": "Activity Logs not found"}
				return make_response(jsonify(response), 200)
			else:
				response = activity_logs_schema.jsonify(activity_logs)
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
