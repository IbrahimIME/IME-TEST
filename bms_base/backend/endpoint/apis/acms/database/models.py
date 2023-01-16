from flask_restx import fields

from ...system_setting_app import Base, ma

# DB Table
ADM_MAIN_MENU				= Base.classes.ADM_MAIN_MENU
ADM_SUB_MENU				= Base.classes.ADM_SUB_MENU
ADM_ORG_USR_MAPPING_MASTER 	= Base.classes.ADM_ORG_USR_MAPPING_MASTER
ADM_APP_ACCESS_MASTER 		= Base.classes.ADM_APP_ACCESS_MASTER
ADM_APP_MODULE_MASTER 		= Base.classes.ADM_APP_MODULE_MASTER
ADM_FEATURE_MASTER 			= Base.classes.ADM_FEATURE_MASTER
ADM_OBJECT_ACCESS_MASTER 	= Base.classes.ADM_OBJECT_ACCESS_MASTER
ADM_APP_MAPPING_MASTER 		= Base.classes.ADM_APP_MAPPING_MASTER
ADM_USR_MASTER 				= Base.classes.ADM_USR_MASTER
ADM_ORG_MASTER 				= Base.classes.ADM_ORG_MASTER
ADM_ROLE_MASTER				= Base.classes.ADM_ROLE_MASTER
ADM_VIEW_EDIT_LIMITATION	= Base.classes.ADM_VIEW_EDIT_LIMITATION
ADM_FIELD_LIMITATION		= Base.classes.ADM_FIELD_LIMITATION
ADM_OBJ_TYPE_MASTER			= Base.classes.ADM_OBJ_TYPE_MASTER
ADM_ATTRIBUTE_MASTER		= Base.classes.ADM_ATTRIBUTE_MASTER
ADM_SENSITIVE_ACCESS_MASTER	= Base.classes.ADM_SENSITIVE_ACCESS_MASTER

# Schema
class MainMenuSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_MAIN_MENU
		load_instance = True

class OrgSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_ORG_MASTER
		load_instance = True

class RoleSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_ROLE_MASTER
		load_instance = True

class OrgUserMappingSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_ORG_USR_MAPPING_MASTER
		include_relationships = True
		load_instance = True
	adm_org_master = ma.Nested(OrgSchema)
	adm_role_master = ma.Nested(RoleSchema)

class AppModuleSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_APP_MODULE_MASTER
		load_instance = True

class FeatureSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_FEATURE_MASTER
		load_instance = True

class AppAccessSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_APP_ACCESS_MASTER
		include_fk = True
		include_relationships = True
		load_instance = True
	adm_app_module_master = ma.Nested(AppModuleSchema)
	adm_feature_master = ma.Nested(FeatureSchema)
	adm_role_master = ma.Nested(RoleSchema)

class AppMappingSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_APP_MAPPING_MASTER
		# include_relationship = True
		load_instance = True
	adm_app_module_master = ma.Nested(AppModuleSchema)
	adm_feature_master = ma.Nested(FeatureSchema)

class FieldLimitationSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_FIELD_LIMITATION
		load_instance = True

class ViewEditLimitationSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_VIEW_EDIT_LIMITATION
		include_relationships = True
		load_instance = True
	adm_field_limitation = ma.Nested(FieldLimitationSchema)

class ObjectTypeSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_OBJ_TYPE_MASTER
		include_fk = True
		load_instance = True

class ObjectAccessSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_OBJECT_ACCESS_MASTER
		include_fk = True
		include_relationships = True
		load_instance = True

class AttributeMasterSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_ATTRIBUTE_MASTER
		include_fk = True
		include_relationships = True
		load_instance = True

class ApiModel():
	# Api Model
	app_body = {
		"App_Name": fields.String,
		"App_Trigram": fields.String,
		"App_Description": fields.String
	}
