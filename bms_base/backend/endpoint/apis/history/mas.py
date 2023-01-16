import traceback

from flask import jsonify, make_response
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import (ADM_OBJECT_LOGGING_MASTER, ADM_USR_MASTER,
                              ADT_CURRENCY_MASTER, ADT_CUST_FIN_MASTER,
                              ADT_CUST_MASTER, ADT_ITEMS_GROUP_MASTER,
                              ADT_ITEMS_MASTER, ADT_SUPPLIER_FIN_MASTER,
                              ADT_SUPPLIER_MASTER)

api = Namespace(path = "/history", name = "History - Master Data")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

# GET
@api.route("/item_group/<ID>")
@api.expect(header_token)
class ItemGroup(Resource):
	@api.doc(
		description = "Item Group History",
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
					ADT_ITEMS_GROUP_MASTER.Op,
					ADT_ITEMS_GROUP_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_ITEMS_GROUP_MASTER.Old_Row_Data,
					ADT_ITEMS_GROUP_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_ITEMS_GROUP_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_ITEMS_GROUP_MASTER.Audit_ID == ID)
				.order_by(ADT_ITEMS_GROUP_MASTER.ID.desc())
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
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Item Group")
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
@api.route("/item_master/<ID>")
@api.expect(header_token)
class ItemMaster(Resource):
	@api.doc(
		description = "Item Master History",
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
					ADT_ITEMS_MASTER.Op,
					ADT_ITEMS_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_ITEMS_MASTER.Old_Row_Data,
					ADT_ITEMS_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_ITEMS_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_ITEMS_MASTER.Audit_ID == ID)
				.order_by(ADT_ITEMS_MASTER.ID.desc())
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
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Item")
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
@api.route("/customer/<ID>")
@api.expect(header_token)
class Customer(Resource):
	@api.doc(
		description = "Customer Master History",
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
					ADT_CUST_MASTER.Op,
					ADT_CUST_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_CUST_MASTER.Old_Row_Data,
					ADT_CUST_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_CUST_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_CUST_MASTER.Audit_ID == ID)
				.order_by(ADT_CUST_MASTER.ID.desc())
				.all()
			)

			adt_fin_history = (
				db.session.query(
					ADT_CUST_FIN_MASTER.Op,
					ADT_CUST_FIN_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_CUST_FIN_MASTER.Old_Row_Data,
					ADT_CUST_FIN_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_CUST_FIN_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_CUST_FIN_MASTER.Audit_ID == ID)
				.order_by(ADT_CUST_FIN_MASTER.ID.desc())
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
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Customer")
				.filter(ADM_OBJECT_LOGGING_MASTER.Object_ID == ID)
				.all()
			)

			if not adt_history and not adt_fin_history and not logging_history:
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

				if adt_fin_history:
					for row in adt_fin_history:
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
@api.route("/supplier/<ID>")
@api.expect(header_token)
class Supplier(Resource):
	@api.doc(
		description = "Supplier Master History",
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
					ADT_SUPPLIER_MASTER.Op,
					ADT_SUPPLIER_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_SUPPLIER_MASTER.Old_Row_Data,
					ADT_SUPPLIER_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_SUPPLIER_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_SUPPLIER_MASTER.Audit_ID == ID)
				.order_by(ADT_SUPPLIER_MASTER.ID.desc())
				.all()
			)

			adt_fin_history = (
				db.session.query(
					ADT_SUPPLIER_FIN_MASTER.Op,
					ADT_SUPPLIER_FIN_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_SUPPLIER_FIN_MASTER.Old_Row_Data,
					ADT_SUPPLIER_FIN_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_SUPPLIER_FIN_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_SUPPLIER_FIN_MASTER.Audit_ID == ID)
				.order_by(ADT_SUPPLIER_FIN_MASTER.ID.desc())
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
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Supplier")
				.filter(ADM_OBJECT_LOGGING_MASTER.Object_ID == ID)
				.all()
			)

			if not adt_history and not adt_fin_history and not logging_history:
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

				if adt_fin_history:
					for row in adt_fin_history:
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
@api.route("/currency/<ID>")
@api.expect(header_token)
class Currency(Resource):
	@api.doc(
		description = "Currency Master History",
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
					ADT_CURRENCY_MASTER.Op,
					ADT_CURRENCY_MASTER.Stamp,
					ADM_USR_MASTER.Preferred_Name,
					ADT_CURRENCY_MASTER.Old_Row_Data,
					ADT_CURRENCY_MASTER.New_Row_Data,
				)
				.join(ADM_USR_MASTER, ADT_CURRENCY_MASTER.Created_by == ADM_USR_MASTER.User_ID, isouter = True)
				.filter(ADT_CURRENCY_MASTER.Audit_ID == ID)
				.order_by(ADT_CURRENCY_MASTER.ID.desc())
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
				.filter(ADM_OBJECT_LOGGING_MASTER.Object == "Currency")
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
