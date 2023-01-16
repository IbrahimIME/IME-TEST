import traceback

from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource
from sqlalchemy import func, literal_column

from ..system_setting_app import db, logger
from ..token import token_required
from .database.models import (ADM_APP_ACCESS_MASTER, ADM_APP_MODULE_MASTER,
                              ADM_ATTRIBUTE_MASTER, ADM_FEATURE_MASTER,
                              ADM_MAIN_MENU, ADM_OBJ_TYPE_MASTER,
                              ADM_OBJECT_ACCESS_MASTER, ADM_ORG_MASTER,
                              ADM_ORG_USR_MAPPING_MASTER, ADM_ROLE_MASTER,
                              ADM_SENSITIVE_ACCESS_MASTER, ADM_SUB_MENU,
                              ADM_USR_MASTER, AppAccessSchema,
                              AttributeMasterSchema, MainMenuSchema,
                              ObjectAccessSchema, ObjectTypeSchema,
                              OrgUserMappingSchema, ViewEditLimitationSchema)

api = Namespace(path = "/acms", name = "Access Control")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

# Init Schema
main_menus_schema = MainMenuSchema(many=True)
app_access_schema = AppAccessSchema()
app_accesses_schema = AppAccessSchema(many=True)
org_user_mappings_schema = OrgUserMappingSchema(many=True)
view_edits_schema = ViewEditLimitationSchema(many=True)
object_type_masters_schema = ObjectTypeSchema(many=True)
object_accesses_schema = ObjectAccessSchema(many=True)
attribute_masters_schema = AttributeMasterSchema(many=True)

# GET
@api.route("/menu_items")
@api.expect(header_token)
class MenuItems(Resource):
	# Get ALL Menu Items
	@api.doc(
		description = "Get ALL Menu Items",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			main_menu_items = (
				db.session.query(ADM_MAIN_MENU)
				.order_by(ADM_MAIN_MENU.ID)
				.all()
			)

			if not main_menu_items:
				response = {"error": "Menu Item not found"}
				return make_response(jsonify(response), 200)
			else:
				# Loop each menu item and check for sub_menu
				final_menu = []
				for main in main_menu_items:
					sub_menu_items = (
						db.session.query(ADM_SUB_MENU)
						.filter(ADM_SUB_MENU.RefID == main.Sub_ID)
						.all()
					)

					if not sub_menu_items:
						final_menu.append({
							"FeatureCategory": main.FeatureCategory,
							"Name": main.Name,
							"Value": main.Value,
						})
					else:
						sub_menu = []
						for sub in sub_menu_items:
							sub_menu.append({
								"Name": sub.Name,
								"Value": sub.Value
							})

						final_menu.append({
							"FeatureCategory": main.FeatureCategory,
							"Name": main.Name,
							"Value": main.Value,
							"Sub_Menu": sub_menu
						})

				return make_response(jsonify(final_menu), 200)

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
@api.route("/apps_access/<Role_List>")
@api.expect(header_token)
@api.doc(params = {"Role_List": "Separate with '|' (e.g. ROL0001|ROL0002)"})
class AppsAccessApi(Resource):
	# Get ALL Application access for Roles
	@api.doc(
		description = "Get ALL Application access for Roles",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Role_List):
		try:
			roles = Role_List.split("|")

			result = (
				db.session.query(
					ADM_APP_ACCESS_MASTER.App_ID.label("App_ID"),
					ADM_APP_MODULE_MASTER.App_Name.label("App_Name"),
					ADM_APP_MODULE_MASTER.App_Trigram.label("App_Trigram"),
					func.string_agg(ADM_APP_ACCESS_MASTER.Create, literal_column("','")).label("Create"),
					func.string_agg(ADM_APP_ACCESS_MASTER.Read, literal_column("','")).label("Read"),
					func.string_agg(ADM_APP_ACCESS_MASTER.Update, literal_column("','")).label("Update"),
					func.string_agg(ADM_APP_ACCESS_MASTER.Delete, literal_column("','")).label("Delete"),
					func.string_agg(ADM_APP_ACCESS_MASTER.Approve, literal_column("','")).label("Approve")
				)
				.filter(ADM_APP_MODULE_MASTER.App_ID == ADM_APP_ACCESS_MASTER.App_ID)
				.filter(ADM_APP_ACCESS_MASTER.Role_ID.in_(roles))
				.group_by(
					ADM_APP_ACCESS_MASTER.App_ID,
					ADM_APP_MODULE_MASTER.App_Name,
					ADM_APP_MODULE_MASTER.App_Trigram,
				)
				.order_by(ADM_APP_ACCESS_MASTER.App_ID)
				.all()
			)

			if not result:
				response = {"error": "Application Access not found"}
				return make_response(jsonify(response), 200)
			else:
				app_access = []
				for app in result:
					for c in app.Create.split(","):
						if c == "1":
							Create = True
							break
						else:
							Create = False

					for r in app.Read.split(","):
						if r == "1":
							Read = True
							break
						else:
							Read = False

					for u in app.Update.split(","):
						if u == "1":
							Update = True
							break
						else:
							Update = False

					for d in app.Delete.split(","):
						if d == "1":
							Delete = True
							break
						else:
							Delete = False

					for a in app.Approve.split(","):
						if a == "1":
							Approve = True
							break
						else:
							Approve = False

					app_access.append({
						"App_ID": app.App_ID,
						"App_Name": app.App_Name,
						"App_Trigram": app.App_Trigram,
						"Create": Create,
						"Read": Read,
						"Update": Update,
						"Delete": Delete,
						"Approve": Approve,
					})

				return make_response(jsonify(app_access), 200)

		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())
			
			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 200)

		finally:
			db.session.close()

