const BASE_URL = process.env.REACT_APP_ENDPOINT_URL + ":" + process.env.REACT_APP_SYSTEM_SETTING_PORT;

class ImportHistory {
	get_all_history() {
		return BASE_URL + "/import_history";
	}

	add_history() {
		return BASE_URL + "/import_history";
	}

	get_single_history(ID) {
		return BASE_URL + "/import_history/" + ID;
	}
}

export default new ImportHistory();
