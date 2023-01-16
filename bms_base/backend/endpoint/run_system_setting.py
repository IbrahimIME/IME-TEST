import os

from apis.acms.app import initialize_acms
from apis.history.app import initialize_history
from apis.notfound import api as notfound
from apis.system.app import initialize_system_setting
from apis.system_setting_app import api, app, logger

initialize_system_setting(api)
initialize_acms(api)
initialize_history(api)

api.add_namespace(notfound)

# Run Server
if __name__ == "__main__":
	logger.info("Environment: " + os.getenv("ENVIRONMENT"))
	logger.info("Running on port " + os.getenv("SYSTEM_SETTING_PORT"))

	app.run(
		debug = False if os.getenv("ENVIRONMENT") == "PRODUCTION" else True,
		host = "0.0.0.0",
		port = os.getenv("SYSTEM_SETTING_PORT"),
		# ssl_context = (os.getenv("SSL_CERT"), os.getenv("SSL_KEY"))
	)