# GET
@api.route("/features_access/<Role_List>")
@api.expect(header_token)
@api.doc(params = {"Role_List": "Separate with '|' (e.g. ROL0001|ROL0002"})
class FeaturesAccessApi(Resource):
	def get(self, Role_List):
		try:
			roles = Role_List.split("|")

			result = (
				db.session.query(
					ADM_APP_ACCESS_MASTER.App_ID,
					ADM_APP_MODULE_MASTER.App_Name,
					ADM_APP_MODULE_MASTER.App_Trigram,
					ADM_FEATURE_MASTER.Feature_ID,
					ADM_FEATURE_MASTER.Feature_Name,
					ADM_FEATURE_MASTER.Feature_Trigram,
					func.string_agg(ADM_APP_ACCESS_MASTER.Create, literal_column("','")).label("Create"),
					func.string_agg(ADM_APP_ACCESS_MASTER.Read, literal_column("','")).label("Read"),
					func.string_agg(ADM_APP_ACCESS_MASTER.Update, literal_column("','")).label("Update"),
					func.string_agg(ADM_APP_ACCESS_MASTER.Delete, literal_column("','")).label("Delete"),
					func.string_agg(ADM_APP_ACCESS_MASTER.Approve, literal_column("','")).label("Approve")
				)
				.filter(ADM_APP_MODULE_MASTER.App_ID == ADM_APP_ACCESS_MASTER.App_ID)
				.filter(ADM_FEATURE_MASTER.Feature_ID == ADM_APP_ACCESS_MASTER.Feature_ID)
				.filter(ADM_APP_ACCESS_MASTER.Role_ID.in_(roles))
				.group_by(
					ADM_APP_ACCESS_MASTER.App_ID,
					ADM_APP_MODULE_MASTER.App_Name,
					ADM_APP_MODULE_MASTER.App_Trigram,
					ADM_FEATURE_MASTER.Feature_ID,
					ADM_FEATURE_MASTER.Feature_Name,
					ADM_FEATURE_MASTER.Feature_Trigram
				)
				.order_by(ADM_APP_ACCESS_MASTER.App_ID)
				.all()
			)

			if not result:
				response = {"error": "Feature Access not found"}
				return make_response(jsonify(response), 403)
			else:
				feature_access = []
				for feature in result:
					for c in feature.Create.split(","):
						if c == "1":
							Create = True
							break
						else:
							Create = False

					for r in feature.Read.split(","):
						if r == "1":
							Read = True
							break
						else:
							Read = False

					for u in feature.Update.split(","):
						if u == "1":
							Update = True
							break
						else:
							Update = False

					for d in feature.Delete.split(","):
						if d == "1":
							Delete = True
							break
						else:
							Delete = False

					for a in feature.Approve.split(","):
						if a == "1":
							Approve = True
							break
						else:
							Approve = False

					feature_access.append({
						"App_ID": feature.App_ID,
						"App_Name": feature.App_Name,
						"App_Trigram": feature.App_Trigram,
						"Feature_ID": feature.Feature_ID,
						"Feature_Name": feature.Feature_Name,
						"Feature_Trigram": feature.Feature_Trigram,
						"Create": Create,
						"Read": Read,
						"Update": Update,
						"Delete": Delete,
						"Approve": Approve,
					})

				return make_response(jsonify(feature_access), 200)

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
@api.route("/objects_access/<Role_List>")
@api.expect(header_token)
class AllObjectAccessesApi(Resource):
	# Get ALL Object accesses of a Role
	@api.doc(
		description = "Get ALL Object accesses of a Role",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, Role_List):
		try:
			roles = Role_List.split("|")

			result = (
				db.session.query(
					ADM_OBJECT_ACCESS_MASTER.Obj_Type_ID.label("Obj_Type_ID"),
					ADM_OBJ_TYPE_MASTER.Obj_Type_Name.label("Obj_Type_Name"),
					func.string_agg(ADM_OBJECT_ACCESS_MASTER.Create, literal_column("','")).label("Create"),
					func.string_agg(ADM_OBJECT_ACCESS_MASTER.Read, literal_column("','")).label("Read"),
					func.string_agg(ADM_OBJECT_ACCESS_MASTER.Update, literal_column("','")).label("Update"),
					func.string_agg(ADM_OBJECT_ACCESS_MASTER.Delete, literal_column("','")).label("Delete"),
					func.string_agg(ADM_OBJECT_ACCESS_MASTER.Approve, literal_column("','")).label("Approve"),
				)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == ADM_OBJECT_ACCESS_MASTER.Obj_Type_ID)
				.filter(ADM_OBJECT_ACCESS_MASTER.Role_ID.in_(roles))
				.group_by(
					ADM_OBJECT_ACCESS_MASTER.Obj_Type_ID,
					ADM_OBJ_TYPE_MASTER.Obj_Type_Name,
				)
				.order_by(ADM_OBJECT_ACCESS_MASTER.Obj_Type_ID)
				.all()
			)

			if not result:
				response = {"error": "Object Access not found"}
				return make_response(jsonify(response), 200)
			else:
				object_access = []
				for object in result:
					for c in object.Create.split(","):
						if c == "1":
							Create = True
							break
						else:
							Create = False

					for r in object.Read.split(","):
						if r == "1":
							Read = True
							break
						else:
							Read = False

					for u in object.Update.split(","):
						if u == "1":
							Update = True
							break
						else:
							Update = False

					for d in object.Delete.split(","):
						if d == "1":
							Delete = True
							break
						else:
							Delete = False

					for a in object.Approve.split(","):
						if a == "1":
							Approve = True
							break
						else:
							Approve = False

					object_access.append({
						"Obj_Type_ID": object.Obj_Type_ID,
						"Obj_Type_Name": object.Obj_Type_Name,
						"Create": Create,
						"Read": Read,
						"Update": Update,
						"Delete": Delete,
						"Approve": Approve,
					})

				return make_response(jsonify(object_access), 200)

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
@api.route("/app/<App_Trigram>/role/<Role_List>/access")
@api.expect(header_token)
@api.doc(params = {"App_Trigram": "BAS, DCM, SND, ...", "Role_List": "Separate with '|' (e.g. ROL0001|ROL0002)"})
class AppAccess(Resource):
	# Get Single Application Access
	@api.doc(
		description = "Get Single Application Access",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, App_Trigram, Role_List):
		try:
			roles = Role_List.split("|")

			application = (
				db.session.query(ADM_APP_MODULE_MASTER)
				.filter(ADM_APP_MODULE_MASTER.App_Trigram == App_Trigram)
				.first()
			)

			if not application:
				response = {"error": "Application not found"}
				return make_response(jsonify(response), 200)
			else:
				role = (
					db.session.query(ADM_ROLE_MASTER)
					.filter(ADM_ROLE_MASTER.Role_ID.in_(roles))
					.first()
				)

				if not role:
					response = {"error": "Role not found"}
					return make_response(jsonify(response), 200)
				else:
					features_access = (
						db.session.query(ADM_APP_ACCESS_MASTER)
						.filter(ADM_APP_ACCESS_MASTER.App_ID == application.App_ID)
						.filter(ADM_APP_ACCESS_MASTER.Role_ID.in_(roles))
						.order_by(ADM_APP_ACCESS_MASTER.Feature_ID)
						.all()
					)

					if not features_access:
						response = {"error": "Access not found"}
						return make_response(jsonify(response), 200)
					else:
						app_access = []
						for access in features_access:
							if access.Create == "1":
								Create = True
							else:
								Create = False

							if access.Read == "1":
								Read = True
							else:
								Read = False

							if access.Update == "1":
								Update = True
							else:
								Update = False

							if access.Delete == "1":
								Delete = True
							else:
								Delete = False

							if access.Approve == "1":
								Approve = True
							else:
								Approve = False

							app_access.append({
								"App_ID": access.App_ID,
								"Feature_ID": access.Feature_ID,
								"Feature_Name": access.adm_feature_master.Feature_Name,
								"Create": Create,
								"Read": Read,
								"Update": Update,
								"Delete": Delete,
								"Approve": Approve
							})

						return make_response(jsonify(app_access), 200)

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
@api.route("/feature/<Feature_Trigram>")
@api.expect(header_token)
@api.doc(params = {"Feature_Trigram": "BAS_PNO, BAS_MAS< DCM_DAM, SNA_QTN, ..."})
class FeatureAccess(Resource):
	# Get Single Feature All Roles Access
	@api.doc(
		description = "Get Single Feature All Roles Access",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Feature_Trigram):
		try:
			feature = (
				db.session.query(ADM_FEATURE_MASTER)
				.filter(ADM_FEATURE_MASTER.Feature_Trigram == Feature_Trigram)
				.first()
			)

			if not feature:
				response = {"error": "Feature not found"}
				return make_response(jsonify(response), 200)
			else:
				feature_accesses = (
					db.session.query(ADM_APP_ACCESS_MASTER)
					.filter(ADM_APP_ACCESS_MASTER.Feature_ID == feature.Feature_ID)
					.order_by(ADM_APP_ACCESS_MASTER.Role_ID)
					.all()
				)

				if not feature_accesses:
					response = {"error": "Feature Access not found"}
					return make_response(jsonify(response), 200)
				else:
					accesses = []
					for row in feature_accesses:
						if row.Create == "1":
							Create = True
						else:
							Create = False

						if row.Read == "1":
							Read = True
						else:
							Read = False

						if row.Update == "1":
							Update = True
						else:
							Update = False

						if row.Delete == "1":
							Delete = True
						else:
							Delete = False

						if row.Approve == "1":
							Approve = True
						else:
							Approve = False

						accesses.append({
							"Feature_ID": row.Feature_ID,
							"Role_ID": row.Role_ID,
							"Role_Name": row.adm_role_master.Role_Name,
							"Create": Create,
							"Read": Read,
							"Update": Update,
							"Delete": Delete,
							"Approve": Approve
						})

					return make_response(jsonify(accesses), 200)

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

	# Update a Feature's Access
	@api.doc(
		description = "Update a Feature's Access",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def put(self, Feature_Trigram):
		try:
			args = request.get_json()

			feature = (
				db.session.query(ADM_FEATURE_MASTER)
				.filter(ADM_FEATURE_MASTER.Feature_Trigram == Feature_Trigram)
				.first()
			)

			if not feature:
				response = {"error": "Feature not found"}
				return make_response(jsonify(response), 200)
			else:
				for row in args:
					access = (
						db.session.query(ADM_APP_ACCESS_MASTER)
						.filter(ADM_APP_ACCESS_MASTER.Feature_ID == feature.Feature_ID)
						.filter(ADM_APP_ACCESS_MASTER.Role_ID == row["Role_ID"])
						.first()
					)

					if access:
						for key in row:
							if key == "Create" or key == "Read" or key == "Update" or key == "Delete" or key == "Approve":
								if row[key] == True:
									row[key] = "1"
								else:
									row[key] = "0"

							setattr(access, key, row[key])

				db.session.commit()

				response = {"success": "Access updated"}
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
@api.route("/feature/<Feature_Trigram>/role/<Role_List>/access")
@api.expect(header_token)
@api.doc(params = {"Feature_Trigram": "BAS_PNO, BAS_MAS, DCM_DAM, SNA_QTN, ...", "Role_List": "Separate with '|' (e.g. ROL0001|ROL0002)"})
class FeatureRoleAccess(Resource):
	# Get Single Feature Access of Role(s)
	@api.doc(
		description = "Get Single Feature Access of Role(s)",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Feature_Trigram, Role_List):
		try:
			roles = Role_List.split("|")

			feature = (
				db.session.query(ADM_FEATURE_MASTER)
				.filter(ADM_FEATURE_MASTER.Feature_Trigram == Feature_Trigram)
				.first()
			)

			if not feature:
				response = {"error": "Feature not found"}
				return make_response(jsonify(response), 200)
			else:
				result = (
					db.session.query(ADM_APP_ACCESS_MASTER)
					.filter(ADM_APP_ACCESS_MASTER.Feature_ID == feature.Feature_ID)
					.filter(ADM_APP_ACCESS_MASTER.Role_ID.in_(roles))
					.all()
				)

				if not result:
					response = {"error": "Feature Access not found"}
					return make_response(jsonify(response), 200)
				else:
					create = False
					read = False
					update = False
					delete = False
					approve = False

					for access in result:
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

					response = {
						"Feature_Trigram": Feature_Trigram,
						"Create": create,
						"Read": read,
						"Update": update,
						"Delete": delete,
						"Approve": approve
					}
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
@api.route("/object/<Object_Type_ID>")
@api.expect(header_token)
class ObjectAccess(Resource):
	# Get Single Object All Role Access
	@api.doc(
		description = "Get Single Object All Role Access",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Object_Type_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_Type_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				result = (
					db.session.query(ADM_OBJECT_ACCESS_MASTER)
					.filter(ADM_OBJECT_ACCESS_MASTER.Obj_Type_ID == Object_Type_ID)
					.order_by(ADM_OBJECT_ACCESS_MASTER.Role_ID)
					.all()
				)

				if not result:
					response = {"error": "Access not found"}
					return make_response(jsonify(response), 200)
				else:
					accesses = []
					for row in result:
						if row.Create == "1":
							Create = True
						else:
							Create = False

						if row.Read == "1":
							Read = True
						else:
							Read = False

						if row.Update == "1":
							Update = True
						else:
							Update = False

						if row.Delete == "1":
							Delete = True
						else:
							Delete = False

						if row.Approve == "1":
							Approve = True
						else:
							Approve = False

						accesses.append({
							"Obj_Type_ID": row.Obj_Type_ID,
							"Role_ID": row.Role_ID,
							"Role_Name": row.adm_role_master.Role_Name,
							"Create": Create,
							"Read": Read,
							"Update": Update,
							"Delete": Delete,
							"Approve": Approve
						})

					return make_response(jsonify(accesses), 200)

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

	# Update Single Object All Role Access
	@api.doc(
		description = "Update Single Object All Role Access",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def put(self, Object_Type_ID):
		try:
			args = request.get_json()

			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_Type_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				for row in args:
					access = (
						db.session.query(ADM_OBJECT_ACCESS_MASTER)
						.filter(ADM_OBJECT_ACCESS_MASTER.Obj_Type_ID == Object_Type_ID)
						.filter(ADM_OBJECT_ACCESS_MASTER.Role_ID == row["Role_ID"])
						.first()
					)

					if access:
						for key in row:
							if key == "Create" or key == "Read" or key == "Update" or key == "Delete" or key == "Approve":
								if row[key] == True:
									row[key] = "1"
								else:
									row[key] = "0"

							setattr(access, key, row[key])

				db.session.commit()

				response = {"success": "Access updated"}
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
@api.route("/object/<Object_Type_ID>/sensitive_fields")
@api.expect(header_token)
class SensitiveFields(Resource):
	# Get Single Object's Sensitive Fields
	@api.doc(
		description = "Get Single Object's Sensitive Fields",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Object_Type_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_Type_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				fields = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == Object_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.Sensitive == True)
					.order_by(ADM_ATTRIBUTE_MASTER.ID)
					.all()
				)

				if not fields:
					response = {"error": "No Sensitive Field(s)"}
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

# GET, PUT
@api.route("/object/<Object_Type_ID>/sensitive_fields/<Attribute_Master_ID>")
@api.expect(header_token)
class SensitiveField(Resource):
	# Get Single Object's Single Sensitive Field
	@api.doc(
		description = "Get Single Object's Single Sensitive Field",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Object_Type_ID, Attribute_Master_ID):
		try:
			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_Type_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				attribute = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == Object_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.ID == Attribute_Master_ID)
					.first()
				)

				if not attribute:
					response = {"error": "Attribute not found"}
					return make_response(jsonify(response), 200)
				else:
					accesses = (
						db.session.query(ADM_SENSITIVE_ACCESS_MASTER)
						.filter(ADM_SENSITIVE_ACCESS_MASTER.Attribute_Master_ID == Attribute_Master_ID)
						.order_by(ADM_SENSITIVE_ACCESS_MASTER.Role_ID)
						.all()
					)

					if not accesses:
						response = {"error": "Access not found"}
					else:
						response = []
						for access in accesses:
							if access.Create == "1":
								create = True
							else:
								create = False

							if access.Read == "1":
								read = True
							else:
								read = False

							if access.Update == "1":
								update = True
							else:
								update = False

							if access.Delete == "1":
								delete = True
							else:
								delete = False

							if access.Approve == "1":
								approve = True
							else:
								approve = False

							response.append({
								"Attribute_Master_ID": access.adm_attribute_master.ID,
								"Attribute_Name": access.adm_attribute_master.Name,
								"Role_ID": access.Role_ID,
								"Role_Name": access.adm_role_master.Role_Name,
								"Create": create,
								"Read": read,
								"Update": update,
								"Delete": delete,
								"Approve": approve
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

	# Update Single Object's Single Sensitive Field
	@api.doc(
		description = "Update Single Object's Single Sensitive Field",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def put(self, Object_Type_ID, Attribute_Master_ID):
		try:
			args = request.get_json()

			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_ID == Object_Type_ID)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				field = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == Object_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.ID == Attribute_Master_ID)
					.first()
				)

				if not field:
					response = {"error": "Field not found"}
					return make_response(jsonify(response), 200)
				else:
					for row in args:
						access = (
							db.session.query(ADM_SENSITIVE_ACCESS_MASTER)
							.filter(ADM_SENSITIVE_ACCESS_MASTER.Attribute_Master_ID == Attribute_Master_ID)
							.filter(ADM_SENSITIVE_ACCESS_MASTER.Role_ID == row["Role_ID"])
							.first()
						)

						if access:
							for key in row:
								if key == "Create" or key == "Read" or key == "Update" or key == "Delete" or key == "Approve":
									if row[key] == True:
										row[key] = "1"
									else:
										row[key] = "0"

								setattr(access, key, row[key])

					db.session.commit()

					response = {"success": "Access updated"}
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
@api.route("/object/<Object_Type_Name>/sensitive_fields/<Field_Name>/role/<Role_List>/access")
@api.expect(header_token)
class SensitiveFieldAccess(Resource):
	# Get Single Sensitive Field Role Access
	@api.doc(
		description = "Get Single Sensitive Field Role Access",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Object_Type_Name, Field_Name, Role_List):
		try:
			roles = Role_List.split("|")

			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_Name == Object_Type_Name)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				attribute_master = (
					db.session.query(ADM_ATTRIBUTE_MASTER)
					.filter(ADM_ATTRIBUTE_MASTER.Obj_Type_ID == object.Obj_Type_ID)
					.filter(ADM_ATTRIBUTE_MASTER.Name == Field_Name)
					.filter(ADM_ATTRIBUTE_MASTER.Sensitive == True)
					.first()
				)

				if not attribute_master:
					response = {"error": "Sensitive Field not found"}
					return make_response(jsonify(response), 200)
				else:
					accesses = (
						db.session.query(ADM_SENSITIVE_ACCESS_MASTER)
						.filter(ADM_SENSITIVE_ACCESS_MASTER.Attribute_Master_ID == attribute_master.ID)
						.filter(ADM_SENSITIVE_ACCESS_MASTER.Role_ID.in_(roles))
						.all()
					)

					if not accesses:
						response = {"error": "Access not found"}
						return make_response(jsonify(response), 200)
					else:
						create = False
						read = False
						update = False
						delete = False
						approve = False

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

						response = {
							"Field_Name": Field_Name,
							"Create": create,
							"Read": read,
							"Update": update,
							"Delete": delete,
							"Approve": approve
						}
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
@api.route("/object/<Object_Type_Name>/role/<Role_List>/access")
@api.expect(header_token)
@api.doc(params = {"Object_Type_Name": "Company, People, Item, Customer, Supplier, ...", "Role_List": "Separate with '|' (e.g. ROL0001|ROL0002)"})
class ObjectRoleAccess(Resource):
	# Get Single Object Access
	@api.doc(
		description = "Get Single Object Access",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Object_Type_Name, Role_List):
		try:
			roles = Role_List.split("|")

			object = (
				db.session.query(ADM_OBJ_TYPE_MASTER)
				.filter(ADM_OBJ_TYPE_MASTER.Obj_Type_Name == Object_Type_Name)
				.first()
			)

			if not object:
				response = {"error": "Object not found"}
				return make_response(jsonify(response), 200)
			else:
				result = (
					db.session.query(ADM_OBJECT_ACCESS_MASTER)
					.filter(ADM_OBJECT_ACCESS_MASTER.Obj_Type_ID == object.Obj_Type_ID)
					.filter(ADM_OBJECT_ACCESS_MASTER.Role_ID.in_(roles))
					.all()
				)

				if not result:
					response = {"error": "Object Access not found"}
					return make_response(jsonify(response), 200)
				else:
					for access in result:
						if access.Create == "1":
							Create = True
						else:
							Create = False

						if access.Read == "1":
							Read = True
						else:
							Read = False

						if access.Update == "1":
							Update = True
						else:
							Update = False

						if access.Delete == "1":
							Delete = True
						else:
							Delete = False

						if access.Approve == "1":
							Approve = True
						else:
							Approve = False

					response = {
						"Obj_Type_ID": object.Obj_Type_ID,
						"Obj_Type_Name": object.Obj_Type_Name,
						"Label_Key": object.Label_Key,
						"Obj_Category": object.Obj_Category,
						"Create": Create,
						"Read": Read,
						"Update": Update,
						"Delete": Delete,
						"Approve": Approve
					}
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
@api.route("/orgs/roles/<User_ID>")
@api.expect(header_token)
class OrgsRolesUserApi(Resource):
	@api.doc(
		description = "Get ALL Roles in All Organisations of an User",
		responses = {
			200: "OK",
			403: "Error",
		}
	)
	@token_required
	def get(self, User_ID):
		try:
			user = (
				db.session.query(ADM_USR_MASTER)
				.filter(ADM_USR_MASTER.User_ID == User_ID)
				.first()
			)

			if not user:
				response = {"error": "User not found"}
				return make_response(jsonify(response), 200)
			else:
				sub_query = (
					db.session.query(
						ADM_ORG_USR_MAPPING_MASTER.Org_ID.label("Org_ID"),
						ADM_ORG_MASTER.Org_Name.label("Org_Name"),
						ADM_ORG_MASTER.Org_Code.label("Org_Code"),
						ADM_ROLE_MASTER.Role_ID.label("Role_ID"),
						ADM_ROLE_MASTER.Role_Name.label("Role_Name")
					)
					.distinct()
					.filter(ADM_ORG_USR_MAPPING_MASTER.Org_ID == ADM_ORG_MASTER.Org_ID)
					.filter(ADM_ORG_USR_MAPPING_MASTER.Role_ID == ADM_ROLE_MASTER.Role_ID)
					.filter(ADM_ORG_USR_MAPPING_MASTER.User_ID == User_ID)
					.subquery()
				)

				org_list = (
					db.session.query(
						sub_query.c.Org_ID,
						sub_query.c.Org_Name,
						sub_query.c.Org_Code,
						func.string_agg(sub_query.c.Role_ID, literal_column("'|'")).label("Role_ID"),
						func.string_agg(sub_query.c.Role_Name, literal_column("', '")).label("Role_Name")
					)
					.group_by(sub_query.c.Org_ID, sub_query.c.Org_Name, sub_query.c.Org_Code)
					.order_by(sub_query.c.Org_ID)
					.all()
				)

				if not org_list:
					response = {"error": "Organisation not found"}
					return make_response(jsonify(response), 200)
				else:
					orgs = []
					for row in org_list:
						orgs.append({
							"Org_ID": row.Org_ID,
							"Org_Name": row.Org_Name,
							"Org_Code": row.Org_Code,
							"Role_ID": row.Role_ID,
							"Role_Name": row.Role_Name
						})
						
					return make_response(jsonify(orgs), 200)

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
