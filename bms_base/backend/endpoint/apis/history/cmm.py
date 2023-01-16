import traceback

from flask import jsonify, make_response
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import (ADM_OBJECT_LOGGING_MASTER, ADM_USR_MASTER,
                              ADT_FORM_MASTER, ADT_WORKFLOW_MASTER)

api = Namespace(path = "/history", name = "History - Content Management")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

# GET
@api.route("/form/<ID>")
@api.expect(header_token)
class Form(Resource):
	@api.doc(
		description = "Form Master History",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, ID):
		try:
			adt_history = (
				db.session.query(
					ADT_FORM_MASTER.Op,
					ADT_FORM_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_FORM_MASTER.Old_Row_Data,
					ADT_FORM_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_FORM_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_FORM_MASTER.Audit_ID == ID)
				.all()
			)

			logging_history = (
				db.session.query(
					ADM_OBJECT_LOGGING_MASTER.Action,
					ADM_OBJECT_LOGGING_MASTER.Time,
					ADM_USR_MASTER.Preferred_Name,
					ADM_OBJECT_LOGGING_MASTER.Object_ID,
					ADM_OBJECT_LOGGING_MASTER.Desc
				)
				.join(ADM_USR_MASTER, ADM_OBJECT_LOGGING_MASTER.User == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Company")
				.filter(ADM_OBJECT_LOGGING_MASTER.Object_ID == ID)
				.all()
			)

			if not adt_history and not logging_history:
				response = {"error": "History not found"}
				return make_response(jsonify(response), 200)
			else:
				response = []
				if adt_history:
					for row in adt_history:
						response.append({
							"Op": row.Op,
							"Stamp": row.Stamp.strftime("%d-%m-%Y %I:%M:%S %p"),
							"Last_Edit_User": row.Preferred_Name,
							"Old_Row_Data": row.Old_Row_Data,
							"New_Row_Data": row.New_Row_Data,
						})

				if logging_history:
					for row in logging_history:
						response.append({
							"Op": row.Action,
							"Stamp": row.Time.strftime("%d-%m-%Y %I:%M:%S %p"),
							"Last_Edit_User": row.Preferred_Name,
							"Old_Row_Data": row.Desc,
							"New_Row_Data": row.Desc,
						})
				
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
@api.route("/workflow/<ID>")
@api.expect(header_token)
class Workflow(Resource):
	@api.doc(
		description = "Workflow Master History",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, ID):
		try:
			adt_history = (
				db.session.query(
					ADT_WORKFLOW_MASTER.Op,
					ADT_WORKFLOW_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_WORKFLOW_MASTER.Old_Row_Data,
					ADT_WORKFLOW_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_WORKFLOW_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_WORKFLOW_MASTER.Audit_ID == ID)
				.all()
			)

			logging_history = (
				db.session.query(
					ADM_OBJECT_LOGGING_MASTER.Action,
					ADM_OBJECT_LOGGING_MASTER.Time,
					ADM_USR_MASTER.Preferred_Name,
					ADM_OBJECT_LOGGING_MASTER.Object_ID,
					ADM_OBJECT_LOGGING_MASTER.Desc
				)
				.join(ADM_USR_MASTER, ADM_OBJECT_LOGGING_MASTER.User == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Company")
				.filter(ADM_OBJECT_LOGGING_MASTER.Object_ID == ID)
				.all()
			)

			if not adt_history and not logging_history:
				response = {"error": "History not found"}
				return make_response(jsonify(response), 200)
			else:
				response = []
				if adt_history:
					for row in adt_history:
						response.append({
							"Op": row.Op,
							"Stamp": row.Stamp.strftime("%d-%m-%Y %I:%M:%S %p"),
							"Last_Edit_User": row.Preferred_Name,
							"Old_Row_Data": row.Old_Row_Data,
							"New_Row_Data": row.New_Row_Data,
						})

				if logging_history:
					for row in logging_history:
						response.append({
							"Op": row.Action,
							"Stamp": row.Time.strftime("%d-%m-%Y %I:%M:%S %p"),
							"Last_Edit_User": row.Preferred_Name,
							"Old_Row_Data": row.Desc,
							"New_Row_Data": row.Desc,
						})
				
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
