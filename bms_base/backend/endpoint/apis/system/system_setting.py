import os
import pathlib
import traceback

import requests
from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource
from sqlalchemy import func

from ..log_configs import LevelFilter
from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import (ADM_SETTING_MAPPING, ADM_SQLA_ORG_MAPPING,
                              ADM_SYS_SETTING, ApiModel, SettingMappingSchema,
                              SQLAOrgSchema)

api = Namespace(path = "/system_setting", name = "System Setting")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

setting_mappings_schema = SettingMappingSchema(many=True)

sqla_orgs_schema = SQLAOrgSchema(many=True)

# Api Model
mail_server_body = api.model("mail_server_body", model = ApiModel.mail_server_body)
logging_level_body = api.model("logging_level_body", model = ApiModel.logging_level_body)

# GET
@api.route("/<Setting_Name>")
@api.expect(header_token)
class SystemSettingApi(Resource):
	# Get System Settings
	@api.doc(
		description = "Get System Settings",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Setting_Name):
		try:
			system_setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(func.upper(ADM_SYS_SETTING.Sys_Name) == Setting_Name.upper())
				.first()
			)

			if not system_setting:
				response = {"error": "System Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				settings = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == system_setting.Sys_ID)
					.all()
				)

				if not settings:
					response = {"error": "System Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					response = {}
					for row in settings:
						response[row.Additional_Name] = row.Additional_Value

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

# GET, PUT
@api.route("/mail_server")
@api.expect(header_token)
class MailServerApi(Resource):
	# Get Mail Server settings
	@api.doc(
		description = "Get Mail Server settings",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self):
		try:
			setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(func.upper(ADM_SYS_SETTING.Sys_Name) == "SMTP")
				.first()
			)

			if not setting:
				response = {"error": "System Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				settings = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == setting.Sys_ID)
					.all()
				)

				if not settings:
					response = {"error": "System Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					response = {}
					for row in settings:
						response[row.Additional_Name] = row.Additional_Value

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

	# Update Mail Server settings
	@api.doc(
		description = "Update Mail Server settings",
		body = mail_server_body,
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def put(self):
		try:
			args = request.get_json()

			system_setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(func.upper(ADM_SYS_SETTING.Sys_Name) == "SMTP")
				.first()
			)

			if not system_setting:
				response = {"error": "Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				settings = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == system_setting.Sys_ID)
					.all()
				)

				if not settings:
					response = {"error": "Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					for key in args:
						setting = (
							db.session.query(ADM_SETTING_MAPPING)
							.filter(ADM_SETTING_MAPPING.Sys_ID == system_setting.Sys_ID)
							.filter(ADM_SETTING_MAPPING.Additional_Name == key)
							.first()
						)

						if setting:
							setting.Additional_Value = args[key]
						else:
							db.session.rollback()

							response = {"error": key + " setting not found"}
							return make_response(jsonify(response), 200)

					db.session.commit()

					response = {"success": "System Settings updated"}
					return make_response(jsonify(response), 200)
						
		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())
			
			db.session.rollback()

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)
		
		finally:
			db.session.close()

