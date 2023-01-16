import traceback

from flask import jsonify, make_response
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import ADM_FEATURE_MASTER, ApiModel, FeatureSchema

api = Namespace(path = "/admin/applications", name = "Feature Master")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)

# GET
@api.route("")
@api.expect(header_token)
class FeatureMaster(Resource):
	# Get ALL Features
	@api.doc(
		description = "Get ALL Features",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self):
		try:
			features = (
				db.session.query(ADM_FEATURE_MASTER)
				.all()
			)

			if not features:
				response = {"error": "Feature not found"}
				return make_response(jsonify(response), 200)
			else:
				response = features_schema.jsonify(features)
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
@api.route("/<Feature_ID>")
@api.expect(header_token)
class SingleFeature(Resource):
	# Get Single Feature
	@api.doc(
		description = "Get Single Feature",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Feature_ID):
		try:
			feature = (
				db.session.query(ADM_FEATURE_MASTER)
				.filter(ADM_FEATURE_MASTER.Feature_ID == Feature_ID)
				.first()
			)

			if not feature:
				response = {"error": "Feature not found"}
				return make_response(jsonify(response), 200)
			else:
				response = feature_schema.jsonify(feature)
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
