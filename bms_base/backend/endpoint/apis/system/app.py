from .additional_attribute import api as additional_attribute
from .attribute import api as attribute
from .import_history import api as import_history
from .logging import api as logging
from .prefix import api as prefix
from .system_setting import api as system_setting

def initialize_system_setting(api):
	api.add_namespace(additional_attribute)
	api.add_namespace(attribute)
	api.add_namespace(import_history)
	api.add_namespace(logging)
	api.add_namespace(prefix)
	api.add_namespace(system_setting)
	