const BASE_URL = process.env.REACT_APP_ENDPOINT_URL + ":" + process.env.REACT_APP_SYSTEM_SETTING_PORT;

class SystemSetting {
	get_mail_server() {
		return BASE_URL + "/system_setting/mail_server";
	}

	update_mail_server() {
		return BASE_URL + "/system_setting/mail_server";
	}

	get_workflow_server() {
		return BASE_URL + "/system_setting/workflow_server";
	}

	update_workflow_server() {
		return BASE_URL + "/system_setting/workflow_server";
	}

	test_workflow_server() {
		return BASE_URL + "/system_setting/workflow_server/test_connection";
	}

	get_sqla_server() {
		return BASE_URL + "/system_setting/sqla_server";
	}

	update_sqla_server() {
		return BASE_URL + "/system_setting/sqla_server";
	}

	test_sqla_server() {
		return BASE_URL + "/system_setting/sqla_server/test_connection";
	}

	get_log_setting() {
		return BASE_URL + "/system_setting/logging";
	}

	update_log_setting() {
		return BASE_URL + "/system_setting/logging";
	}

	read_logs(logDate) {
		return BASE_URL + "/system_setting/logs/" + logDate;
	}

	get_authentication_setting() {
		return BASE_URL + "/system_setting/authentication";
	}

	update_authentication_setting() {
		return BASE_URL + "/system_setting/authentication";
	}

	get_sqla_org_mapping() {
		return BASE_URL + "/system_setting/sqla_org_mapping";
	}

	update_sqla_org_mapping() {
		return BASE_URL + "/system_setting/sqla_org_mapping";
	}
}

export default new SystemSetting();
