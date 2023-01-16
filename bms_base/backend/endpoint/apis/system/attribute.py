import traceback

from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import (ADM_ADDITIONAL_ATTRIBUTE, ADM_ATTRIBUTE_MASTER,
                              ADM_ATTRIBUTE_VALUE, ADM_OBJ_TYPE_MASTER,
                              ADM_ROLE_MASTER, ADM_SENSITIVE_ACCESS_MASTER,
                              AttributeMasterSchema, AttributeValueSchema,
                              ObjectTypeMasterSchema)

api = Namespace(path = "/attribute", name = "Attribute")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

object_type_master_schema = ObjectTypeMasterSchema()
object_type_masters_schema = ObjectTypeMasterSchema(many=True)
attribute_master_schema = AttributeMasterSchema()
attribute_masters_schema = AttributeMasterSchema(many=True)
attribute_value_schema = AttributeValueSchema()
attribute_values_schema = AttributeValueSchema(many=True)

# GET
@api.route("/all_categories")
@api.expect(header_token)
class AllObjectCategories(Resource):
	# Get ALL Object Categories
	@api.doc(
		description = "Get ALL Object Categories",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			object_categories = (
				db.session.query(ADM_OBJ_TYPE_MASTER.Obj_Category)
				.distinct(ADM_OBJ_TYPE_MASTER.Obj_Category)
				.all()
			)

			if not object_categories:
				response = {"error": "Object Category not found"}
				return make_response(jsonify(response), 200)
			else:
				categories = []
				for row in object_categories:
					categories.append(row.Obj_Category)

				return make_response(jsonify(categories), 200)
			
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
@api.route("/all_objects")
@api.expect(header_token)
class AllObjects(Resource):
	# Get ALL Objects
	@api.doc(
		description = "Get ALL Objects",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self):
		try:
			objects = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.all()
			)

			if not objects:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				response = object_type_masters_schema.jsonify(objects)
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

# GET
@api.route("/object_id/<Object_ID>")
@api.expect(header_token)
class Attribute(Resource):
	# Get Single Object
	@api.doc(
		description = "Get Single Object",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Object_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				response = object_type_master_schema.jsonify(object)
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

# GET, POST
@api.route("/object_id/<Object_ID>/field")
@api.expect(header_token)
class AttributeField(Resource):
	# Get ALL Fields by Object
	@api.doc(
		description = "Get ALL Fields by Object",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Object_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				fields = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == Object_ID)
					.order_by(ADM_ATTRIBUTE_MASTER.ID)
					.all()
				)

				if not fields:
					response = {"error": "Object not found"}
					return make_response(jsonify(response), 200)
				else:
					response = attribute_masters_schema.jsonify(fields)
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

	# Add a Field
	@api.doc(
		description = "Add a Field",
		responses = {
			201: "OK",
			403: "Error",
		}
	)
	@token_required
	def post(self, Object_ID):
		try:
			args = request.get_json()

			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				new_field = attribute_master_schema.load(args, session = db.session)

				db.session.add(new_field)
				db.session.commit()

				if new_field.Sensitive == True:
					all_roles = (
						db.session.query(ADM_ROLE_MASTER)
						.all()
					)

					if all_roles:
						for row in all_roles:
							new_sensitive_access = ADM_SENSITIVE_ACCESS_MASTER(
								Attribute_Master_ID = new_field.ID,
								Role_ID = row.Role_ID,
								Create = "0",
								Read = "0",
								Update = "0",
								Delete = "0",
								Approve = "0"
							)

							db.session.add(new_sensitive_access)

						db.session.commit()

				response = {
					"ID": new_field.ID,
					"success": "Field added"
				}
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
			db.session.rollback()
			db.session.close()

