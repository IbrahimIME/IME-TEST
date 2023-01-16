import traceback

from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource
from sqlalchemy import String, and_, cast, func, literal_column

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import (ADM_ADDITIONAL_ATTRIBUTE, ADM_ATTRIBUTE_MASTER,
                              ADM_OBJ_TYPE_MASTER, ADM_SENSITIVE_ACCESS_MASTER,
                              AdditionalAttributeSchema, AttributeMasterSchema)

api = Namespace(path = "/additional_attribute", name = "Additional Attribute")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

additional_header_token = api.parser()
additional_header_token.add_argument("access-token", location = "headers")
additional_header_token.add_argument("Role_ID", location = "headers")

attribute_masters_schema = AttributeMasterSchema(many=True)
additional_attributes_schema = AdditionalAttributeSchema(many=True)

# GET
@api.route("/object/<Object>")
@api.expect(additional_header_token)
class AllAdditionalAttribute(Resource):
	# Get ALL Additional Attribute of an Object
	@api.doc(
		description = "Get ALL Additional Attribute of an Object",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Object):
		try:
			if "Role_ID" in request.headers:
				object = (
					db.session.query(ADM_OBJ_TYPE_MASTER)
					.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_Name == Object)
					.first()
				)

				if not object:
					response = {"error": "Object not found"}
					return make_response(jsonify(response), 200)
				else:
					attribute_masters = (
						db.session.query(ADM_ATTRIBUTE_MASTER)
						.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == object.Obj_Type_ID)
						.filter(ADM_ATTRIBUTE_MASTER.System == False)
						.order_by(ADM_ATTRIBUTE_MASTER.ID)
						.all()
					)

					if not attribute_masters:
						response = {"none": "No Additional Attribute"}
						return make_response(jsonify(response), 200)
					else:
						response = []
						for row in attribute_masters:
							if row.Sensitive == True and "Role_ID" in request.headers:
								roles = request.headers["Role_ID"].split("|")

								accesses = (
									db.session.query(ADM_SENSITIVE_ACCESS_MASTER)
									.filter(ADM_SENSITIVE_ACCESS_MASTER.Role_ID.in_(roles))
									.filter(ADM_SENSITIVE_ACCESS_MASTER.Attribute_Master_ID == row.ID)
									.all()
								)

								create = False
								read = False
								update = False
								delete = False
								approve = False

								if accesses:
									for access in accesses:
										if access.Create == "1":
											create = True

										if access.Read == "1":
											read = True

										if access.Update == "1":
											update = True

										if access.Delete == "1":
											delete = True

										if access.Approve == "1":
											approve = True

								response.append({
									"Obj_Type_ID": row.Obj_Type_ID,
									"Name": row.Name,
									"Input_Type": row.Input_Type,
									"Data_Type": row.Data_Type,
									"Length": row.Length,
									"System": row.System,
									"Mandatory": row.Mandatory,
									"Default_Value": row.Default_Value,
									"Sensitive": row.Sensitive,
									"Create": create,
									"Read": read,
									"Update": update,
									"Delete": delete,
									"Approve": approve,
									"Attribute_Master_ID": row.ID,
									"Attribute_Value": None,
									"Attribute_Value_ID": None
								})

							else:
								response.append({
									"Obj_Type_ID": row.Obj_Type_ID,
									"Name": row.Name,
									"Input_Type": row.Input_Type,
									"Data_Type": row.Data_Type,
									"Length": row.Length,
									"System": row.System,
									"Mandatory": row.Mandatory,
									"Default_Value": row.Default_Value,
									"Sensitive": row.Sensitive,
									"Attribute_Master_ID": row.ID,
									"Attribute_Value": None,
									"Attribute_Value_ID": None
								})

						return make_response(jsonify(response), 200)

			else:
				response = {"error": "Role_ID is not in headers"}
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

