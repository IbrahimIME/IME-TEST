const BASE_URL = process.env.REACT_APP_ENDPOINT_URL + ":" + process.env.REACT_APP_SYSTEM_SETTING_PORT;

class CMM {
	form(ID) {
		return BASE_URL + "/history/form/" + ID;
	}

	workflow(ID) {
		return BASE_URL + "/history/workflow/" + ID;
	}
}

export default new CMM();
