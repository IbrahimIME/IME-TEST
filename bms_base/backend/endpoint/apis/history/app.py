from .cmm import api as bas_cmm
from .dam import api as dcm_dam
from .mas import api as bas_mas
from .pno import api as bas_pno

def initialize_history(api):
	api.add_namespace(bas_cmm)
	api.add_namespace(bas_mas)
	api.add_namespace(bas_pno)
	api.add_namespace(dcm_dam)
	