# GET, POST, PUT, DELETE
@api.route("/object/<Object>/id/<Object_ID>")
@api.expect(header_token)
class AllAdditionalAttributeValue(Resource):
	# Get ALL Additional Attribute Value of an Object
	@api.doc(
		description = "Get ALL Additional Attribute Value of an Object",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Object, Object_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_Name == Object)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				additional_attributes = (
					db.session.query(
						ADM_ATTRIBUTE_MASTER.Obj_Type_ID.label("Obj_Type_ID"),
						ADM_ADDITIONAL_ATTRIBUTE.Object.label("Object"),
						ADM_ADDITIONAL_ATTRIBUTE.Object_ID.label("Object_ID"),
						ADM_ATTRIBUTE_MASTER.Name.label("Name"),
						ADM_ATTRIBUTE_MASTER.Default_Value.label("Default_Value"),
						ADM_ATTRIBUTE_MASTER.Length.label("Length"),
						ADM_ATTRIBUTE_MASTER.Input_Type.label("Input_Type"),
						ADM_ATTRIBUTE_MASTER.Data_Type.label("Data_Type"),
						ADM_ATTRIBUTE_MASTER.Mandatory.label("Mandatory"),
						ADM_ATTRIBUTE_MASTER.Sensitive.label("Sensitive"),
						ADM_ATTRIBUTE_MASTER.ID.label("Attribute_Master_ID"),
						func.string_agg(cast(ADM_ADDITIONAL_ATTRIBUTE.Attribute_Value_ID, String), literal_column("'|'")).label("Attribute_Value_ID"),
						func.string_agg(ADM_ADDITIONAL_ATTRIBUTE.Attribute_Value, literal_column("'|'")).label("Attribute_Value"),
					)
					.join(
						ADM_ADDITIONAL_ATTRIBUTE, and_(
							ADM_ATTRIBUTE_MASTER.ID == ADM_ADDITIONAL_ATTRIBUTE.Attribute_Master_ID,
							ADM_ADDITIONAL_ATTRIBUTE.Object == Object,
							ADM_ADDITIONAL_ATTRIBUTE.Object_ID == Object_ID
						), isouter = True
					)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == object.Obj_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.System == False)
					.order_by(ADM_ATTRIBUTE_MASTER.ID)
					.group_by(
						ADM_ATTRIBUTE_MASTER.Obj_Type_ID,
						ADM_ADDITIONAL_ATTRIBUTE.Object,
						ADM_ADDITIONAL_ATTRIBUTE.Object_ID,
						ADM_ATTRIBUTE_MASTER.Name,
						ADM_ATTRIBUTE_MASTER.Default_Value,
						ADM_ATTRIBUTE_MASTER.Length,
						ADM_ATTRIBUTE_MASTER.Input_Type,
						ADM_ATTRIBUTE_MASTER.Data_Type,
						ADM_ATTRIBUTE_MASTER.Mandatory,
						ADM_ATTRIBUTE_MASTER.Sensitive,
						ADM_ATTRIBUTE_MASTER.ID,
					)
					.all()
				)

				if not additional_attributes:
					response = {"none": "No Additional Attribute"}
					return make_response(jsonify(response), 200)
				else:
					result = []
					
					for row in additional_attributes:
						if row.Sensitive == True and "Role_ID" in request.headers:
							roles = request.headers["Role_ID"].split("|")

							accesses = (
								db.session.query(ADM_SENSITIVE_ACCESS_MASTER)
								.filter(ADM_SENSITIVE_ACCESS_MASTER.Role_ID.in_(roles))
								.filter(ADM_SENSITIVE_ACCESS_MASTER.Attribute_Master_ID == row.Attribute_Master_ID)
								.all()
							)

							create = False
							read = False
							update = False
							delete = False
							approve = False

							if accesses:
								for access in accesses:
									if access.Create == "1":
										create = True

									if access.Read == "1":
										read = True

									if access.Update == "1":
										update = True

									if access.Delete == "1":
										delete = True

									if access.Approve == "1":
										approve = True

							result.append({
								"Obj_Type_ID": row.Obj_Type_ID,
								"Object": row.Object,
								"Object_ID": row.Object_ID,
								"Name": row.Name,
								"Default_Value": row.Default_Value,
								"Length": row.Length,
								"Input_Type": row.Input_Type,
								"Data_Type": row.Data_Type,
								"Mandatory": row.Mandatory,
								"Sensitive": row.Sensitive,
								"Attribute_Master_ID": row.Attribute_Master_ID,
								"Attribute_Value_ID": row.Attribute_Value_ID,
								"Attribute_Value": row.Attribute_Value,
								"Create": create,
								"Read": read,
								"Update": update,
								"Delete": delete,
								"Approve": approve
							})
						else:
							result.append({
								"Obj_Type_ID": row.Obj_Type_ID,
								"Object": row.Object,
								"Object_ID": row.Object_ID,
								"Name": row.Name,
								"Default_Value": row.Default_Value,
								"Length": row.Length,
								"Input_Type": row.Input_Type,
								"Data_Type": row.Data_Type,
								"Mandatory": row.Mandatory,
								"Sensitive": row.Sensitive,
								"Attribute_Master_ID": row.Attribute_Master_ID,
								"Attribute_Value_ID": row.Attribute_Value_ID,
								"Attribute_Value": row.Attribute_Value,
							})

					return make_response(jsonify(result), 200)

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

	# Add Additional Attributes Value of an Object
	@api.doc(
		description = "Add Additional Attributes Value of an Object",
		responses = {
			201: "OK",
			403: "Error",
		}
	)
	@token_required
	def post(self, Object, Object_ID):
		try:
			args = request.get_json()

			for row in args:
				if row["Input_Type"] == "dropdown":
					new_value = ADM_ADDITIONAL_ATTRIBUTE(
						Object = Object,
						Object_ID = Object_ID,
						Attribute_Master_ID = row["Attribute_Master_ID"],
						Attribute_Value_ID = row["Attribute_Value_ID"],
						Attribute_Value = None,
						Last_Edit_User = row["Last_Edit_User"]
					)

					db.session.add(new_value)

				elif row["Input_Type"] == "checkbox":
					for attribute_value in row["Attribute_Value_ID"]:
						if isinstance(attribute_value, str) and attribute_value.isnumeric():
							new_value = ADM_ADDITIONAL_ATTRIBUTE(
								Object = Object,
								Object_ID = Object_ID,
								Attribute_Master_ID = row["Attribute_Master_ID"],
								Attribute_Value_ID = int(attribute_value),
								Attribute_Value = None,
								Last_Edit_User = row["Last_Edit_User"]
							)

							db.session.add(new_value)

				elif row["Input_Type"] == "radio":
					new_value = ADM_ADDITIONAL_ATTRIBUTE(
						Object = Object,
						Object_ID = Object_ID,
						Attribute_Master_ID = row["Attribute_Master_ID"],
						Attribute_Value_ID = int(row["Attribute_Value_ID"]),
						Attribute_Value = None,
						Last_Edit_User = row["Last_Edit_User"]
					)

					db.session.add(new_value)

				elif row["Input_Type"] == "freeinput":
					new_value = ADM_ADDITIONAL_ATTRIBUTE(
						Object = Object,
						Object_ID = Object_ID,
						Attribute_Master_ID = row["Attribute_Master_ID"],
						Attribute_Value_ID = None,
						Attribute_Value = row["Attribute_Value"],
						Last_Edit_User = row["Last_Edit_User"]
					)

					db.session.add(new_value)

			db.session.commit()

			response = {"success": "Additional Attributes added"}
			return make_response(jsonify(response), 201)

		except Exception as e:
			db.session.rollback()

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

	# Update Additional Attributes of an Object
	@api.doc(
		description = "Update Additional Attributes of an Object",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def put(self, Object, Object_ID):
		try:
			args = request.get_json()

			for row in args:
				if row["Input_Type"] == "checkbox":
					additional_attributes = (
						db.session.query(ADM_ADDITIONAL_ATTRIBUTE)
						.filter(ADM_ADDITIONAL_ATTRIBUTE.Object == Object)
						.filter(ADM_ADDITIONAL_ATTRIBUTE.Object_ID == Object_ID)
						.filter(ADM_ADDITIONAL_ATTRIBUTE.Attribute_Master_ID == row["Attribute_Master_ID"])
						.all()
					)

					if additional_attributes:
						for attr in additional_attributes:
							db.session.delete(attr)

					for attribute_value in row["Attribute_Value_ID"]:
						if isinstance(attribute_value, str) and attribute_value.isnumeric():
							new_value = ADM_ADDITIONAL_ATTRIBUTE(
								Object = Object,
								Object_ID = Object_ID,
								Attribute_Master_ID = row["Attribute_Master_ID"],
								Attribute_Value_ID = int(attribute_value),
								Attribute_Value = None,
								Last_Edit_User = row["Last_Edit_User"]
							)

							db.session.add(new_value)

				else:
					additional_attribute = (
						db.session.query(ADM_ADDITIONAL_ATTRIBUTE)
						.filter(ADM_ADDITIONAL_ATTRIBUTE.Object == Object)
						.filter(ADM_ADDITIONAL_ATTRIBUTE.Object_ID == Object_ID)
						.filter(ADM_ADDITIONAL_ATTRIBUTE.Attribute_Master_ID == row["Attribute_Master_ID"])
						.first()
					)

					if additional_attribute:
						if row["Input_Type"] == "freeinput":
							additional_attribute.Attribute_Value = row["Attribute_Value"]
							additional_attribute.Attribute_Value_ID = None

						elif row["Input_Type"] == "dropdown" or row["Input_Type"] == "radio":
							additional_attribute.Attribute_Value = None
							additional_attribute.Attribute_Value_ID = row["Attribute_Value_ID"]

					else:
						if row["Input_Type"] == "dropdown":
							new_value = ADM_ADDITIONAL_ATTRIBUTE(
								Object = Object,
								Object_ID = Object_ID,
								Attribute_Master_ID = row["Attribute_Master_ID"],
								Attribute_Value_ID = row["Attribute_Value_ID"],
								Attribute_Value = None,
								Last_Edit_User = row["Last_Edit_User"]
							)

							db.session.add(new_value)

						elif row["Input_Type"] == "checkbox":
							for attribute_value in row["Attribute_Value_ID"]:
								if isinstance(attribute_value, str) and attribute_value.isnumeric():
									new_value = ADM_ADDITIONAL_ATTRIBUTE(
										Object = Object,
										Object_ID = Object_ID,
										Attribute_Master_ID = row["Attribute_Master_ID"],
										Attribute_Value_ID = int(attribute_value),
										Attribute_Value = None,
										Last_Edit_User = row["Last_Edit_User"]
									)

									db.session.add(new_value)

						elif row["Input_Type"] == "radio":
							new_value = ADM_ADDITIONAL_ATTRIBUTE(
								Object = Object,
								Object_ID = Object_ID,
								Attribute_Master_ID = row["Attribute_Master_ID"],
								Attribute_Value_ID = int(row["Attribute_Value_ID"]),
								Attribute_Value = None,
								Last_Edit_User = row["Last_Edit_User"]
							)

							db.session.add(new_value)
							
						elif row["Input_Type"] == "freeinput":
							new_value = ADM_ADDITIONAL_ATTRIBUTE(
								Object = Object,
								Object_ID = Object_ID,
								Attribute_Master_ID = row["Attribute_Master_ID"],
								Attribute_Value_ID = None,
								Attribute_Value = row["Attribute_Value"],
								Last_Edit_User = row["Last_Edit_User"]
							)

							db.session.add(new_value)

			db.session.commit()

			response = {"success": "Additional Attribute updated"}
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

	# Delete ALL Additional Attributes of an Object
	@api.doc(
		description = "Delete ALL Additional Attributes of an Object",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def delete(self, Object, Object_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_Name == Object)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				additional_attributes = (
					db.session.query(ADM_ADDITIONAL_ATTRIBUTE)
					.filter(ADM_ADDITIONAL_ATTRIBUTE.Object == Object)
					.filter(ADM_ADDITIONAL_ATTRIBUTE.Object_ID == Object_ID)
					.all()
				)

				if additional_attributes:
					for row in additional_attributes:
						db.session.delete(row)

					db.session.commit()
				
				response = {"success": "Additional Attributes deleted"}
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