# PUT, DELETE
@api.route("/object_id/<Object_ID>/field_id/<Field_ID>")
@api.expect(header_token)
class SingleAttributeByID(Resource):
	# Update a Field by ID
	@api.doc(
		description = "Update a Field by ID",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def put(self, Object_ID, Field_ID):
		try:
			args = request.get_json()

			field = (
				db.session.query(ADM_ATTRIBUTE_MASTER)
				.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == Object_ID)
				.filter(ADM_ATTRIBUTE_MASTER.ID == Field_ID)
				.first()
			)

			if not field:
				response = {"error": "Object / Field not found"}
				return make_response(jsonify(response), 200)
			else:
				for key in args:
					setattr(field, key, args[key])

				db.session.commit()

				if field.Sensitive == True:
					all_roles = (
						db.session.query(ADM_ROLE_MASTER)
						.all()
					)

					if all_roles:
						for row in all_roles:
							new_sensitive_access = ADM_SENSITIVE_ACCESS_MASTER(
								Attribute_Master_ID = field.ID,
								Role_ID = row.Role_ID,
								Create = "0",
								Read = "0",
								Update = "0",
								Delete = "0",
								Approve = "0"
							)

							db.session.add(new_sensitive_access)

						db.session.commit()
				else:
					accesses = (
						db.session.query(ADM_SENSITIVE_ACCESS_MASTER)
						.filter(ADM_SENSITIVE_ACCESS_MASTER.Attribute_Master_ID == field.ID)
						.all()
					)

					if accesses:
						for access in accesses:
							db.session.delete(access)

						db.session.commit()

				response = {"success": "Attribute Value updated"}
				return make_response(jsonify(response), 200)

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

	# Delete a Field by ID
	@api.doc(
		description = "Delete a Field by ID",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def delete(self, Object_ID, Field_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				field = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == Object_ID)
					.filter(ADM_ATTRIBUTE_MASTER.ID == Field_ID)
					.first()
				)

				if not field:
					response = {"error": "Object / Field not found"}
					return make_response(jsonify(response), 200)
				else:
					values = (
						db.session.query(ADM_ATTRIBUTE_VALUE)
						.filter(ADM_ATTRIBUTE_VALUE.Master_ID == Field_ID)
						.all()
					)

					if values:
						for value in values:
							db.session.delete(value)

					additional_attributes = (
						db.session.query(ADM_ADDITIONAL_ATTRIBUTE)
						.filter(ADM_ADDITIONAL_ATTRIBUTE.Object == object.Obj_Type_Name)
						.filter(ADM_ADDITIONAL_ATTRIBUTE.Attribute_Master_ID == Field_ID)
						.all()
					)

					if additional_attributes:
						for attribute in additional_attributes:
							db.session.delete(attribute)

					if field.Sensitive == True:
						accesses = (
							db.session.query(ADM_SENSITIVE_ACCESS_MASTER)
							.filter(ADM_SENSITIVE_ACCESS_MASTER.Attribute_Master_ID == field.ID)
							.all()
						)

						if accesses:
							for access in accesses:
								db.session.delete(access)

					db.session.delete(field)
					db.session.commit()

					response = {"success": "Field deleted"}
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
			db.session.rollback()
			db.session.close()

# GET
@api.route("/object_name/<Object>/field_name/<Field_Name>")
@api.expect(header_token)
class SingleAttributeByName(Resource):
	# Get a Field by Field Name
	@api.doc(
		description = "Get a Field by Field Name",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Object, Field_Name):
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
				field = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == object.Obj_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.Name == Field_Name)
					.first()
				)

				if not field:
					response = {"error": "Field not found"}
					return make_response(jsonify(response), 200)
				else:
					response = attribute_master_schema.jsonify(field)
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
			db.session.rollback()
			db.session.close()

# GET, POST
@api.route("/object_id/<Object_ID>/field_id/<Field_ID>/value")
@api.expect(header_token)
class AttributeValuesByID(Resource):
	# Get ALL Values of a Field by Field ID
	@api.doc(
		description = "Get ALL Values of a Field by Field ID",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Object_ID, Field_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				field = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == Object_ID)
					.filter(ADM_ATTRIBUTE_MASTER.ID == Field_ID)
					.first()
				)

				if not field:
					response = {"error": "Field not found"}
					return make_response(jsonify(response), 200)
				else:
					values = (
						db.session.query(ADM_ATTRIBUTE_VALUE)
						.filter(ADM_ATTRIBUTE_VALUE.Master_ID == field.ID)
						.order_by(ADM_ATTRIBUTE_VALUE.Label)
						.all()
					)

					if not values:
						value_count = (
							db.session.query(ADM_ATTRIBUTE_VALUE)
							.filter(ADM_ATTRIBUTE_VALUE.Master_ID == field.ID)
							.count()
						)

						if value_count == 0:
							response = []
							return make_response(jsonify(response), 200)
						else:
							response = {"error": "No value(s)"}
							return make_response(jsonify(response), 200)
					else:
						response = attribute_values_schema.jsonify(values)
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

	# Add a Value of a Field by Field ID
	@api.doc(
		description = "Add a Value of a Field by Field ID",
		responses = {
			201: "OK",
			403: "Error",
		}
	)
	@token_required
	def post(self, Object_ID, Field_ID):
		try:
			args = request.get_json()

			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				field = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == Object_ID)
					.filter(ADM_ATTRIBUTE_MASTER.ID == Field_ID)
					.first()
				)

				if not field:
					response = {"error": "Field not found"}
					return make_response(jsonify(response), 200)
				else:
					new_attribute_value = attribute_value_schema.load(args, session = db.session)
					
					db.session.add(new_attribute_value)
					db.session.commit()

					response = {"success": "Attribute Value added"}
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
			db.session.rollback()
			db.session.close()

