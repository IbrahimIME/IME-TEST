const BASE_URL = process.env.REACT_APP_ENDPOINT_URL + ":" + process.env.REACT_APP_SYSTEM_SETTING_PORT;

class ActivityLog {
	save_log() {
		return BASE_URL + "/logging/activity";
	}

	read_logs(Date) {
		return BASE_URL + "/logging/activity/" + Date;
	}
}

export default new ActivityLog();
