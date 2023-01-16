const BASE_URL = process.env.REACT_APP_ENDPOINT_URL + ":" + process.env.REACT_APP_SYSTEM_SETTING_PORT;

class PNO {
	company(ID) {
		return BASE_URL + "/history/company/" + ID;
	}

	business_unit(ID) {
		return BASE_URL + "/history/business_unit/" + ID;
	}

	department(ID) {
		return BASE_URL + "/history/department/" + ID;
	}

	role(ID) {
		return BASE_URL + "/history/role/" + ID;
	}

	user(ID) {
		return BASE_URL + "/history/user/" + ID;
	}
}

export default new PNO();
