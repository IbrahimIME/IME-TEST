const BASE_URL = process.env.REACT_APP_ENDPOINT_URL + ":" + process.env.REACT_APP_SYSTEM_SETTING_PORT;

class ObjectLog {
	save_log() {
		return BASE_URL + "/object_logs";
	}

	read_log(Object_ID) {
		return BASE_URL + "/object_logs/" + Object_ID;
	}
}

export default new ObjectLog();