# GET, PUT
@api.route("/workflow_server")
@api.expect(header_token)
class WorkflowServer(Resource):
	# Get Workflow Server setting
	@api.doc(
		description = "Get Workflow Server setting",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(ADM_SYS_SETTING.Sys_Name == "WORKFLOW SERVER")
				.first()
			)

			if not setting:
				response = {"error": "System Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				result = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == setting.Sys_ID)
					.all()
				)

				if not result:
					response = {"error": "Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					response = {}
					for row in result:
						response[row.Additional_Name] = row.Additional_Value
					
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

	# Update Workflow Server Setting
	@api.doc(
		description = "Update Workflow Server Setting",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def put(self):
		try:
			args = request.get_json()

			setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(ADM_SYS_SETTING.Sys_Name == "WORKFLOW SERVER")
				.first()
			)

			if not setting:
				response = {"error": "System Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				result = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == setting.Sys_ID)
					.all()
				)

				if not result:
					response = {"error": "Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					for key in args:
						setting = (
							db.session.query(ADM_SETTING_MAPPING)
							.filter(ADM_SETTING_MAPPING.Sys_ID == setting.Sys_ID)
							.filter(ADM_SETTING_MAPPING.Additional_Name == key)
							.first()
						)

						if setting:
							setting.Additional_Value = args[key]
						else:
							db.session.rollback()

							response = {"error": key + " setting not found"}
							return make_response(jsonify(response), 200)

					db.session.commit()

					response = {"success": "Workflow Server Setting updated"}
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

# POST
@api.route("/workflow_server/test_connection")
@api.expect(header_token)
class WorkflowTestConnection(Resource):
	# Test Workflow Server Connection
	@api.doc(
		description = "Test Workflow Server Connection",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self):
		try:
			args = request.get_json()

			if args["url"]:
				result = requests.get(args["url"] + "/engine-rest/version")
				response = result.json()
				return make_response(jsonify(response), result.status_code)
			
			else:
				response = {"error": "No URL"}
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

# GET, PUT
@api.route("/sqla_server")
@api.expect(header_token)
class SQLAServer(Resource):
	# Get SQLA Server setting
	@api.doc(
		description = "Get SQLA Server setting",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(ADM_SYS_SETTING.Sys_Name == "SQLA SERVER")
				.first()
			)

			if not setting:
				response = {"error": "System Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				result = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == setting.Sys_ID)
					.all()
				)

				if not result:
					response = {"error": "Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					response = {}
					for row in result:
						response[row.Additional_Name] = row.Additional_Value
					
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

	# Update SQLA Server Setting
	@api.doc(
		description = "Update SQLA Server Setting",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def put(self):
		try:
			args = request.get_json()

			setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(ADM_SYS_SETTING.Sys_Name == "SQLA SERVER")
				.first()
			)

			if not setting:
				response = {"error": "System Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				result = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == setting.Sys_ID)
					.all()
				)

				if not result:
					response = {"error": "Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					for key in args:
						setting = (
							db.session.query(ADM_SETTING_MAPPING)
							.filter(ADM_SETTING_MAPPING.Sys_ID == setting.Sys_ID)
							.filter(ADM_SETTING_MAPPING.Additional_Name == key)
							.first()
						)

						if setting:
							setting.Additional_Value = args[key]
						else:
							db.session.rollback()

							response = {"error": key + " setting not found"}
							return make_response(jsonify(response), 200)

					db.session.commit()

					response = {"success": "Workflow Server Setting updated"}
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

# POST
@api.route("/sqla_server/test_connection")
@api.expect(header_token)
class SQLATestConnection(Resource):
	# Test SQLA Server Connection
	@api.doc(
		description = "Test SQLA Server Connection",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self):
		try:
			args = request.get_json()

			if args:
				if "web_port" in args and "url" in args and "Org_ID" in args:
					sqla_org = (
						db.session.query(ADM_SQLA_ORG_MAPPING)
						.filter(ADM_SQLA_ORG_MAPPING.Org_ID == args["Org_ID"])
						.first()
					)

					if not sqla_org:
						response = {"error": ""}
						return make_response(jsonify(response), 200)

					else:
						json = {
							"UserName": sqla_org.UserName,
							"PassWord": sqla_org.Password,
							"dbname": sqla_org.Database,
							"path": sqla_org.Path
						}

						result = requests.post(
							"http://localhost:" + args["web_port"] + "/test_connection",
							json = { 
								"url": args["url"] + "/test_connection",
								"sqladb": json
							}
						)
						response = result.json()
						return make_response(jsonify(response), result.status_code)

				elif "web_port" not in args:
					response = {"error": "SQLA Web Port is empty"}
					return make_response(jsonify(response), 200)

				elif "url" not in args:
					response = {"error": "SQLA Host or Port is empty"}
					return make_response(jsonify(response), 200)

				elif "Org_ID" in args:
					response = {"error": "Org ID is empty"}
					return make_response(jsonify(response), 200)
			
			else:
				response = {"error": "No URL"}
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

# GET, PUT
@api.route("/logging")
@api.expect(header_token)
class LogSettingApi(Resource):
	# Get System Logging settings
	@api.doc(
		description = "Get System Logging settings",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self):
		try:
			system_setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(func.upper(ADM_SYS_SETTING.Sys_Name) == "LOG SETTING")
				.first()
			)

			if not system_setting:
				response = {"error": "System Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				settings = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == system_setting.Sys_ID)
					.all()
				)

				if not settings:
					response = {"error": "System Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					response = {}
					for row in settings:
						response[row.Additional_Name] = row.Additional_Value

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

	# Update System Logging settings
	@api.doc(
		description = "Update System Logging settings (<strong>BACKEND_LVL</strong>: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL; <strong>DB_LVL</strong>: LOG, INFO, NOTICE, WARNING, ERROR)",
		body = logging_level_body,
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def put(self):
		try:
			args = request.get_json()

			system_setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(func.upper(ADM_SYS_SETTING.Sys_Name) == "LOG SETTING")
				.first()
			)

			if not system_setting:
				response = {"error": "Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				settings = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == system_setting.Sys_ID)
					.all()
				)

				if not settings:
					response = {"error": "Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					for key in args:
						setting = (
							db.session.query(ADM_SETTING_MAPPING)
							.filter(ADM_SETTING_MAPPING.Sys_ID == system_setting.Sys_ID)
							.filter(ADM_SETTING_MAPPING.Additional_Name == key)
							.first()
						)

						if setting:
							setting.Additional_Value = args[key]
							db.session.commit()

							if key == "BACKEND_LVL":
								for handler in logger.handlers:
									if args[key] == "NOTSET":
										handler.addFilter(LevelFilter(0, 0))

									elif args[key] == "DEBUG":
										handler.addFilter(LevelFilter(10, 50))

									elif args[key] == "INFO":
										handler.addFilter(LevelFilter(20, 50))

									elif args[key] == "WARNING":
										handler.addFilter(LevelFilter(30, 50))

									elif args[key] == "ERROR":
										handler.addFilter(LevelFilter(40, 50))

									elif args[key] == "CRITICAL":
										handler.addFilter(LevelFilter(50, 50))
								
								logger.critical("Logging " + key + " changed to " + args[key])

						else:
							response = {"error": key + " setting not found"}
							return make_response(jsonify(response), 200)


					response = {"success": "System Settings updated"}
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

# GET
@api.route("/logs/<LogDate>")
@api.expect(header_token)
class Logs(Resource):
	# Get Logs
	@api.doc(
		description = "Get Logs",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, LogDate):
		try:
			logs_folder_path = os.path.dirname(__file__) + "\\..\\..\\logs\\"
			mainFile = logs_folder_path + LogDate + "_werkzeug_log.log"
			adminFile = logs_folder_path + "apis.admin_app\\" + LogDate + ".log"
			authFile = logs_folder_path + "apis.auth_app\\" + LogDate + ".log"
			documentFile = logs_folder_path + "apis.document_management_app\\" + LogDate + ".log"
			masterFile = logs_folder_path + "apis.master_data_app\\" + LogDate + ".log"
			systemFile = logs_folder_path + "apis.system_setting_app\\" + LogDate + ".log"

			if os.path.exists(logs_folder_path):
				if os.path.exists(mainFile):
					with open(mainFile, 'r') as file:
						mainData = file.read()
				else:
					mainData = ""

				if os.path.exists(adminFile):
					with open(adminFile, 'r') as file:
						adminData = file.read()
				else:
					adminData = ""

				if os.path.exists(authFile):
					with open(authFile, 'r') as file:
						authData = file.read()
				else:
					authData = ""

				if os.path.exists(documentFile):
					with open(documentFile, 'r') as file:
						documentData = file.read()
				else:
					documentData = ""

				if os.path.exists(masterFile):
					with open(masterFile, 'r') as file:
						masterData = file.read()
				else:
					masterData = ""

				if os.path.exists(systemFile):
					with open(systemFile, 'r') as file:
						systemData = file.read()
				else:
					systemData = ""

				response = {
					"mainLogs": mainData,
					"adminLogs": adminData,
					"authLogs": authData,
					"documentLogs": documentData,
					"masterLogs": masterData,
					"systemLogs": systemData
				}
				return make_response(jsonify(response), 200)

			else:
				response = {"error": "No Log"}
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

# GET, PUT
@api.route("/authentication")
@api.expect(header_token)
class Authentication(Resource):
	# Get Authentication Setting
	@api.doc(
		description = "Get Authentication Setting",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			system_setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(func.upper(ADM_SYS_SETTING.Sys_Name) == "AUTHENTICATION")
				.first()
			)

			if not system_setting:
				response = {"error": "System Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				settings = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == system_setting.Sys_ID)
					.all()
				)

				if not settings:
					response = {"error": "System Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					response = {}
					for row in settings:
						response[row.Additional_Name] = row.Additional_Value

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

	# Update Authentication Setting
	@api.doc(
		description = "Update Authentication Setting",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def put(self):
		try:
			args = request.get_json()

			system_setting = (
				db.session.query(ADM_SYS_SETTING)
				.filter(func.upper(ADM_SYS_SETTING.Sys_Name) == "AUTHENTICATION")
				.first()
			)

			if not system_setting:
				response = {"error": "Setting not found"}
				return make_response(jsonify(response), 200)
			else:
				settings = (
					db.session.query(ADM_SETTING_MAPPING)
					.filter(ADM_SETTING_MAPPING.Sys_ID == system_setting.Sys_ID)
					.all()
				)

				if not settings:
					response = {"error": "Setting not found"}
					return make_response(jsonify(response), 200)
				else:
					for key in args:
						setting = (
							db.session.query(ADM_SETTING_MAPPING)
							.filter(ADM_SETTING_MAPPING.Sys_ID == system_setting.Sys_ID)
							.filter(ADM_SETTING_MAPPING.Additional_Name == key)
							.first()
						)

						if setting:
							setting.Additional_Value = args[key]
							db.session.commit()

						else:
							response = {"error": key + " setting not found"}
							return make_response(jsonify(response), 200)


					response = {"success": "System Settings updated"}
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

# GET, PUT
@api.route("/sqla_org_mapping")
@api.expect(header_token)
class SQLAOrgMapping(Resource):
	# Get SQLA Org Mapping
	@api.doc(
		description = "Get SQLA Org Mapping",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			sqla_orgs = (
				db.session.query(ADM_SQLA_ORG_MAPPING)
				.order_by(ADM_SQLA_ORG_MAPPING.Org_ID)
				.all()
			)

			if not sqla_orgs:
				response = {"error": "SQLA Org Mapping not found"}
				return make_response(jsonify(response), 200)
			else:
				response = sqla_orgs_schema.jsonify(sqla_orgs)
				return make_response(response, 200)

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

	# Update SQLA Org Mapping
	@api.doc(
		description = "Update SQLA Org Mapping",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def put(self):
		try:
			args = request.get_json()

			if "Org_ID" not in args:
				response = {"error": "Org ID not provided"}
				return make_response(jsonify(response), 200)
			else:
				sqla_org = (
					db.session.query(ADM_SQLA_ORG_MAPPING)
					.filter(ADM_SQLA_ORG_MAPPING.Org_ID == args["Org_ID"])
					.first()
				)

				if not sqla_org:
					response = {"error": "SQLA Org Mapping not found"}
					return make_response(jsonify(response), 200)
				else:
					for key in args:
						setattr(sqla_org, key, args[key])
						
					db.session.commit()

					response = {"success": "SQLA Org Mapping updated"}
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
