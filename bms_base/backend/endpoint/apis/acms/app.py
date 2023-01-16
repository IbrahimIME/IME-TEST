from .acms import api as acms
from .application import api as app
from .application_nested import api as app_nested
from .object_type import api as object_type

def initialize_acms(api):
	api.add_namespace(acms)
	api.add_namespace(app)
	api.add_namespace(app_nested)
	api.add_namespace(object_type)
