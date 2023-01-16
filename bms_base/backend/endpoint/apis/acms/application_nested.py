import traceback

from flask import jsonify, make_response
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import (ADM_APP_MAPPING_MASTER, ADM_FEATURE_MASTER,
                              AppMappingSchema, FeatureSchema)

api = Namespace(path = "/applications", name = "Application (Nested)")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)
app_mappings_schema = AppMappingSchema(many=True)

# GET
@api.route("/<App_ID>/features")
@api.expect(header_token)
class Features(Resource):
	# Get ALL Features of an Application
	@api.doc(
		description = "Get ALL Features of an Application",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, App_ID):
		try:
			app_feature_mappings = (
				db.session.query(ADM_APP_MAPPING_MASTER)
				.filter(ADM_APP_MAPPING_MASTER.App_ID == App_ID)
				.all()
			)

			if not app_feature_mappings:
				response = {"error": "Application not found"}
				return make_response(jsonify(response), 200)
			else:
				features_id = []
				for row in app_feature_mappings:
					features_id.append(row.Feature_ID)

				features = (
					db.session.query(ADM_FEATURE_MASTER)
					.filter(ADM_FEATURE_MASTER.Feature_ID.in_(features_id))
					.order_by(ADM_FEATURE_MASTER.Feature_ID)
					.all()
				)

				if not features:
					response = {"error": "Feature Master not found"}
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
@api.route("/<App_ID>/features/<Feature_ID>")
@api.expect(header_token)
class SingleFeature(Resource):
	# Get Single Feature of an Application
	@api.doc(
		description = "Get Single Feature of an Application",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, App_ID, Feature_ID):
		try:
			result = (
				db.session.query(ADM_APP_MAPPING_MASTER)
				.filter(ADM_APP_MAPPING_MASTER.App_ID == App_ID)
				.filter(ADM_APP_MAPPING_MASTER.Feature_ID == Feature_ID)
				.first()
			)

			if not result:
				response = {"error": "Application / Feature not found"}
				return make_response(jsonify(response), 200)
			else:
				response = feature_schema.jsonify(result.adm_feature_master)
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
