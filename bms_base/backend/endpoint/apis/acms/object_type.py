import traceback

from flask import jsonify, make_response
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import ADM_OBJ_TYPE_MASTER, ObjectTypeSchema

api = Namespace(path = "/objects", name = "Object")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

object_type_schema = ObjectTypeSchema()
object_types_schema = ObjectTypeSchema(many=True)

# GET
@api.route("/")
@api.expect(header_token)
class Object(Resource):
	# Get ALL Objects
	@api.doc(
		description = "Get ALL Objects",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			object_types = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.all()
			)

			if not object_types:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				response = object_types_schema.jsonify(object_types)
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
@api.route("/<Object_Type_ID>")
@api.expect(header_token)
class SingleObject(Resource):
	# Get Single Object
	@api.doc(
		description = "Get Single Object",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Object_Type_ID):
		try:
			object_type = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_Type_ID)
				.first()
			)

			if not object_type:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				response = object_type_schema.jsonify(object_type)
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
