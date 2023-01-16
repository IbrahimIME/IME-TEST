import traceback

from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import ADM_PREFIX_MASTER, ApiModel, PrefixSchema

api = Namespace(path = "/system_setting/prefix", name = "Prefix")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

# Init Schema
prefix_schema = PrefixSchema()
prefixes_schema = PrefixSchema(many=True)

# Api Model
prefix_body = api.model("prefix_body", model = ApiModel.prefix_body)

# GET, POST
@api.route("")
@api.expect(header_token)
class PrefixMaster(Resource):
	# Get ALL Prefixes
	@api.doc(
		description = "Get ALl Prefixes",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self):
		try:
			prefixes = (
				db.session.query(ADM_PREFIX_MASTER)
				.order_by(ADM_PREFIX_MASTER.Prefix_ID)
				.all()
			)

			if not prefixes:
				response = {"error": "Prefix not found"}
				return make_response(jsonify(response), 200)
			else:
				response = prefixes_schema.jsonify(prefixes)
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

	# Add a new Prefix
	@api.doc(
		description = "Add a Prefix",
		body = prefix_body,
		responses = {
			201: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self):
		try:
			args = request.get_json()

			new_prefix = prefix_schema.load(args, session = db.session)

			db.session.add(new_prefix)
			db.session.commit()

			response = {"success": "Prefix created successfully"}
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

# GET, PUT, DELETE
@api.route("/<Prefix_ID>")
@api.expect(header_token)
class SinglePrefix(Resource):
	# Get Single Prefix
	@api.doc(
		description = "Get Single Prefix",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Prefix_ID):
		try:
			prefix = (
				db.session.query(ADM_PREFIX_MASTER)
				.filter(ADM_PREFIX_MASTER.Prefix_ID == Prefix_ID)
				.first()
			)

			if not prefix:
				response = {"error": "Prefix not found"}
				return make_response(jsonify(response), 200)
			else:
				response = prefix_schema.jsonify(prefix)
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

	# Update a Prefix
	@api.doc(
		description = "Update a Prefix",
		body = prefix_body,
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def put(self, Prefix_ID):
		try:
			args = request.get_json()

			prefix = (
				db.session.query(ADM_PREFIX_MASTER)
				.filter(ADM_PREFIX_MASTER.Prefix_ID == Prefix_ID)
				.first()
			)

			if not prefix:
				response = {"error": "Prefix not found"}
				return make_response(jsonify(response), 200)
			else:
				for key in args:
					setattr(prefix, key, args[key])

				db.session.commit()

				response = {"success": "Prefix updated successfully"}
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

	# Delete a Prefix
	@api.doc(
		description = "Delete a Prefix",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def delete(self, Prefix_ID):
		try:
			prefix = (
				db.session.query(ADM_PREFIX_MASTER)
				.filter(ADM_PREFIX_MASTER.Prefix_ID == Prefix_ID)
				.first()
			)

			if not prefix:
				response = {"error": "Prefix not found"}
				return make_response(jsonify(response), 200)
			else:
				db.session.delete(prefix)
				db.session.commit()

				response = {"success": "Prefix deleted"}
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
