import traceback

from flask import jsonify, make_response
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import (ADM_OBJECT_LOGGING_MASTER, ADM_USR_MASTER,
                              ADT_BUS_UNIT_MASTER, ADT_DEPT_MASTER,
                              ADT_ORG_MASTER, ADT_ROLE_MASTER, ADT_USR_MASTER)

api = Namespace(path = "/history", name = "History - People & Organization")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

# GET
@api.route("/company/<ID>")
@api.expect(header_token)
class Company(Resource):
	@api.doc(
		description = "Organization Master History",
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
					ADT_ORG_MASTER.Op,
					ADT_ORG_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_ORG_MASTER.Old_Row_Data,
					ADT_ORG_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_ORG_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_ORG_MASTER.Audit_ID == ID)
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
@api.route("/business_unit/<ID>")
@api.expect(header_token)
class BusinessUnit(Resource):
	@api.doc(
		description = "Business Unit Master History",
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
					ADT_BUS_UNIT_MASTER.Op,
					ADT_BUS_UNIT_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_BUS_UNIT_MASTER.Old_Row_Data,
					ADT_BUS_UNIT_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_BUS_UNIT_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_BUS_UNIT_MASTER.Audit_ID == ID)
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
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Business Unit")
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
@api.route("/department/<ID>")
@api.expect(header_token)
class Department(Resource):
	@api.doc(
		description = "Department Master History",
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
					ADT_DEPT_MASTER.Op,
					ADT_DEPT_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_DEPT_MASTER.Old_Row_Data,
					ADT_DEPT_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_DEPT_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_DEPT_MASTER.Audit_ID == ID)
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
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Department")
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
@api.route("/role/<ID>")
@api.expect(header_token)
class Role(Resource):
	@api.doc(
		description = "Role Master History",
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
					ADT_ROLE_MASTER.Op,
					ADT_ROLE_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_ROLE_MASTER.Old_Row_Data,
					ADT_ROLE_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_ROLE_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_ROLE_MASTER.Audit_ID == ID)
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
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Role")
				.filter(ADM_OBJECT_LOGGING_MASTER.Object_ID == ID)
				.all()
			)

			if not adt_history:
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
@api.route("/user/<ID>")
@api.expect(header_token)
class User(Resource):
	@api.doc(
		description = "User Master History",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, ID):
		try:
			adt_master_history = (
				db.session.query(
					ADT_USR_MASTER.Op,
					ADT_USR_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_USR_MASTER.Old_Row_Data,
					ADT_USR_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_USR_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_USR_MASTER.Audit_ID == ID)
				.all()
			)

			# adt_auth_history = (
			# 	db.session.query(
			# 		ADT_USR_AUTH.Op,
			# 		ADT_USR_AUTH.Stamp,
			# 		ADM_USR_MASTER.Preferred_Name,
			# 		ADT_USR_AUTH.Old_Row_Data,
			# 		ADT_USR_AUTH.New_Row_Data,
			# 	)
			# 	.join(ADM_USR_MASTER, ADT_USR_AUTH.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
			# 	.filter(ADT_USR_AUTH.Audit_ID == ID)
			# 	.all()
			# )

			logging_master_history = (
				db.session.query(
					ADM_OBJECT_LOGGING_MASTER.Action,
					ADM_OBJECT_LOGGING_MASTER.Time,
					ADM_USR_MASTER.Preferred_Name,
					ADM_OBJECT_LOGGING_MASTER.Object_ID,
					ADM_OBJECT_LOGGING_MASTER.Desc
				)
				.join(ADM_USR_MASTER, ADM_OBJECT_LOGGING_MASTER.User == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "User")
				.filter(ADM_OBJECT_LOGGING_MASTER.Object_ID == ID)
				.all()
			)

			if not adt_master_history and not logging_master_history:
				response = {"error": "History not found"}
				return make_response(jsonify(response), 200)
			else:
				response = []
				if adt_master_history:
					for row in adt_master_history:
						response.append({
							"Op": row.Op,
							"Stamp": row.Stamp.strftime("%d-%m-%Y %I:%M:%S %p"),
							"Last_Edit_User": row.Preferred_Name,
							"Old_Row_Data": row.Old_Row_Data,
							"New_Row_Data": row.New_Row_Data,
						})

				# if adt_auth_history:
				# 	for row in adt_auth_history:
				# 		response.append({
				# 			"Op": row.Op,
				# 			"Stamp": row.Stamp.strftime("%d-%m-%Y %I:%M:%S %p"),
				# 			"Last_Edit_User": row.Preferred_Name,
				# 			"Old_Row_Data": row.Old_Row_Data,
				# 			"New_Row_Data": row.New_Row_Data,
				# 		})

				if logging_master_history:
					for row in logging_master_history:
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