# GET
@api.route("/object_name/<Object>/field_name/<Field_Name>/value")
@api.expect(header_token)
class AttributeValuesByName(Resource):
	# Get ALL Values of a Field by Field Name
	@api.doc(
		description = "Get ALL Values of a Field by Field Name",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Object, Field_Name):
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
				field = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == object.Obj_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.Name == Field_Name)
					.first()
				)

				if not field:
					response = {"error": "Field not found"}
					return make_response(jsonify(response), 200)
				else:
					values = (
						db.session.query(ADM_ATTRIBUTE_VALUE)
						.filter(ADM_ATTRIBUTE_VALUE.Master_ID == field.ID)
						.order_by(ADM_ATTRIBUTE_VALUE.Label)
						.all()
					)

					if not values:
						response = {"error": "No value(s)"}
						return make_response(jsonify(response), 200)
					else:
						response = attribute_values_schema.jsonify(values)
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

# GET
@api.route("/object_name/<Object>/field_id/<Field_ID>/value_id/<Value_ID>")
@api.expect(header_token)
class SingleAttributeValueByObjectName(Resource):
	# Get Attribute Value's Label by Field ID and Value ID
	@api.doc(
		description = "Get Attribute Value's Label by Field ID and Value ID",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Object, Field_ID, Value_ID):
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
				attribute_master = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == object.Obj_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.ID == Field_ID)
					.first()
				)

				if not attribute_master:
					response = {"error": "Attribute Master not found"}
					return make_response(jsonify(response), 200)
				else:
					attribute_value = (
						db.session.query(ADM_ATTRIBUTE_VALUE)
						.filter(ADM_ATTRIBUTE_VALUE.ID == Value_ID)
						.first()
					)

					if not attribute_value:
						response = {"error": "Attribute Value not found"}
						return make_response(jsonify(response), 200)
					else:
						response = attribute_value_schema.jsonify(attribute_value)
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

# PUT, DELETE
@api.route("/object_id/<Object_ID>/field_id/<Field_ID>/value_id/<Value_ID>")
@api.expect(header_token)
class SingleAttributeValueByObjectID(Resource):
	# Update a Value of a Field by Field ID and Value ID
	@api.doc(
		description = "Update a Value of a Field by Field ID and Value ID",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def put(self, Object_ID, Field_ID, Value_ID):
		try:
			args = request.get_json()

			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				field = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == object.Obj_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.ID == Field_ID)
					.first()
				)

				if not field:
					response = {"error": "Field not found"}
					return make_response(jsonify(response), 200)
				else:
					value = (
						db.session.query(ADM_ATTRIBUTE_VALUE)
						.filter(ADM_ATTRIBUTE_VALUE.Master_ID == Field_ID)
						.filter(ADM_ATTRIBUTE_VALUE.ID == Value_ID)
						.first()
					)

					if not value:
						response = {"error": "Value not found"}
						return make_response(jsonify(response), 200)
					else:
						for key in args:
							setattr(value, key, args[key])

						db.session.commit()

						response = {"success": "Attribute Value updated"}
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

	# Delete a Value from a Field
	@api.doc(
		description = "Delete a Value from a Field",
		responses = {
			200: "OK",
			403: "Error",
			200: "Object / Field / Value not found"
		}
	)
	@token_required
	def delete(self, Object_ID, Field_ID, Value_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				master = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == object.Obj_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.ID == Field_ID)
					.first()
				)

				if not master:
					response = {"error": "Field not found"}
					return make_response(jsonify(response), 200)
				
				value = (
					db.session.query(ADM_ATTRIBUTE_VALUE)
					.filter(ADM_ATTRIBUTE_VALUE.Master_ID == master.ID)
					.filter(ADM_ATTRIBUTE_VALUE.ID == Value_ID)
					.first()
				)

				if not value:
					response = {"error": "Value not found"}
					return make_response(jsonify(response), 200)
				else:
					db.session.delete(value)
					db.session.commit()

					response = {"success": "Value deleted"}
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
			db.session.rollback()
			db.session.close()

# GET
@api.route("/<Object>/field_name/<Field_Name>/value/<Value>")
@api.expect(header_token)
class GetAttributeLabelByName(Resource):
	# Get Attribute Value's Label by Field Name and Value
	@api.doc(
		description = "Get Attribute Value's Label by Field Name and Value",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Object, Field_Name, Value):
		try:
			attribute_master = (
				db.session.query(ADM_ATTRIBUTE_MASTER)
				.filter(ADM_ATTRIBUTE_MASTER.Object == Object)
				.filter(ADM_ATTRIBUTE_MASTER.Name == Field_Name)
				.first()
			)

			if not attribute_master:
				response = {"error": "Attribute Master not found"}
				return make_response(jsonify(response), 200)
			else:
				attribute_value = (
					db.session.query(ADM_ATTRIBUTE_VALUE)
					.filter(ADM_ATTRIBUTE_VALUE.Master_ID == attribute_master.ID)
					.filter(ADM_ATTRIBUTE_VALUE.Value == Value)
					.first()
				)

				if not attribute_value:
					response = {"error": "Attribute Value not found"}
					return make_response(jsonify(response), 200)
				else:
					response = attribute_value_schema.jsonify(attribute_value)
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
