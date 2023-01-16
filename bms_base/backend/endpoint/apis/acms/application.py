import traceback

from flask import jsonify, make_response
from flask_restx import Namespace, Resource

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import ADM_APP_MODULE_MASTER, ApiModel, AppModuleSchema

api = Namespace(path = "/applications", name = "Application")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

app_module_schema = AppModuleSchema()
app_modules_schema = AppModuleSchema(many=True)

app_body = api.model("app_body", ApiModel.app_body)

# GET
@api.route("")
@api.expect(header_token)
class ApplicationMaster(Resource):
	# Get ALL Applications
	@api.doc(
		description = "Get ALL Applications",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self):
		try:
			apps = (
				db.session.query(ADM_APP_MODULE_MASTER)
				.order_by(ADM_APP_MODULE_MASTER.App_ID)
				.all()
			)

			if not apps:
				response = {"error": "Application not found"}
				return make_response(jsonify(response), 200)
			else:
				response = app_modules_schema.jsonify(apps)
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
@api.route("/<App_ID>")
@api.expect(header_token)
class SingleApplication(Resource):
	# Get Single Application
	@api.doc(
		description = "Get Single Application",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, App_ID):
		try:
			app = (
				db.session.query(ADM_APP_MODULE_MASTER)
				.filter(ADM_APP_MODULE_MASTER.App_ID == App_ID)
				.first()
			)

			if not app:
				response = {"error": "Application not found"}
				return make_response(jsonify(response), 200)
			else:
				response = app_module_schema.jsonify(app)
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
