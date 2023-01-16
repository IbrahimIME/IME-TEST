from flask_restx import fields
from marshmallow import fields as ma_fields

from ...system_setting_app import Base, ma

# DB Table
ADM_IMPORT_HISTORY				= Base.classes.ADM_IMPORT_HISTORY
ADM_OBJ_TYPE_MASTER				= Base.classes.ADM_OBJ_TYPE_MASTER
ADM_ATTRIBUTE_MASTER			= Base.classes.ADM_ATTRIBUTE_MASTER
ADM_ATTRIBUTE_VALUE				= Base.classes.ADM_ATTRIBUTE_VALUE
ADM_ADDITIONAL_ATTRIBUTE		= Base.classes.ADM_ADDITIONAL_ATTRIBUTE
ADM_SYS_SETTING 				= Base.classes.ADM_SYS_SETTING
ADM_SETTING_MAPPING 			= Base.classes.ADM_SETTING_MAPPING
ADM_PREFIX_MASTER 				= Base.classes.ADM_PREFIX_MASTER
ADM_OBJECT_LOGGING_MASTER 		= Base.classes.ADM_OBJECT_LOGGING_MASTER
ADM_OBJECT_LOGGING_EXTENDED 	= Base.classes.ADM_OBJECT_LOGGING_EXTENDED
ADM_ROLE_MASTER					= Base.classes.ADM_ROLE_MASTER
ADM_SENSITIVE_ACCESS_MASTER		= Base.classes.ADM_SENSITIVE_ACCESS_MASTER
ADM_ORG_MASTER					= Base.classes.ADM_ORG_MASTER
ADM_SQLA_ORG_MAPPING			= Base.classes.ADM_SQLA_ORG_MAPPING
ADM_USER_ACTIVITY				= Base.classes.ADM_USER_ACTIVITY

# DB Schema
class ImportHistorySchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_IMPORT_HISTORY
		load_instance = True

class ObjectTypeMasterSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_OBJ_TYPE_MASTER
		load_instance = True

class AttributeMasterSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_ATTRIBUTE_MASTER
		include_fk = True
		load_instance = True

class AttributeValueSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_ATTRIBUTE_VALUE
		load_instance = True

class AdditionalAttributeSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_ADDITIONAL_ATTRIBUTE
		include_fk = True
		include_relationship = True
		load_instance = True
	adm_attribute_master = ma.Nested(AttributeMasterSchema)
	adm_attribute_value = ma.Nested(AttributeValueSchema)

class SysSettingSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_SYS_SETTING
		load_instance = True

class SettingMappingSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_SETTING_MAPPING
		include_relationships = True
		load_instance = True
	adm_sys_setting = ma.Nested(SysSettingSchema)

class PrefixSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_PREFIX_MASTER
		load_instance = True

class LoggingExtendedSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_OBJECT_LOGGING_EXTENDED
		load_instance = True

class LoggingMasterSchema(ma.SQLAlchemyAutoSchema):
	Time = ma_fields.DateTime("%Y-%m-%d %H:%M:%S")
	class Meta:
		model = ADM_OBJECT_LOGGING_MASTER
		include_relationships = True
		load_instance = True
	adm_object_logging_extended = ma.Nested(LoggingExtendedSchema)

class OrgSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_ORG_MASTER
		load_instance = True

class SQLAOrgSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_SQLA_ORG_MAPPING
		include_fk = True
		include_relationships = True
		load_instance = True
	adm_org_master = ma.Nested(OrgSchema)

class ActivityLogSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = ADM_USER_ACTIVITY
		include_fk = True
		load_instance = True

# Api Model
class ApiModel():
	# Mail Server setting
	mail_server_body = {
		"HOST": fields.String,
		"PORT": fields.Integer,
		"USER": fields.String,
		"PASSWORD": fields.String
	}

	# System Logging Level
	logging_level_body = {
		"BACKEND_LVL": fields.String,
		"DB_LVL": fields.String,
	}

	# Prefix
	prefix_body = {
		"Prefix_Name": fields.String,
		"Prefix_Description": fields.String,
		"Running_Number": fields.Integer,
		"Value": fields.Integer,
		"Separator": fields.String,
		"Suffix": fields.String,
	}

	# Object Log
	object_log_body = {
		"User": fields.String,
		"Org": fields.String,
		"Roles": fields.String,
		"Action": fields.String,
		"Object": fields.String,
		"Object_ID": fields.String,
	}


